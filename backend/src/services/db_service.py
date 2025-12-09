
import os
import mimetypes
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")

class DBService:
    def __init__(self):
        self.client: Client = None
        if SUPABASE_URL and SUPABASE_KEY:
            try:
                self.client = create_client(SUPABASE_URL, SUPABASE_KEY)
            except Exception as e:
                print(f"⚠️ Failed to initialize Supabase client: {e}")
        else:
            print("⚠️ Supabase credentials not found in env. DB/Storage features disabled.")

    def upload_file(self, file_path: str, bucket_name: str = "processed_files") -> str:
        """
        Uploads a file to Supabase Storage and returns the public URL or path.
        """
        if not self.client:
            return None

        path_obj = Path(file_path)
        if not path_obj.exists():
            return None

        file_name = path_obj.name
        # Simple path strategy: just the filename. 
        # For production, might want 'user_id/timestamp_filename' to avoid collisions.
        storage_path = f"{file_name}" 
        
        try:
            # Guess mime type
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = "application/octet-stream"

            with open(file_path, 'rb') as f:
                self.client.storage.from_(bucket_name).upload(
                    file=f,
                    path=storage_path,
                    file_options={"content-type": mime_type, "upsert": "true"}
                )
            
            # Get public URL (optional, depending on if bucket is public)
            # stored_url = self.client.storage.from_(bucket_name).get_public_url(storage_path)
            return storage_path

        except Exception as e:
            print(f"Error uploading file to Supabase: {e}")
            return None

    def save_file_record(self, filename: str, storage_path: str, size_bytes: int, user_id: str = None):
        """
        Inserts a record into the 'files' table.
        """
        if not self.client:
            return None

        try:
            data = {
                "filename": filename,
                "storage_path": storage_path,
                "size_bytes": size_bytes,
                # "user_id": user_id  # Uncomment if you have user_id available
            }
            if user_id:
                data["user_id"] = user_id

            response = self.client.table("files").insert(data).execute()
            return response
        except Exception as e:
            print(f"Error saving file record to Supabase: {e}")
            return None

    def get_usage_metrics(self, user_id: str):
        """
        Fetch usage metrics for a specific user.
        """
        if not self.client:
            return None
        try:
            response = self.client.table("usage_metrics").select("*").eq("user_id", user_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error fetching usage metrics: {e}")
            return None

    def update_usage_metrics(self, user_id: str, minutes_added: float, storage_added_bytes: int):
        """
        Increment usage metrics for a user using an RPC call or direct update.
        Here we fetch first then update for simplicity, though RPC 'increment' is better for concurrency.
        """
        if not self.client:
            return None
        try:
            # Fetch current
            print(f"Updating usage for user: {user_id} (+{minutes_added} mins, +{storage_added_bytes} bytes)")
            current = self.get_usage_metrics(user_id)
            
            if not current:
                # Create if not exists (Upsert-ish logic)
                print(f"Metrics not found for {user_id}. Creating new record.")
                self.client.table("usage_metrics").insert({
                    "user_id": user_id,
                    "minutes_processed": minutes_added,
                    "storage_used_bytes": storage_added_bytes
                }).execute()
                return {"status": "created"}

            new_minutes = (current.get('minutes_processed') or 0) + minutes_added
            new_storage = (current.get('storage_used_bytes') or 0) + storage_added_bytes
            
            response = self.client.table("usage_metrics").update({
                "minutes_processed": new_minutes,
                "storage_used_bytes": new_storage
            }).eq("user_id", user_id).execute()
            
            return response
        except Exception as e:
            print(f"Error updating usage metrics: {e}")
            return None

# Singleton instance
db_service = DBService()
