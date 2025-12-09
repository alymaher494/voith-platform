"""
Pydantic models for ASR service.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class WordTimestamp(BaseModel):
    """Word-level timestamp information."""
    word: str = Field(..., description="The transcribed word")
    start: float = Field(..., description="Start time in seconds")
    end: float = Field(..., description="End time in seconds")
    confidence: Optional[float] = Field(None,
                                        description="Confidence score (0-1)")


class TranscriptionSegment(BaseModel):
    """Transcription segment with timestamps."""
    text: str = Field(..., description="Transcribed text for this segment")
    translated_text: Optional[str] = Field(
        None, description="Translated text (if translation enabled)")
    start: float = Field(..., description="Start time in seconds")
    end: float = Field(..., description="End time in seconds")
    words: List[WordTimestamp] = Field(default_factory=list,
                                       description="Word-level timestamps")


class TranscriptionResult(BaseModel):
    """Complete transcription result."""
    text: str = Field(..., description="Full transcribed text")
    translated_text: Optional[str] = Field(
        None, description="Full translated text (if translation enabled)")
    summarized_content: Optional[str] = Field(
        None, description="Summarized content (if summarization enabled)")
    language: str = Field(..., description="Detected language code")
    segments: List[TranscriptionSegment] = Field(
        default_factory=list, description="Transcription segments")
    processing_time: float = Field(...,
                                    description="Processing time in seconds")
    model: str = Field(..., description="ASR model used")
    confidence: Optional[float] = Field(None,
                                         description="Overall confidence score")


class TranscribeRequest(BaseModel):
    """Request model for transcription."""
    audio_path: str = Field(..., description="Path to audio file")
    language: Optional[str] = Field(
        None, description="Language code (auto-detect if None)")
    model_size: str = Field(
        "base",
        description="Whisper model size: tiny, base, small, medium, large")
    compute_type: str = Field("float16",
                              description="Compute type for inference")
    batch_size: int = Field(16, description="Batch size for processing")
    correct_typos: bool = Field(False, description="Apply typo correction to transcription")
    context: bool = Field(False, description="Use contextual translation (better quality, slower)")


class TranscribeVideoRequest(BaseModel):
    """Request model for video transcription."""
    video_path: str = Field(..., description="Path to video file")
    language: Optional[str] = Field(
        None, description="Language code (auto-detect if None)")
    model_size: str = Field("base", description="Whisper model size")
    extract_audio_format: str = Field(
        "wav", description="Audio format to extract from video")
    compute_type: str = Field("float16",
                              description="Compute type for inference")
    batch_size: int = Field(16, description="Batch size for processing")
    correct_typos: bool = Field(False, description="Apply typo correction to transcription")
