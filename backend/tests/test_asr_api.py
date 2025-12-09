"""
Tests for src/asr/api.py ASR router endpoints.
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
from pathlib import Path
import tempfile
import io

from src.asr.api import router, get_transcriber
from src.asr.models import TranscribeRequest, TranscribeVideoRequest, TranscriptionResult


@pytest.fixture
def client():
    """Create a test client for the ASR router."""
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


@patch('src.asr.api.AudioTranscriber')
def test_get_transcriber_success(mock_transcriber_class):
    """Test successful transcriber initialization."""
    mock_transcriber = MagicMock()
    mock_transcriber_class.return_value = mock_transcriber

    # Reset global transcriber
    import src.asr.api
    src.asr.api._transcriber = None

    result = get_transcriber()

    assert result == mock_transcriber
    mock_transcriber_class.assert_called_once()


@patch('src.asr.api.AudioTranscriber')
def test_get_transcriber_failure(mock_transcriber_class):
    """Test transcriber initialization failure."""
    mock_transcriber_class.side_effect = Exception("Init failed")

    # Reset global transcriber
    import src.asr.api
    src.asr.api._transcriber = None

    with pytest.raises(HTTPException) as exc:
        get_transcriber()

    assert exc.value.status_code == 500
    assert "ASR service initialization failed" in exc.value.detail


@patch('src.asr.api.get_transcriber')
@patch('pathlib.Path.exists')
def test_transcribe_audio_success(mock_exists, mock_get_transcriber, client):
    """Test successful audio transcription."""
    mock_exists.return_value = True

    mock_transcriber = MagicMock()
    mock_get_transcriber.return_value = mock_transcriber

    mock_result = TranscriptionResult(
        text="Test transcription",
        language="en",
        segments=[],
        processing_time=1.0,
        model="whisperx-base",
        confidence=0.9
    )
    mock_transcriber.transcribe_audio.return_value = mock_result

    request_data = {
        "audio_path": "/path/to/audio.wav",
        "language": "en",
        "model_size": "base",
        "batch_size": 16
    }

    response = client.post("/asr/transcribe/audio", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Test transcription"
    assert data["language"] == "en"


@patch('src.asr.api.get_transcriber')
@patch('pathlib.Path.exists')
def test_transcribe_audio_file_not_found(mock_exists, mock_get_transcriber, client):
    """Test audio transcription with non-existent file."""
    mock_exists.return_value = False

    request_data = {"audio_path": "/nonexistent/audio.wav"}

    response = client.post("/asr/transcribe/audio", json=request_data)

    assert response.status_code == 404
    assert "Audio file not found" in response.json()["detail"]


@patch('src.asr.api.get_transcriber')
@patch('pathlib.Path.exists')
def test_transcribe_audio_transcription_failure(mock_exists, mock_get_transcriber, client):
    """Test audio transcription failure."""
    mock_exists.return_value = True

    mock_transcriber = MagicMock()
    mock_get_transcriber.return_value = mock_transcriber
    mock_transcriber.transcribe_audio.side_effect = Exception("Transcription failed")

    request_data = {"audio_path": "/path/to/audio.wav"}

    response = client.post("/asr/transcribe/audio", json=request_data)

    assert response.status_code == 500
    assert "Transcription failed" in response.json()["detail"]


@patch('src.asr.api.get_transcriber')
@patch('pathlib.Path.exists')
def test_transcribe_video_success(mock_exists, mock_get_transcriber, client):
    """Test successful video transcription."""
    mock_exists.return_value = True

    mock_transcriber = MagicMock()
    mock_get_transcriber.return_value = mock_transcriber

    mock_result = TranscriptionResult(
        text="Video transcription",
        language="en",
        segments=[],
        processing_time=2.0,
        model="whisperx-base",
        confidence=0.85
    )
    mock_transcriber.transcribe_video.return_value = mock_result

    request_data = {
        "video_path": "/path/to/video.mp4",
        "language": "en",
        "model_size": "base",
        "extract_audio_format": "wav"
    }

    response = client.post("/asr/transcribe/video", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Video transcription"


@patch('src.asr.api.get_transcriber')
@patch('pathlib.Path.exists')
def test_transcribe_video_file_not_found(mock_exists, mock_get_transcriber, client):
    """Test video transcription with non-existent file."""
    mock_exists.return_value = False

    request_data = {"video_path": "/nonexistent/video.mp4"}

    response = client.post("/asr/transcribe/video", json=request_data)

    assert response.status_code == 404
    assert "Video file not found" in response.json()["detail"]


@patch('src.asr.api.get_transcriber')
def test_transcribe_uploaded_audio_success(mock_get_transcriber, client):
    """Test successful uploaded audio transcription."""
    mock_transcriber = MagicMock()
    mock_get_transcriber.return_value = mock_transcriber

    mock_result = TranscriptionResult(
        text="Uploaded audio transcription",
        language="en",
        segments=[],
        processing_time=1.5,
        model="whisperx-base",
        confidence=0.9
    )
    mock_transcriber.transcribe_audio.return_value = mock_result

    # Create a mock audio file
    audio_content = b"mock audio data"
    files = {"file": ("test.wav", io.BytesIO(audio_content), "audio/wav")}

    response = client.post("/asr/transcribe/audio/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Uploaded audio transcription"


def test_transcribe_uploaded_audio_unsupported_format(client):
    """Test uploaded audio with unsupported file format."""
    files = {"file": ("test.txt", io.BytesIO(b"text content"), "text/plain")}

    response = client.post("/asr/transcribe/audio/upload", files=files)

    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


@patch('src.asr.api.get_transcriber')
def test_transcribe_uploaded_video_success(mock_get_transcriber, client):
    """Test successful uploaded video transcription."""
    mock_transcriber = MagicMock()
    mock_get_transcriber.return_value = mock_transcriber

    mock_result = TranscriptionResult(
        text="Uploaded video transcription",
        language="en",
        segments=[],
        processing_time=2.5,
        model="whisperx-base",
        confidence=0.88
    )
    mock_transcriber.transcribe_video.return_value = mock_result

    # Create a mock video file
    video_content = b"mock video data"
    files = {"file": ("test.mp4", io.BytesIO(video_content), "video/mp4")}

    response = client.post("/asr/transcribe/video/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Uploaded video transcription"


def test_transcribe_uploaded_video_unsupported_format(client):
    """Test uploaded video with unsupported file format."""
    files = {"file": ("test.txt", io.BytesIO(b"text content"), "text/plain")}

    response = client.post("/asr/transcribe/video/upload", files=files)

    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


@patch('src.asr.api.get_transcriber')
def test_get_supported_languages_success(mock_get_transcriber, client):
    """Test getting supported languages successfully."""
    mock_transcriber = MagicMock()
    mock_get_transcriber.return_value = mock_transcriber
    mock_transcriber.get_supported_languages.return_value = ["en", "fr", "es", "de"]

    response = client.get("/asr/languages")

    assert response.status_code == 200
    data = response.json()
    assert data["languages"] == ["en", "fr", "es", "de"]
    assert data["count"] == 4


@patch('src.asr.api.get_transcriber')
def test_get_supported_languages_failure(mock_get_transcriber, client):
    """Test getting supported languages failure."""
    mock_get_transcriber.side_effect = Exception("Service unavailable")

    response = client.get("/asr/languages")

    assert response.status_code == 500
    assert "Failed to get languages" in response.json()["detail"]


@patch('src.asr.api.get_transcriber')
def test_get_model_sizes_success(mock_get_transcriber, client):
    """Test getting model sizes successfully."""
    mock_transcriber = MagicMock()
    mock_get_transcriber.return_value = mock_transcriber
    mock_transcriber.get_model_sizes.return_value = ["tiny", "base", "small", "medium", "large"]

    response = client.get("/asr/models")

    assert response.status_code == 200
    data = response.json()
    assert data["models"] == ["tiny", "base", "small", "medium", "large"]
    assert data["recommended"] == "base"


@patch('src.asr.api.get_transcriber')
def test_get_model_sizes_failure(mock_get_transcriber, client):
    """Test getting model sizes failure."""
    mock_get_transcriber.side_effect = Exception("Service unavailable")

    response = client.get("/asr/models")

    assert response.status_code == 500
    assert "Failed to get models" in response.json()["detail"]


@patch('src.asr.api.get_transcriber')
def test_health_check_healthy(mock_get_transcriber, client):
    """Test health check when service is healthy."""
    mock_transcriber = MagicMock()
    mock_transcriber.device = "cuda"
    mock_transcriber.compute_type = "float16"
    mock_transcriber.models = {"base": "loaded"}
    mock_get_transcriber.return_value = mock_transcriber

    response = client.get("/asr/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["device"] == "cuda"
    assert data["compute_type"] == "float16"
    assert data["models_loaded"] == 1


@patch('src.asr.api.get_transcriber')
def test_health_check_unhealthy(mock_get_transcriber, client):
    """Test health check when service is unhealthy."""
    mock_get_transcriber.side_effect = Exception("Service initialization failed")

    response = client.get("/asr/health")

    assert response.status_code == 200  # Health endpoint always returns 200
    data = response.json()
    assert data["status"] == "unhealthy"
    assert "Service initialization failed" in data["error"]


@patch('src.asr.api.get_transcriber')
@patch('pathlib.Path.unlink')
def test_transcribe_uploaded_audio_cleanup_on_failure(mock_unlink, mock_get_transcriber, client):
    """Test that temporary files are cleaned up when upload transcription fails."""
    mock_transcriber = MagicMock()
    mock_get_transcriber.return_value = mock_transcriber
    mock_transcriber.transcribe_audio.side_effect = Exception("Transcription failed")

    # Create a mock audio file
    audio_content = b"mock audio data"
    files = {"file": ("test.wav", io.BytesIO(audio_content), "audio/wav")}

    response = client.post("/asr/transcribe/audio/upload", files=files)

    assert response.status_code == 500
    # Verify cleanup was attempted
    mock_unlink.assert_called()


@patch('src.asr.api.get_transcriber')
@patch('pathlib.Path.unlink')
def test_transcribe_uploaded_video_cleanup_on_failure(mock_unlink, mock_get_transcriber, client):
    """Test that temporary files are cleaned up when upload video transcription fails."""
    mock_transcriber = MagicMock()
    mock_get_transcriber.return_value = mock_transcriber
    mock_transcriber.transcribe_video.side_effect = Exception("Transcription failed")

    # Create a mock video file
    video_content = b"mock video data"
    files = {"file": ("test.mp4", io.BytesIO(video_content), "video/mp4")}

    response = client.post("/asr/transcribe/video/upload", files=files)

    assert response.status_code == 500
    # Verify cleanup was attempted
    mock_unlink.assert_called()