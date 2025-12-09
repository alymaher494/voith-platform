"""
FastAPI router for ASR transcription endpoints.
"""
import logging
from pathlib import Path
from typing import Optional
import tempfile
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Form
from fastapi.responses import JSONResponse

from .core import AudioTranscriber
from .models import TranscribeRequest, TranscribeVideoRequest, TranscriptionResult
from ..summarizer import ContentProcessor

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/asr", tags=["ASR"])

# Global instances (lazy loaded)
_transcriber = None
_summarizer = None


def get_transcriber() -> AudioTranscriber:
    """Get or create the global transcriber instance."""
    global _transcriber
    if _transcriber is None:
        try:
            _transcriber = AudioTranscriber()
            logger.info("Initialized AudioTranscriber for API")
        except Exception as e:
            logger.error(f"Failed to initialize AudioTranscriber: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"ASR service initialization failed: {str(e)}"
            )
    return _transcriber

def get_summarizer(model_size: str = "small") -> ContentProcessor:
    """Get or create the global summarizer instance with specified model size."""
    global _summarizer
    if _summarizer is None or getattr(_summarizer, 'model_size', None) != model_size:
        try:
            _summarizer = ContentProcessor()
            logger.info(f"Initialized ContentProcessor for API with {model_size} model")
        except Exception as e:
            logger.error(f"Failed to initialize ContentProcessor: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Summarizer service initialization failed: {str(e)}"
            )
    return _summarizer


@router.post("/transcribe/audio", response_model=TranscriptionResult)
async def transcribe_audio(
    request: TranscribeRequest,
    background_tasks: BackgroundTasks,
    correct_typos: bool = False,
    summarize_content: bool = False,
    summarizer_model: str = "small"
):
    """
    Transcribe an audio file with word-level timestamps.

    - **audio_path**: Path to audio file on server
    - **language**: Optional language code (auto-detect if not provided)
    - **model_size**: Whisper model size (tiny, base, small, medium, large)
    - **compute_type**: Compute precision (float16, float32, int8)
    - **batch_size**: Processing batch size
    - **correct_typos**: Apply typo correction to transcription (optional)
    - **summarize_content**: Summarize the transcribed content using mT5 (optional)
    - **summarizer_model**: mT5 model size for summarization ('small', 'base', 'large')
    """
    try:
        transcriber = get_transcriber()

        # Validate audio file exists
        if not Path(request.audio_path).exists():
            raise HTTPException(status_code=404, detail="Audio file not found")

        logger.info(f"Starting audio transcription: {request.audio_path}")

        # Run transcription
        result = transcriber.transcribe_audio(
            audio_path=request.audio_path,
            language=request.language,
            model_size=request.model_size,
            batch_size=request.batch_size,
            translate_to=None,  # Will be handled in post-processing if needed
            context=request.context,
            correct_typos=correct_typos
        )

        # Handle summarization if requested
        if summarize_content and result.text.strip():
            try:
                summarizer = get_summarizer(summarizer_model)
                # Use translated text if available, otherwise original text
                text_to_summarize = result.translated_text if result.translated_text else result.text
                result.summarized_content = summarizer.summarize(text_to_summarize)
                logger.info("Successfully summarized transcription content")
            except Exception as e:
                logger.warning(f"Summarization failed: {e}")
                # Continue without summarization rather than failing the whole request

        logger.info(f"Audio transcription completed: {len(result.segments)} segments")
        return result

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Audio transcription failed: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@router.post("/transcribe/video", response_model=TranscriptionResult)
async def transcribe_video(
    request: TranscribeVideoRequest,
    background_tasks: BackgroundTasks,
    correct_typos: bool = False,
    summarize_content: bool = False,
    summarizer_model: str = "small"
):
    """
    Transcribe a video file by extracting audio first.

    - **video_path**: Path to video file on server
    - **language**: Optional language code (auto-detect if not provided)
    - **model_size**: Whisper model size
    - **extract_audio_format**: Audio format to extract (wav, mp3, etc.)
    - **compute_type**: Compute precision
    - **batch_size**: Processing batch size
    - **correct_typos**: Apply typo correction to transcription (optional)
    - **summarize_content**: Summarize the transcribed content using mT5 (optional)
    - **summarizer_model**: mT5 model size for summarization ('small', 'base', 'large')
    """
    try:
        transcriber = get_transcriber()

        # Validate video file exists
        if not Path(request.video_path).exists():
            raise HTTPException(status_code=404, detail="Video file not found")

        logger.info(f"Starting video transcription: {request.video_path}")

        # Run transcription
        result = transcriber.transcribe_video(
            video_path=request.video_path,
            language=request.language,
            model_size=request.model_size,
            extract_audio_format=request.extract_audio_format,
            batch_size=request.batch_size,
            context=request.context,
            correct_typos=correct_typos
        )

        # Handle summarization if requested
        if summarize_content and result.text.strip():
            try:
                summarizer = get_summarizer(summarizer_model)
                # Use translated text if available, otherwise original text
                text_to_summarize = result.translated_text if result.translated_text else result.text
                result.summarized_content = summarizer.summarize(text_to_summarize)
                logger.info("Successfully summarized video transcription content")
            except Exception as e:
                logger.warning(f"Summarization failed: {e}")
                # Continue without summarization rather than failing the whole request

        logger.info(f"Video transcription completed: {len(result.segments)} segments")
        return result

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Video transcription failed: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@router.post("/transcribe/audio/upload", response_model=TranscriptionResult)
async def transcribe_uploaded_audio(
    file: UploadFile = File(...),
    language: Optional[str] = None,
    model_size: str = "base",
    compute_type: str = "float16",
    batch_size: int = 16,
    correct_typos: bool = Form(False, description="Apply typo correction to transcription"),
    summarize_content: bool = Form(False, description="Summarize the transcribed content using mT5"),
    summarizer_model: str = Form("small", description="mT5 model size for summarization ('small', 'base', 'large')"),
    background_tasks: BackgroundTasks = None
):
    """
    Transcribe an uploaded audio file.

    - **file**: Audio file upload
    - **language**: Optional language code
    - **model_size**: Whisper model size
    - **compute_type**: Compute precision
    - **batch_size**: Processing batch size
    - **correct_typos**: Apply typo correction to transcription
    - **summarize_content**: Summarize the transcribed content using mT5
    - **summarizer_model**: mT5 model size for summarization ('small', 'base', 'large')
    """
    temp_path = None

    try:
        # Validate file type
        allowed_extensions = {'.wav', '.mp3', '.flac', '.m4a', '.ogg', '.aac'}
        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name

        logger.info(f"Uploaded audio file: {file.filename} -> {temp_path}")

        # Create transcription request
        request = TranscribeRequest(
            audio_path=temp_path,
            language=language,
            model_size=model_size,
            compute_type=compute_type,
            batch_size=batch_size
        )

        # Add cleanup task
        if background_tasks:
            background_tasks.add_task(Path(temp_path).unlink, missing_ok=True)

        # Transcribe
        transcriber = get_transcriber()
        result = transcriber.transcribe_audio(
            audio_path=request.audio_path,
            language=request.language,
            model_size=request.model_size,
            batch_size=request.batch_size,
            correct_typos=correct_typos
        )

        # Handle summarization if requested
        if summarize_content and result.text.strip():
            try:
                summarizer = get_summarizer(summarizer_model)
                # Use translated text if available, otherwise original text
                text_to_summarize = result.translated_text if result.translated_text else result.text
                result.summarized_content = summarizer.summarize(text_to_summarize)
                logger.info("Successfully summarized uploaded audio transcription content")
            except Exception as e:
                logger.warning(f"Summarization failed: {e}")
                # Continue without summarization rather than failing the whole request

        logger.info(f"Upload transcription completed: {len(result.segments)} segments")
        return result

    except HTTPException:
        # Clean up temp file if it exists
        if temp_path and Path(temp_path).exists():
            try:
                Path(temp_path).unlink()
            except:
                pass
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Clean up temp file if it exists
        if temp_path and Path(temp_path).exists():
            try:
                Path(temp_path).unlink()
            except:
                pass

        logger.error(f"Upload transcription failed: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@router.post("/transcribe/video/upload", response_model=TranscriptionResult)
async def transcribe_uploaded_video(
    file: UploadFile = File(...),
    language: Optional[str] = None,
    model_size: str = "base",
    extract_audio_format: str = "wav",
    compute_type: str = "float16",
    batch_size: int = 16,
    correct_typos: bool = Form(False, description="Apply typo correction to transcription"),
    summarize_content: bool = Form(False, description="Summarize the transcribed content using mT5"),
    summarizer_model: str = Form("small", description="mT5 model size for summarization ('small', 'base', 'large')"),
    background_tasks: BackgroundTasks = None
):
    """
    Transcribe an uploaded video file.

    - **file**: Video file upload
    - **language**: Optional language code
    - **model_size**: Whisper model size
    - **extract_audio_format**: Audio format to extract
    - **compute_type**: Compute precision
    - **batch_size**: Processing batch size
    - **correct_typos**: Apply typo correction to transcription
    - **summarize_content**: Summarize the transcribed content using mT5
    - **summarizer_model**: mT5 model size for summarization ('small', 'base', 'large')
    """
    temp_path = None

    try:
        # Validate file type
        allowed_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'}
        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name

        logger.info(f"Uploaded video file: {file.filename} -> {temp_path}")

        # Create transcription request
        request = TranscribeVideoRequest(
            video_path=temp_path,
            language=language,
            model_size=model_size,
            extract_audio_format=extract_audio_format,
            compute_type=compute_type,
            batch_size=batch_size
        )

        # Add cleanup task
        if background_tasks:
            background_tasks.add_task(Path(temp_path).unlink, missing_ok=True)

        # Transcribe
        transcriber = get_transcriber()
        result = transcriber.transcribe_video(
            video_path=request.video_path,
            language=request.language,
            model_size=request.model_size,
            extract_audio_format=request.extract_audio_format,
            batch_size=request.batch_size,
            correct_typos=correct_typos
        )

        # Handle summarization if requested
        if summarize_content and result.text.strip():
            try:
                summarizer = get_summarizer(summarizer_model)
                # Use translated text if available, otherwise original text
                text_to_summarize = result.translated_text if result.translated_text else result.text
                result.summarized_content = summarizer.summarize(text_to_summarize)
                logger.info("Successfully summarized uploaded video transcription content")
            except Exception as e:
                logger.warning(f"Summarization failed: {e}")
                # Continue without summarization rather than failing the whole request

        logger.info(f"Upload video transcription completed: {len(result.segments)} segments")
        return result

    except HTTPException:
        # Clean up temp file if it exists
        if temp_path and Path(temp_path).exists():
            try:
                Path(temp_path).unlink()
            except:
                pass
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Clean up temp file if it exists
        if temp_path and Path(temp_path).exists():
            try:
                Path(temp_path).unlink()
            except:
                pass

        logger.error(f"Upload video transcription failed: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@router.get("/languages")
async def get_supported_languages():
    """Get list of supported languages."""
    try:
        transcriber = get_transcriber()
        languages = transcriber.get_supported_languages()
        return {"languages": languages, "count": len(languages)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get languages: {str(e)}")


@router.get("/models")
async def get_model_sizes():
    """Get available model sizes."""
    try:
        transcriber = get_transcriber()
        models = transcriber.get_model_sizes()
        return {"models": models, "recommended": "base"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get models: {str(e)}")


@router.get("/health")
async def health_check():
    """Check if ASR service is healthy."""
    try:
        transcriber = get_transcriber()
        return {
            "status": "healthy",
            "device": transcriber.device,
            "compute_type": transcriber.compute_type,
            "models_loaded": len(transcriber.models)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }