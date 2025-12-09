"""
Tests for src/downloader/api.py downloader endpoints.
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import HTTPException

from src.downloader.api import router, perform_download


@pytest.fixture
def client():
    """Create a test client for the downloader router."""
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestGetFormats:
    """Test get_formats endpoint."""

    @patch('src.downloader.api.GenericDownloader')
    def test_get_formats_success(self, mock_downloader_class, client):
        """Test successful format retrieval."""
        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader
        mock_downloader.get_available_resolutions.return_value = [
            {"format_id": "22", "ext": "mp4", "resolution": "720p", "note": "hd"},
            {"format_id": "18", "ext": "mp4", "resolution": "360p", "note": "medium"}
        ]

        response = client.get("/downloader/formats/https://youtube.com/watch?v=test")

        assert response.status_code == 200
        result = response.json()
        assert "formats" in result
        assert len(result["formats"]) == 2
        assert result["formats"][0]["format_id"] == "22"

    @patch('src.downloader.api.GenericDownloader')
    def test_get_formats_no_formats_found(self, mock_downloader_class, client):
        """Test when no formats are found for URL."""
        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader
        mock_downloader.get_available_resolutions.return_value = []

        response = client.get("/downloader/formats/https://invalid-url.com")

        assert response.status_code == 404
        assert "No formats found" in response.json()["detail"]

    @patch('src.downloader.api.GenericDownloader')
    def test_get_formats_exception(self, mock_downloader_class, client):
        """Test format retrieval when exception occurs."""
        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader
        mock_downloader.get_available_resolutions.side_effect = Exception("Network error")

        response = client.get("/downloader/formats/https://youtube.com/watch?v=test")

        assert response.status_code == 500
        assert "Failed to retrieve formats" in response.json()["detail"]


class TestDownloadVideo:
    """Test download_video endpoint."""

    @patch('src.downloader.api.GenericDownloader')
    @patch('src.downloader.api.perform_download')
    def test_download_video_success(self, mock_perform_download, mock_downloader_class, client):
        """Test successful download initiation."""
        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader

        request_data = {
            "url": "https://youtube.com/watch?v=test",
            "output_dir": "./downloads",
            "audio_only": False
        }

        response = client.post("/downloader/download", json=request_data)

        assert response.status_code == 200
        result = response.json()
        assert result["success"] is True
        assert "Download started in background" in result["message"]
        assert result["output_dir"] == "./downloads"

    @patch('src.downloader.api.GenericDownloader')
    @patch('src.downloader.api.perform_download')
    def test_download_video_with_time_slicing(self, mock_perform_download, mock_downloader_class, client):
        """Test download with time slicing parameters."""
        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader

        request_data = {
            "url": "https://youtube.com/watch?v=test",
            "start_time": "1:30",
            "end_time": "5:45"
        }

        response = client.post("/downloader/download", json=request_data)

        assert response.status_code == 200
        # Verify that perform_download was called with parsed time values
        call_args = mock_perform_download.call_args
        assert call_args[1]["start_time"] == 90  # 1:30 = 90 seconds
        assert call_args[1]["end_time"] == 345  # 5:45 = 345 seconds

    @patch('src.downloader.api.GenericDownloader')
    @patch('src.downloader.api.perform_download')
    def test_download_video_audio_only(self, mock_perform_download, mock_downloader_class, client):
        """Test download with audio_only flag."""
        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader

        request_data = {
            "url": "https://youtube.com/watch?v=test",
            "audio_only": True
        }

        response = client.post("/downloader/download", json=request_data)

        assert response.status_code == 200
        call_args = mock_perform_download.call_args
        assert call_args[1]["audio_only"] is True

    @patch('src.downloader.api.GenericDownloader')
    @patch('src.downloader.api.perform_download')
    def test_download_video_with_format_id(self, mock_perform_download, mock_downloader_class, client):
        """Test download with specific format ID."""
        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader

        request_data = {
            "url": "https://youtube.com/watch?v=test",
            "format_id": "22"
        }

        response = client.post("/downloader/download", json=request_data)

        assert response.status_code == 200
        call_args = mock_perform_download.call_args
        assert call_args[1]["format_id"] == "22"

    def test_download_video_invalid_time_range(self, client):
        """Test download with invalid time range (start > end)."""
        request_data = {
            "url": "https://youtube.com/watch?v=test",
            "start_time": "5:45",
            "end_time": "1:30"
        }

        response = client.post("/downloader/download", json=request_data)

        assert response.status_code == 400
        assert "Invalid request parameters" in response.json()["detail"]

    @patch('src.downloader.api.GenericDownloader')
    def test_download_video_downloader_exception(self, mock_downloader_class, client):
        """Test download when GenericDownloader initialization fails."""
        mock_downloader_class.side_effect = Exception("Downloader init failed")

        request_data = {
            "url": "https://youtube.com/watch?v=test"
        }

        response = client.post("/downloader/download", json=request_data)

        assert response.status_code == 500
        assert "Failed to start download" in response.json()["detail"]

    def test_download_video_invalid_time_format(self, client):
        """Test download with invalid time format."""
        request_data = {
            "url": "https://youtube.com/watch?v=test",
            "start_time": "invalid-time"
        }

        response = client.post("/downloader/download", json=request_data)

        assert response.status_code == 400
        assert "Invalid request parameters" in response.json()["detail"]


class TestPerformDownload:
    """Test perform_download function."""

    @patch('src.downloader.api.logger')
    def test_perform_download_success(self, mock_logger):
        """Test successful background download."""
        mock_downloader = MagicMock()
        mock_result = {
            "output_dir": "/downloads",
            "platform": "YouTube"
        }
        mock_downloader.download.return_value = mock_result

        # Run the async function
        import asyncio
        asyncio.run(perform_download(
            downloader=mock_downloader,
            url="https://youtube.com/watch?v=test",
            start_time=None,
            end_time=None,
            audio_only=False,
            format_id=None
        ))

        # Verify download was called
        mock_downloader.__enter__.assert_called_once()
        mock_downloader.download.assert_called_once_with(
            url="https://youtube.com/watch?v=test",
            start_time=None,
            end_time=None,
            audio_only=False,
            format_id=None
        )
        mock_downloader.__exit__.assert_called_once()

        # Verify success logging
        mock_logger.info.assert_called()

    @patch('src.downloader.api.logger')
    def test_perform_download_failure(self, mock_logger):
        """Test background download failure."""
        mock_downloader = MagicMock()
        mock_downloader.download.side_effect = Exception("Download failed")

        # Run the async function
        import asyncio
        asyncio.run(perform_download(
            downloader=mock_downloader,
            url="https://youtube.com/watch?v=test",
            start_time=10,
            end_time=60,
            audio_only=True,
            format_id="22"
        ))

        # Verify error logging
        mock_logger.error.assert_called_with("❌ Download failed for https://youtube.com/watch?v=test: Download failed")


class TestDownloadRequest:
    """Test DownloadRequest model."""

    def test_download_request_creation(self):
        """Test creating a DownloadRequest instance."""
        from src.downloader.api import DownloadRequest

        request = DownloadRequest(
            url="https://youtube.com/watch?v=test",
            output_dir="/downloads",
            start_time="1:30",
            end_time="5:45",
            audio_only=True,
            format_id="22"
        )

        assert request.url == "https://youtube.com/watch?v=test"
        assert request.output_dir == "/downloads"
        assert request.start_time == "1:30"
        assert request.end_time == "5:45"
        assert request.audio_only is True
        assert request.format_id == "22"

    def test_download_request_defaults(self):
        """Test DownloadRequest with default values."""
        from src.downloader.api import DownloadRequest

        request = DownloadRequest(url="https://youtube.com/watch?v=test")

        assert request.url == "https://youtube.com/watch?v=test"
        assert request.output_dir == "./downloads"
        assert request.start_time is None
        assert request.end_time is None
        assert request.audio_only is False
        assert request.format_id is None


class TestFormatResponse:
    """Test FormatResponse model."""

    def test_format_response_creation(self):
        """Test creating a FormatResponse instance."""
        from src.downloader.api import FormatResponse

        response = FormatResponse(
            format_id="22",
            ext="mp4",
            resolution="720p",
            note="hd"
        )

        assert response.format_id == "22"
        assert response.ext == "mp4"
        assert response.resolution == "720p"
        assert response.note == "hd"


class TestDownloadResponse:
    """Test DownloadResponse model."""

    def test_download_response_creation(self):
        """Test creating a DownloadResponse instance."""
        from src.downloader.api import DownloadResponse

        response = DownloadResponse(
            success=True,
            message="Download started",
            output_dir="/downloads",
            platform="YouTube",
            platform_info={"title": "Test Video"}
        )

        assert response.success is True
        assert response.message == "Download started"
        assert response.output_dir == "/downloads"
        assert response.platform == "YouTube"
        assert response.platform_info == {"title": "Test Video"}

    def test_download_response_optional_fields(self):
        """Test DownloadResponse with optional fields as None."""
        from src.downloader.api import DownloadResponse

        response = DownloadResponse(
            success=False,
            message="Download failed"
        )

        assert response.success is False
        assert response.message == "Download failed"
        assert response.output_dir is None
        assert response.platform is None
        assert response.platform_info is None