"""
FastAPI endpoints for the converter library.

This module provides REST API endpoints for audio and video conversion operations,
including format conversion, compression, and metadata extraction.
"""
import logging
import shutil
from pathlib import Path
from typing import Optional, Dict, Any

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .audio import AudioConverter
from .video import VideoConverter

# Configure logging for API operations
logger = logging.getLogger(__name__)

# Create router for converter endpoints
router = APIRouter(prefix="/converter", tags=["converter"])

# Initialize converters
audio_converter = AudioConverter()
video_converter = VideoConverter()

# Pydantic models for API request/response validation

class ConversionResponse(BaseModel):
    """
    Response model for conversion operations.
    """
    success: bool = Field(..., description="Whether the conversion was successful")
    message: str = Field(..., description="Human-readable status message")
    output_file: Optional[str] = Field(None, description="Path to the converted file")
    input_file: Optional[str] = Field(None, description="Original input file path")
    conversion_type: Optional[str] = Field(None, description="Type of conversion performed")


class AudioConversionRequest(BaseModel):
    """
    Request model for audio conversion operations.
    """
    input_format: str = Field(..., description="Input audio format (e.g., 'mp3', 'wav')")
    output_format: str = Field(..., description="Target audio format (e.g., 'wav', 'mp3', 'flac')")
    bitrate: Optional[str] = Field("192k", description="Audio bitrate for compressed formats")
    sample_rate: Optional[int] = Field(44100, description="Sample rate in Hz")


class VideoConversionRequest(BaseModel):
    """
    Request model for video conversion operations.
    """
    input_format: str = Field(..., description="Input video format")
    output_format: str = Field(..., description="Target video format (e.g., 'mp4', 'webm', 'avi')")
    resolution: Optional[str] = Field(None, description="Target resolution (e.g., '1920x1080')")
    quality: Optional[str] = Field("medium", description="Compression quality ('high', 'medium', 'low')")
    video_bitrate: Optional[str] = Field(None, description="Video bitrate")
    audio_bitrate: Optional[str] = Field("128k", description="Audio bitrate")


@router.post("/convert/audio", response_model=ConversionResponse)
async def convert_audio(
    file: UploadFile = File(...),
    output_format: str = Form(..., description="Target audio format"),
    bitrate: Optional[str] = Form("192k", description="Audio bitrate"),
    sample_rate: Optional[int] = Form(44100, description="Sample rate")
):
    """
    Convert uploaded audio file to specified format.

    This endpoint accepts an audio file upload and converts it to the specified
    output format with customizable quality settings.

    Args:
        file: Audio file to convert
        output_format: Target format (mp3, wav, flac, aac)
        bitrate: Audio bitrate for compressed formats
        sample_rate: Sample rate in Hz

    Returns:
        ConversionResponse: Conversion result with file path
    """
    try:
        # Validate input
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        # Create temporary input file
        temp_dir = Path("./temp")
        temp_dir.mkdir(exist_ok=True)

        input_path = temp_dir / f"input_{file.filename}"
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Converting audio file: {file.filename} to {output_format}")

        # Perform conversion
        output_path = audio_converter.convert_audio_format(
            str(input_path),
            output_format,
            bitrate=bitrate,
            sample_rate=sample_rate
        )

        # Clean up temp file
        input_path.unlink(missing_ok=True)

        if output_path:
            return ConversionResponse(
                success=True,
                message=f"Audio converted successfully to {output_format}",
                output_file=output_path,
                input_file=file.filename,
                conversion_type="audio_format"
            )
        else:
            raise HTTPException(status_code=500, detail="Audio conversion failed")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Audio conversion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")


@router.post("/convert/video", response_model=ConversionResponse)
async def convert_video(
    file: UploadFile = File(...),
    output_format: str = Form(..., description="Target video format"),
    resolution: Optional[str] = Form(None, description="Target resolution"),
    quality: Optional[str] = Form("medium", description="Compression quality"),
    video_bitrate: Optional[str] = Form(None, description="Video bitrate"),
    audio_bitrate: Optional[str] = Form("128k", description="Audio bitrate")
):
    """
    Convert uploaded video file to specified format.

    This endpoint accepts a video file upload and converts it to the specified
    output format with customizable quality and resolution settings.

    Args:
        file: Video file to convert
        output_format: Target format (mp4, webm, avi, mkv)
        resolution: Target resolution (e.g., '1920x1080')
        quality: Compression quality (high, medium, low)
        video_bitrate: Video bitrate
        audio_bitrate: Audio bitrate

    Returns:
        ConversionResponse: Conversion result with file path
    """
    try:
        # Validate input
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        # Create temporary input file
        temp_dir = Path("./temp")
        temp_dir.mkdir(exist_ok=True)

        input_path = temp_dir / f"input_{file.filename}"
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Converting video file: {file.filename} to {output_format}")

        # Perform conversion
        output_path = video_converter.convert_video_format(
            str(input_path),
            output_format,
            resolution=resolution,
            quality=quality,
            video_bitrate=video_bitrate,
            audio_bitrate=audio_bitrate
        )

        # Clean up temp file
        input_path.unlink(missing_ok=True)

        if output_path:
            return ConversionResponse(
                success=True,
                message=f"Video converted successfully to {output_format}",
                output_file=output_path,
                input_file=file.filename,
                conversion_type="video_format"
            )
        else:
            raise HTTPException(status_code=500, detail="Video conversion failed")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Video conversion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")


@router.post("/convert/audio/extract", response_model=ConversionResponse)
async def extract_audio_from_video(
    file: UploadFile = File(...),
    audio_format: str = Form("mp3", description="Audio format to extract")
):
    """
    Extract audio track from uploaded video file.

    Args:
        file: Video file to extract audio from
        audio_format: Audio format (mp3, wav, aac)

    Returns:
        ConversionResponse: Extraction result with audio file path
    """
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        temp_dir = Path("./temp")
        temp_dir.mkdir(exist_ok=True)

        input_path = temp_dir / f"input_{file.filename}"
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Extracting audio from video: {file.filename}")

        output_path = video_converter.extract_audio_from_video(
            str(input_path),
            audio_format
        )

        input_path.unlink(missing_ok=True)

        if output_path:
            return ConversionResponse(
                success=True,
                message=f"Audio extracted successfully as {audio_format}",
                output_file=output_path,
                input_file=file.filename,
                conversion_type="audio_extraction"
            )
        else:
            raise HTTPException(status_code=500, detail="Audio extraction failed")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Audio extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@router.post("/convert/video/compress", response_model=ConversionResponse)
async def compress_video(
    file: UploadFile = File(...),
    quality: str = Form("medium", description="Compression quality")
):
    """
    Compress uploaded video file to reduce file size.

    Args:
        file: Video file to compress
        quality: Compression quality (high, medium, low)

    Returns:
        ConversionResponse: Compression result with compressed file path
    """
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        temp_dir = Path("./temp")
        temp_dir.mkdir(exist_ok=True)

        input_path = temp_dir / f"input_{file.filename}"
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Compressing video: {file.filename} with {quality} quality")

        output_path = video_converter.compress_video(
            str(input_path),
            quality=quality
        )

        input_path.unlink(missing_ok=True)

        if output_path:
            return ConversionResponse(
                success=True,
                message=f"Video compressed successfully with {quality} quality",
                output_file=output_path,
                input_file=file.filename,
                conversion_type="video_compression"
            )
        else:
            raise HTTPException(status_code=500, detail="Video compression failed")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Video compression error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Compression failed: {str(e)}")


@router.get("/info/audio/{file_path:path}")
async def get_audio_info(file_path: str):
    """
    Get information about an audio file.

    Args:
        file_path: Path to the audio file

    Returns:
        dict: Audio file information
    """
    try:
        info = audio_converter.get_audio_info(file_path)
        if info:
            return {"file_info": info}
        else:
            raise HTTPException(status_code=404, detail="Could not read audio file information")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting audio info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get audio info: {str(e)}")


@router.get("/info/video/{file_path:path}")
async def get_video_info(file_path: str):
    """
    Get information about a video file.

    Args:
        file_path: Path to the video file

    Returns:
        dict: Video file information
    """
    try:
        info = video_converter.get_video_info(file_path)
        if info:
            return {"file_info": info}
        else:
            raise HTTPException(status_code=404, detail="Could not read video file information")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting video info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get video info: {str(e)}")