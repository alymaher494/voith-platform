"""
Utility functions for ASR processing.
"""
import logging
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


def validate_audio_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate if a file is a supported audio format.

    Args:
        file_path: Path to the audio file

    Returns:
        Tuple of (is_valid, error_message)
    """
    path = Path(file_path)

    if not path.exists():
        return False, f"File does not exist: {file_path}"

    if not path.is_file():
        return False, f"Path is not a file: {file_path}"

    # Supported audio formats
    supported_extensions = {
        '.wav', '.mp3', '.flac', '.m4a', '.ogg', '.aac',
        '.wma', '.aiff', '.au', '.ra', '.ape'
    }

    file_ext = path.suffix.lower()
    if file_ext not in supported_extensions:
        return False, f"Unsupported audio format: {file_ext}. Supported: {', '.join(sorted(supported_extensions))}"

    # Check file size (max 500MB for safety)
    max_size = 500 * 1024 * 1024  # 500MB
    if path.stat().st_size > max_size:
        return False, f"File too large: {path.stat().st_size / (1024*1024):.1f}MB. Maximum allowed: {max_size / (1024*1024)}MB"

    return True, ""


def validate_video_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate if a file is a supported video format.

    Args:
        file_path: Path to the video file

    Returns:
        Tuple of (is_valid, error_message)
    """
    path = Path(file_path)

    if not path.exists():
        return False, f"File does not exist: {file_path}"

    if not path.is_file():
        return False, f"Path is not a file: {file_path}"

    # Supported video formats
    supported_extensions = {
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv',
        '.webm', '.m4v', '.3gp', '.mpg', '.mpeg'
    }

    file_ext = path.suffix.lower()
    if file_ext not in supported_extensions:
        return False, f"Unsupported video format: {file_ext}. Supported: {', '.join(sorted(supported_extensions))}"

    # Check file size (max 2GB for safety)
    max_size = 2 * 1024 * 1024 * 1024  # 2GB
    if path.stat().st_size > max_size:
        return False, f"File too large: {path.stat().st_size / (1024*1024*1024):.1f}GB. Maximum allowed: {max_size / (1024*1024*1024)}GB"

    return True, ""


def get_audio_duration(file_path: str) -> Optional[float]:
    """
    Get audio file duration using ffprobe.

    Args:
        file_path: Path to audio file

    Returns:
        Duration in seconds, or None if failed
    """
    try:
        import subprocess
        import json

        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            file_path
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            data = json.loads(result.stdout)
            duration = float(data['format']['duration'])
            return duration

    except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError, ValueError) as e:
        logger.warning(f"Failed to get audio duration for {file_path}: {e}")

    return None


def format_timestamp(seconds: float) -> str:
    """
    Format seconds into HH:MM:SS.mmm or MM:SS.mmm format.

    Args:
        seconds: Time in seconds

    Returns:
        Formatted timestamp string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:05.2f}"
    elif minutes > 0:
        return f"{minutes:02d}:{secs:05.2f}"
    else:
        return f"{secs:05.2f}"


def estimate_transcription_time(audio_duration: float, model_size: str) -> float:
    """
    Estimate transcription processing time based on audio duration and model.

    Args:
        audio_duration: Audio duration in seconds
        model_size: Model size (tiny, base, small, medium, large)

    Returns:
        Estimated processing time in seconds
    """
    # Rough estimates based on typical WhisperX performance
    # These are conservative estimates and actual times may vary
    model_multipliers = {
        'tiny': 0.3,    # ~0.3x audio duration
        'base': 0.5,    # ~0.5x audio duration
        'small': 0.8,   # ~0.8x audio duration
        'medium': 1.2,  # ~1.2x audio duration
        'large': 2.0    # ~2.0x audio duration
    }

    multiplier = model_multipliers.get(model_size, 1.0)
    base_time = audio_duration * multiplier

    # Add fixed overhead for model loading and alignment
    overhead = 10.0  # 10 seconds

    return base_time + overhead


def cleanup_temp_files(*file_paths: str) -> None:
    """
    Clean up temporary files safely.

    Args:
        *file_paths: Paths to files to delete
    """
    for file_path in file_paths:
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                logger.debug(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to clean up {file_path}: {e}")