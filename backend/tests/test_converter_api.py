"""
Tests for src/converter/api.py converter endpoints.
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
from pathlib import Path
import io

from src.converter.api import router, audio_converter, video_converter


@pytest.fixture
def client():
    """Create a test client for the converter router."""
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestConvertAudio:
    """Test convert_audio endpoint."""

    @patch('src.converter.api.audio_converter')
    def test_convert_audio_success(self, mock_audio_converter, client):
        """Test successful audio conversion."""
        mock_audio_converter.convert_audio_format.return_value = "converted/test.wav"

        # Create mock audio file
        audio_content = b"mock audio data"
        files = {"file": ("test.mp3", io.BytesIO(audio_content), "audio/mp3")}
        data = {"output_format": "wav", "bitrate": "192k", "sample_rate": "44100"}

        response = client.post("/converter/convert/audio", files=files, data=data)

        assert response.status_code == 200
        result = response.json()
        assert result["success"] is True
        assert result["output_file"] == "converted/test.wav"
        assert result["conversion_type"] == "audio_format"

    def test_convert_audio_no_file(self, client):
        """Test audio conversion with no file provided."""
        data = {"output_format": "wav"}

        response = client.post("/converter/convert/audio", data=data)

        assert response.status_code == 422
        assert "Field required" in response.json()["detail"][0]["msg"]

    @patch('src.converter.api.audio_converter')
    def test_convert_audio_conversion_failure(self, mock_audio_converter, client):
        """Test audio conversion when conversion fails."""
        mock_audio_converter.convert_audio_format.return_value = None

        audio_content = b"mock audio data"
        files = {"file": ("test.mp3", io.BytesIO(audio_content), "audio/mp3")}
        data = {"output_format": "wav"}

        response = client.post("/converter/convert/audio", files=files, data=data)

        assert response.status_code == 500
        assert "Audio conversion failed" in response.json()["detail"]

    @patch('src.converter.api.audio_converter')
    def test_convert_audio_exception(self, mock_audio_converter, client):
        """Test audio conversion when exception occurs."""
        mock_audio_converter.convert_audio_format.side_effect = Exception("FFmpeg error")

        audio_content = b"mock audio data"
        files = {"file": ("test.mp3", io.BytesIO(audio_content), "audio/mp3")}
        data = {"output_format": "wav"}

        response = client.post("/converter/convert/audio", files=files, data=data)

        assert response.status_code == 500
        assert "Conversion failed" in response.json()["detail"]


class TestConvertVideo:
    """Test convert_video endpoint."""

    @patch('src.converter.api.video_converter')
    def test_convert_video_success(self, mock_video_converter, client):
        """Test successful video conversion."""
        mock_video_converter.convert_video_format.return_value = "converted/test.mp4"

        video_content = b"mock video data"
        files = {"file": ("test.avi", io.BytesIO(video_content), "video/avi")}
        data = {
            "output_format": "mp4",
            "resolution": "1920x1080",
            "quality": "high",
            "video_bitrate": "5000k",
            "audio_bitrate": "256k"
        }

        response = client.post("/converter/convert/video", files=files, data=data)

        assert response.status_code == 200
        result = response.json()
        assert result["success"] is True
        assert result["output_file"] == "converted/test.mp4"
        assert result["conversion_type"] == "video_format"

    def test_convert_video_no_file(self, client):
        """Test video conversion with no file provided."""
        data = {"output_format": "mp4"}

        response = client.post("/converter/convert/video", data=data)

        assert response.status_code == 422
        assert "Field required" in response.json()["detail"][0]["msg"]

    @patch('src.converter.api.video_converter')
    def test_convert_video_conversion_failure(self, mock_video_converter, client):
        """Test video conversion when conversion fails."""
        mock_video_converter.convert_video_format.return_value = None

        video_content = b"mock video data"
        files = {"file": ("test.avi", io.BytesIO(video_content), "video/avi")}
        data = {"output_format": "mp4"}

        response = client.post("/converter/convert/video", files=files, data=data)

        assert response.status_code == 500
        assert "Video conversion failed" in response.json()["detail"]


class TestExtractAudioFromVideo:
    """Test extract_audio_from_video endpoint."""

    @patch('src.converter.api.video_converter')
    def test_extract_audio_success(self, mock_video_converter, client):
        """Test successful audio extraction from video."""
        mock_video_converter.extract_audio_from_video.return_value = "converted/test_audio.mp3"

        video_content = b"mock video data"
        files = {"file": ("test.mp4", io.BytesIO(video_content), "video/mp4")}
        data = {"audio_format": "mp3"}

        response = client.post("/converter/convert/audio/extract", files=files, data=data)

        assert response.status_code == 200
        result = response.json()
        assert result["success"] is True
        assert result["output_file"] == "converted/test_audio.mp3"
        assert result["conversion_type"] == "audio_extraction"

    def test_extract_audio_no_file(self, client):
        """Test audio extraction with no file provided."""
        data = {"audio_format": "wav"}

        response = client.post("/converter/convert/audio/extract", data=data)

        assert response.status_code == 422
        assert "Field required" in response.json()["detail"][0]["msg"]

    @patch('src.converter.api.video_converter')
    def test_extract_audio_failure(self, mock_video_converter, client):
        """Test audio extraction when extraction fails."""
        mock_video_converter.extract_audio_from_video.return_value = None

        video_content = b"mock video data"
        files = {"file": ("test.mp4", io.BytesIO(video_content), "video/mp4")}
        data = {"audio_format": "mp3"}

        response = client.post("/converter/convert/audio/extract", files=files, data=data)

        assert response.status_code == 500
        assert "Audio extraction failed" in response.json()["detail"]


class TestCompressVideo:
    """Test compress_video endpoint."""

    @patch('src.converter.api.video_converter')
    def test_compress_video_success(self, mock_video_converter, client):
        """Test successful video compression."""
        mock_video_converter.compress_video.return_value = "converted/test_compressed.mp4"

        video_content = b"mock video data"
        files = {"file": ("test.mp4", io.BytesIO(video_content), "video/mp4")}
        data = {"quality": "medium"}

        response = client.post("/converter/convert/video/compress", files=files, data=data)

        assert response.status_code == 200
        result = response.json()
        assert result["success"] is True
        assert result["output_file"] == "converted/test_compressed.mp4"
        assert result["conversion_type"] == "video_compression"
        assert "medium quality" in result["message"]

    def test_compress_video_no_file(self, client):
        """Test video compression with no file provided."""
        data = {"quality": "low"}

        response = client.post("/converter/convert/video/compress", data=data)

        assert response.status_code == 422
        assert "Field required" in response.json()["detail"][0]["msg"]

    @patch('src.converter.api.video_converter')
    def test_compress_video_failure(self, mock_video_converter, client):
        """Test video compression when compression fails."""
        mock_video_converter.compress_video.return_value = None

        video_content = b"mock video data"
        files = {"file": ("test.mp4", io.BytesIO(video_content), "video/mp4")}
        data = {"quality": "high"}

        response = client.post("/converter/convert/video/compress", files=files, data=data)

        assert response.status_code == 500
        assert "Video compression failed" in response.json()["detail"]


class TestGetAudioInfo:
    """Test get_audio_info endpoint."""

    @patch('src.converter.api.audio_converter')
    def test_get_audio_info_success(self, mock_audio_converter, client):
        """Test successful audio info retrieval."""
        mock_info = {"duration": 120.5, "bitrate": 192000, "sample_rate": 44100}
        mock_audio_converter.get_audio_info.return_value = mock_info

        response = client.get("/converter/info/audio/path/to/audio.mp3")

        assert response.status_code == 200
        result = response.json()
        assert result["file_info"] == mock_info

    @patch('src.converter.api.audio_converter')
    def test_get_audio_info_not_found(self, mock_audio_converter, client):
        """Test audio info retrieval when file info cannot be read."""
        mock_audio_converter.get_audio_info.return_value = None

        response = client.get("/converter/info/audio/nonexistent.mp3")

        assert response.status_code == 404
        assert "Could not read audio file information" in response.json()["detail"]

    @patch('src.converter.api.audio_converter')
    def test_get_audio_info_exception(self, mock_audio_converter, client):
        """Test audio info retrieval when exception occurs."""
        mock_audio_converter.get_audio_info.side_effect = Exception("FFprobe error")

        response = client.get("/converter/info/audio/test.mp3")

        assert response.status_code == 500
        assert "Failed to get audio info" in response.json()["detail"]


class TestGetVideoInfo:
    """Test get_video_info endpoint."""

    @patch('src.converter.api.video_converter')
    def test_get_video_info_success(self, mock_video_converter, client):
        """Test successful video info retrieval."""
        mock_info = {
            "duration": 300.0,
            "width": 1920,
            "height": 1080,
            "bitrate": 5000000,
            "codec": "h264"
        }
        mock_video_converter.get_video_info.return_value = mock_info

        response = client.get("/converter/info/video/path/to/video.mp4")

        assert response.status_code == 200
        result = response.json()
        assert result["file_info"] == mock_info

    @patch('src.converter.api.video_converter')
    def test_get_video_info_not_found(self, mock_video_converter, client):
        """Test video info retrieval when file info cannot be read."""
        mock_video_converter.get_video_info.return_value = None

        response = client.get("/converter/info/video/nonexistent.mp4")

        assert response.status_code == 404
        assert "Could not read video file information" in response.json()["detail"]

    @patch('src.converter.api.video_converter')
    def test_get_video_info_exception(self, mock_video_converter, client):
        """Test video info retrieval when exception occurs."""
        mock_video_converter.get_video_info.side_effect = Exception("FFprobe error")

        response = client.get("/converter/info/video/test.mp4")

        assert response.status_code == 500
        assert "Failed to get video info" in response.json()["detail"]


class TestConversionResponse:
    """Test ConversionResponse model."""

    def test_conversion_response_creation(self):
        """Test creating a ConversionResponse instance."""
        from src.converter.api import ConversionResponse

        response = ConversionResponse(
            success=True,
            message="Conversion successful",
            output_file="output.wav",
            input_file="input.mp3",
            conversion_type="audio_format"
        )

        assert response.success is True
        assert response.message == "Conversion successful"
        assert response.output_file == "output.wav"
        assert response.input_file == "input.mp3"
        assert response.conversion_type == "audio_format"

    def test_conversion_response_optional_fields(self):
        """Test ConversionResponse with optional fields as None."""
        from src.converter.api import ConversionResponse

        response = ConversionResponse(
            success=False,
            message="Conversion failed"
        )

        assert response.success is False
        assert response.message == "Conversion failed"
        assert response.output_file is None
        assert response.input_file is None
        assert response.conversion_type is None


class TestAudioConversionRequest:
    """Test AudioConversionRequest model."""

    def test_audio_conversion_request_creation(self):
        """Test creating an AudioConversionRequest instance."""
        from src.converter.api import AudioConversionRequest

        request = AudioConversionRequest(
            input_format="mp3",
            output_format="wav",
            bitrate="256k",
            sample_rate=48000
        )

        assert request.input_format == "mp3"
        assert request.output_format == "wav"
        assert request.bitrate == "256k"
        assert request.sample_rate == 48000

    def test_audio_conversion_request_defaults(self):
        """Test AudioConversionRequest with default values."""
        from src.converter.api import AudioConversionRequest

        request = AudioConversionRequest(
            input_format="wav",
            output_format="mp3"
        )

        assert request.input_format == "wav"
        assert request.output_format == "mp3"
        assert request.bitrate == "192k"
        assert request.sample_rate == 44100


class TestVideoConversionRequest:
    """Test VideoConversionRequest model."""

    def test_video_conversion_request_creation(self):
        """Test creating a VideoConversionRequest instance."""
        from src.converter.api import VideoConversionRequest

        request = VideoConversionRequest(
            input_format="avi",
            output_format="mp4",
            resolution="1920x1080",
            quality="high",
            video_bitrate="8000k",
            audio_bitrate="256k"
        )

        assert request.input_format == "avi"
        assert request.output_format == "mp4"
        assert request.resolution == "1920x1080"
        assert request.quality == "high"
        assert request.video_bitrate == "8000k"
        assert request.audio_bitrate == "256k"

    def test_video_conversion_request_defaults(self):
        """Test VideoConversionRequest with default values."""
        from src.converter.api import VideoConversionRequest

        request = VideoConversionRequest(
            input_format="mp4",
            output_format="webm"
        )

        assert request.input_format == "mp4"
        assert request.output_format == "webm"
        assert request.resolution is None
        assert request.quality == "medium"
        assert request.video_bitrate is None
        assert request.audio_bitrate == "128k"