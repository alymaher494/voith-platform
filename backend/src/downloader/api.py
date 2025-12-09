"""
FastAPI endpoints for the video downloader.

This module provides REST API endpoints for video downloading functionality,
including format listing and download operations with background processing.
"""
import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

# Add project root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from .utils import parse_time, validate_time_range
from .generic import GenericDownloader

# Configure logging for API operations
logger = logging.getLogger(__name__)

# Create router for downloader endpoints
router = APIRouter(prefix="/downloader", tags=["downloader"])

# Pydantic models for API request/response validation

class DownloadRequest(BaseModel):
    """
    Request model for video download operations.

    Defines the structure and validation for download requests including
    optional parameters for customization.
    """
    url: str = Field(..., description="Video URL to download from any supported platform")
    output_dir: Optional[str] = Field("./downloads", description="Directory to save downloaded files")
    start_time: Optional[str] = Field(None, description="Start time for video slicing (format: mm:ss or hh:mm:ss)")
    end_time: Optional[str] = Field(None, description="End time for video slicing (format: mm:ss or hh:mm:ss)")
    audio_only: Optional[bool] = Field(False, description="Extract audio only as MP3 format")
    format_id: Optional[str] = Field(None, description="Specific format ID to download (from /formats endpoint)")

    class Config:
        """Pydantic configuration for the model."""
        schema_extra = {
            "example": {
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "output_dir": "./downloads",
                "start_time": "1:30",
                "end_time": "5:45",
                "audio_only": False,
                "format_id": "22"
            }
        }


class FormatResponse(BaseModel):
    """
    Response model for video format information.

    Contains details about available video/audio formats for a given URL.
    """
    format_id: str = Field(..., description="Unique identifier for the format")
    ext: str = Field(..., description="File extension (e.g., 'mp4', 'webm')")
    resolution: str = Field(..., description="Video resolution or 'audio' for audio-only")
    note: str = Field(..., description="Additional format information or quality notes")


class DownloadResponse(BaseModel):
    """
    Response model for download operations.

    Provides feedback about the download initiation and basic result information.
    """
    success: bool = Field(..., description="Whether the download was successfully initiated")
    message: str = Field(..., description="Human-readable status message")
    output_dir: Optional[str] = Field(None, description="Output directory where files will be saved")
    platform: Optional[str] = Field(None, description="Detected platform name")
    platform_info: Optional[Dict[str, Any]] = Field(None, description="Additional platform metadata")


@router.get("/formats/{url:path}")
async def get_formats(url: str):
    """
    Retrieve available video/audio formats for a given URL.

    This endpoint analyzes the provided video URL and returns all available
    download formats including resolutions, file types, and quality options.
    Useful for format selection before downloading.

    Args:
        url (str): Video URL to analyze (can be URL-encoded)

    Returns:
        dict: Contains 'formats' key with list of FormatResponse objects

    Raises:
        HTTPException: 404 if no formats found, 500 for processing errors
    """
    try:
        logger.info(f"Getting formats for URL: {url}")
        downloader = GenericDownloader()
        formats = downloader.get_available_resolutions(url)

        if not formats:
            logger.warning(f"No formats found for URL: {url}")
            raise HTTPException(
                status_code=404,
                detail="No formats found for this URL. Please check the URL is valid and accessible."
            )

        logger.info(f"Found {len(formats)} formats for URL")
        return {"formats": formats}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get formats for {url}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve formats: {str(e)}. Please try again later."
        )


@router.post("/download", response_model=DownloadResponse)
async def download_video(request: DownloadRequest, background_tasks: BackgroundTasks):
    """
    Initiate video download with customizable options.

    This endpoint starts a background download process for the specified video URL.
    The download runs asynchronously, allowing the API to handle multiple concurrent requests.
    Progress and completion are logged but not streamed back in real-time.

    Args:
        request (DownloadRequest): Download configuration including URL and options
        background_tasks (BackgroundTasks): FastAPI background task manager

    Returns:
        DownloadResponse: Confirmation that download was initiated

    Raises:
        HTTPException: 400 for validation errors, 500 for processing errors
    """
    try:
        logger.info(f"Starting download for URL: {request.url}")

        # Parse and validate time parameters for video slicing
        start_time = parse_time(request.start_time) if request.start_time else None
        end_time = parse_time(request.end_time) if request.end_time else None

        # Validate time range if both times are provided
        if start_time is not None and end_time is not None:
            validate_time_range(start_time, end_time)

        # Initialize downloader with specified output directory
        downloader = GenericDownloader(request.output_dir)

        # Queue download task to run in background
        background_tasks.add_task(
            perform_download,
            downloader=downloader,
            url=request.url,
            start_time=start_time,
            end_time=end_time,
            audio_only=request.audio_only,
            format_id=request.format_id
        )

        logger.info(f"Download queued for {request.url}")
        return DownloadResponse(
            success=True,
            message="Download started in background. Check logs for progress.",
            output_dir=request.output_dir
        )

    except ValueError as e:
        logger.warning(f"Validation error for download request: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid request parameters: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Failed to start download for {request.url}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start download: {str(e)}. Please try again later."
        )


async def perform_download(
    downloader: GenericDownloader,
    url: str,
    start_time: Optional[int],
    end_time: Optional[int],
    audio_only: bool,
    format_id: Optional[str]
) -> None:
    """
    Background task that performs the actual video download.

    This function runs in a separate thread/process and handles the complete
    download workflow including error handling and logging.

    Args:
        downloader (GenericDownloader): Configured downloader instance
        url (str): Video URL to download
        start_time (Optional[int]): Start time in seconds for slicing
        end_time (Optional[int]): End time in seconds for slicing
        audio_only (bool): Whether to extract audio only
        format_id (Optional[str]): Specific format ID to download
    """
    try:
        logger.info(f"Starting background download for: {url}")

        # Use context manager for automatic cleanup
        with downloader:
            result = downloader.download(
                url=url,
                start_time=start_time,
                end_time=end_time,
                audio_only=audio_only,
                format_id=format_id
            )

            # Log successful completion with details
            output_dir = result.get('output_dir', 'unknown')
            platform = result.get('platform', 'unknown')
            logger.info(f"✅ Download completed successfully!")
            logger.info(f"📁 Files saved to: {output_dir}")
            logger.info(f"🎬 Platform: {platform}")

    except Exception as e:
        logger.error(f"❌ Download failed for {url}: {str(e)}")