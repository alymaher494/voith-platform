
import os
import sys
import subprocess
from dotenv import load_dotenv
from supabase import create_client

def check_ffmpeg():
    print("[1] Checking FFmpeg...")
    try:
        result = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            version_line = result.stdout.decode().split('\n')[0]
            print(f"✅ FFmpeg found: {version_line}")
            return True
        else:
            print("❌ FFmpeg command failed.")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg binary not found in PATH.")
        return False

def check_env_vars():
    print("\n[2] Checking Environment Variables...")
    load_dotenv()
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    
    missing = []
    if not url: missing.append("SUPABASE_URL")
    if not key: missing.append("SUPABASE_SERVICE_KEY")
    
    if missing:
        print(f"❌ Missing keys in .env: {', '.join(missing)}")
        return False, url, key
    
    print("✅ All required Supabase keys are present.")
    return True, url, key

def check_supabase(url, key):
    print("\n[3] Checking Supabase Connection...")
    if not url or not key:
        print("⏭️  Skipping Supabase check due to missing keys.")
        return False

    try:
        # Initialize client
        client = create_client(url, key)
        
        # Try a simple read operation. 
        # Using count of 'files' table. If table doesn't exist, this might error, which is also good info.
        response = client.table("files").select("*", count="exact").limit(1).execute()
        
        print(f"✅ Connection successful! Found {response.count} rows in 'files' table.")
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {str(e)}")
        # Specific hint for common error
        if "relation \"public.files\" does not exist" in str(e):
             print("   (Hint: The database connection works, but the table 'files' is missing.)")
        return False

def main():
    print("🔍 Starting System Diagnostic...")
    print("="*40)
    
    ffmpeg_ok = check_ffmpeg()
    env_ok, url, key = check_env_vars()
    supabase_ok = check_supabase(url, key)
    
    print("="*40)
    print("Diagnostic Complete.")

if __name__ == "__main__":
    main()
