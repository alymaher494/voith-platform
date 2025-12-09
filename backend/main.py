
import os
import ctypes
import logging
import sys
import shutil
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks, Depends, Header, status

# ... imports ...

# Import DB Service
from src.services.db_service import db_service

# --- "The Gatekeeper" Logic ---

async def get_current_user(authorization: str = Header(None)):
    """
    Verifies the Supabase JWT token and returns the user_id.
    """
    if not authorization:
        # For development/testing without auth, you might want to bypass this or throw 401
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
        return None  # Allow unauthenticated for now until frontend sends token
    
    try:
        token = authorization.replace("Bearer ", "")
        user = db_service.client.auth.get_user(token)
        if not user or not user.user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user.user.id
    except Exception as e:
        logger.error(f"Auth error: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")

def check_quota(user_id: str):
    """
    Checks if the user has exceeded their monthly limits.
    """
    if not user_id:
        return # Skip for unauthenticated
        
    metrics = db_service.get_usage_metrics(user_id)
    if not metrics:
        # If metrics don't exist, maybe create them or skip
        return

    # Default limit: 10 minutes (Free Tier)
    MONTHLY_LIMIT_MINUTES = 10.0 
    
    if metrics.get('minutes_processed', 0) >= MONTHLY_LIMIT_MINUTES:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You have exhausted your ritual energy for this month (Quota Exceeded)"
        )

# --- Direct Endpoints (As requested) ---

@app.post("/transcribe")
async def transcribe_endpoint(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None),
    bg_tasks: BackgroundTasks = None,
    # Authorization Dependency (The Gatekeeper)
    user_id: Optional[str] = Depends(get_current_user) 
):
    print(f"🔐 Authenticated User ID: {user_id}")
    """
    Direct endpoint to transcribe an uploaded audio/video file.
    Wraps logic from transcribe_audio.py.
    """
    
    # 1. Quota Check (Before Processing)
    if user_id:
        check_quota(user_id)
    
    temp_path = None
    try:
        # Save upload to temp file
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            temp_path = tmp.name
        
        logger.info(f"Processing transcription for: {file.filename}")
        
        # Transcribe
        transcriber = get_transcriber()
        
        if suffix.lower() in ['.mp4', '.mkv', '.avi', '.mov']:
             result = transcriber.transcribe_video(
                video_path=temp_path,
                language=language
            )
             # Basic duration estimation (improve with specific metadata extraction if needed)
             # For video, transcriber usually extracts audio, we can approximate or get from result if available
             duration_seconds = result.segments[-1].end if result.segments else 0
        else:
            result = transcriber.transcribe_audio(
                audio_path=temp_path,
                language=language
            )
            duration_seconds = result.segments[-1].end if result.segments else 0

        # --- DB Integration: Upload Original File & Save Record ---
        # Note: We are uploading the temp file we just processed
        file_size = os.path.getsize(temp_path)
        
        # Upload to Storage
        storage_path = db_service.upload_file(temp_path, bucket_name="processed_files")
        
        file_id = None
        if storage_path:
            logger.info(f"File uploaded to Supabase Storage: {storage_path}")
            # Insert DB Record
            db_response = db_service.save_file_record(
                filename=file.filename,
                storage_path=storage_path,
                size_bytes=file_size,
                user_id=user_id 
            )
            
            # Extract file_id if available
            if db_response and hasattr(db_response, 'data') and len(db_response.data) > 0:
                file_id = db_response.data[0].get('id')
        # ----------------------------------------------------

        # 2. Usage Update (After Processing)
        if user_id:
            minutes = duration_seconds / 60.0
            db_service.update_usage_metrics(user_id, minutes, file_size)

        # Cleanup temp file
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

        return {
            "text": result.text,
            "language": result.language,
            "file_id": file_id,
            "segments": [
                {"start": s.start, "end": s.end, "text": s.text} 
                for s in result.segments
            ]
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
        logger.error(f"Transcription failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
async def summarize_endpoint(request: SummarizeRequest):
    """
    Direct endpoint to summarize text.
    Wraps logic from summarize_text.py.
    """
    try:
        summarizer = get_summarizer()
        summary = summarizer.summarize(
            text=request.text,
            max_length=request.max_length,
            summary_style=request.style
        )
        return {"original_text": request.text, "summary": summary}
    except Exception as e:
        logger.error(f"Summarization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Include Full API Routers ---
app.include_router(downloader_router)
app.include_router(converter_router)
app.include_router(asr_router)
app.include_router(ocr_router)
app.include_router(summarizer_router)

@app.get("/")
def home():
    return {
        "message": "Media Processing Studio API is running",
        "docs": "http://localhost:8000/docs",
        "endpoints": ["/transcribe", "/summarize", "/downloader", "/converter", "/asr", "/ocr"]
    }

if __name__ == "__main__":
    import uvicorn
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
