import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.downloader.generic import GenericDownloader
import yt_dlp


@pytest.fixture
def generic_downloader(tmp_path):
    downloader = GenericDownloader(output_dir=str(tmp_path))
    yield downloader
    downloader.cleanup()


class TestGenericDownloader:
    """Test suite for GenericDownloader class."""

    def test_init(self, generic_downloader, tmp_path):
        assert generic_downloader.output_dir == tmp_path
        assert generic_downloader.output_dir.exists()
        assert generic_downloader.platform_name == "Generic"
        assert generic_downloader.detected_platform is None

    def test_validate_url_valid(self, generic_downloader):
        valid_urls = [
            "https://www.example.com/video",
            "http://example.com/watch?v=123",
            "https://vimeo.com/123456789",
            "https://dailymotion.com/video/x123abc",
        ]
        for url in valid_urls:
            assert generic_downloader.validate_url(url) is True

    def test_validate_url_invalid(self, generic_downloader):
        invalid_urls = [
            "not a url", "ftp://example.com/video", "", "javascript:alert('x')"
        ]
        for url in invalid_urls:
            assert generic_downloader.validate_url(url) is False

    @patch("src.downloader.generic.yt_dlp.YoutubeDL")
    def test_get_platform_info_success(self, mock_ydl_class,
                                       generic_downloader):
        mock_ydl = MagicMock()
        mock_ydl.extract_info.return_value = {
            "extractor_key": "Youtube",
            "extractor": "youtube",
            "title": "Test Video",
            "duration": 120,
            "uploader": "Test Channel",
        }
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl

        info = generic_downloader.get_platform_info(
            "https://www.youtube.com/watch?v=test")
        assert info["platform"] == "Youtube"
        assert info["platform_name"] == "youtube"
        assert info["title"] == "Test Video"

    @patch("src.downloader.generic.yt_dlp.YoutubeDL")
    def test_get_platform_info_failure(self, mock_ydl_class,
                                       generic_downloader):
        mock_ydl = MagicMock()
        mock_ydl.extract_info.side_effect = Exception("Extraction failed")
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl

        info = generic_downloader.get_platform_info(
            "https://example.com/video")
        assert info["platform"] == "Unknown"
        assert info["title"] == "Unknown"

    @patch("src.downloader.generic.yt_dlp.YoutubeDL")
    def test_get_available_resolutions(self, mock_ydl_class,
                                       generic_downloader):
        mock_ydl = MagicMock()
        mock_ydl.extract_info.return_value = {
            "formats": [
                {
                    "format_id": "18",
                    "ext": "mp4",
                    "height": 360,
                    "format_note": "medium"
                },
                {
                    "format_id": "22",
                    "ext": "mp4",
                    "height": 720,
                    "format_note": "hd"
                },
            ]
        }
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl

        resolutions = generic_downloader.get_available_resolutions(
            "https://youtube.com/watch?v=abc")
        assert len(resolutions) == 2
        assert resolutions[0]["resolution"] == "360p"
        assert resolutions[1]["resolution"] == "720p"

    @patch("src.downloader.generic.yt_dlp.YoutubeDL")
    def test_download_success(self, mock_ydl_class, generic_downloader,
                              tmp_path):
        mock_info = MagicMock()
        mock_info.extract_info.return_value = {
            "extractor_key": "Youtube",
            "extractor": "youtube",
            "title": "Test Video",
            "duration": 120,
            "uploader": "Test Channel",
        }
        mock_download = MagicMock()
        mock_download.download.return_value = None
        mock_ydl_class.return_value.__enter__.side_effect = [
            mock_info, mock_download
        ]

        result = generic_downloader.download(
            "https://www.youtube.com/watch?v=test")
        assert result["success"] is True
        assert result["platform"] == "Youtube"
        assert result["platform_info"]["title"] == "Test Video"

    @patch("src.downloader.generic.yt_dlp.YoutubeDL")
    def test_download_audio_only(self, mock_ydl_class, generic_downloader):
        mock_info = MagicMock()
        mock_info.extract_info.return_value = {
            "extractor_key": "Vimeo",
            "extractor": "vimeo",
            "title": "Test",
            "duration": 60,
            "uploader": "User"
        }
        mock_download = MagicMock()
        mock_ydl_class.return_value.__enter__.side_effect = [
            mock_info, mock_download
        ]

        result = generic_downloader.download("https://vimeo.com/123",
                                             audio_only=True)
        download_args = mock_ydl_class.call_args_list[1][0][0]
        assert download_args["format"] == "bestaudio/best"
        assert "postprocessors" in download_args

    @patch("src.downloader.generic.yt_dlp.YoutubeDL")
    def test_download_with_time_slice(self, mock_ydl_class,
                                      generic_downloader):
        mock_info = MagicMock()
        mock_info.extract_info.return_value = {
            "extractor_key": "Dailymotion",
            "extractor": "dailymotion",
            "title": "Test",
            "duration": 180,
            "uploader": "User"
        }
        mock_download = MagicMock()
        mock_ydl_class.return_value.__enter__.side_effect = [
            mock_info, mock_download
        ]

        result = generic_downloader.download(
            "https://dailymotion.com/video/x123", start_time=10, end_time=30)
        download_args = mock_ydl_class.call_args_list[1][0][0]
        assert "-ss" in download_args["postprocessor_args"]
        assert "10" in download_args["postprocessor_args"]
        assert "-to" in download_args["postprocessor_args"]
        assert "30" in download_args["postprocessor_args"]

    def test_download_invalid_url(self, generic_downloader):
        with pytest.raises(ValueError):
            generic_downloader.download("invalid_url")

    @patch("src.downloader.generic.yt_dlp.YoutubeDL")
    def test_download_raises_yt_dlp_error(self, mock_ydl_class,
                                          generic_downloader):
        mock_info = MagicMock()
        mock_info.extract_info.return_value = {
            "extractor_key": "Test",
            "extractor": "test",
            "title": "Test",
            "duration": 60,
            "uploader": "User"
        }
        mock_download = MagicMock()
        mock_download.download.side_effect = yt_dlp.utils.DownloadError(
            "Failed")
        mock_ydl_class.return_value.__enter__.side_effect = [
            mock_info, mock_download
        ]

        with pytest.raises(yt_dlp.utils.DownloadError):
            generic_downloader.download("https://example.com/video")

    def test_context_manager_calls_cleanup(self, tmp_path):
        with GenericDownloader(output_dir=str(tmp_path)) as dl:
            assert dl.output_dir == tmp_path
        assert dl.pbar is None

    @patch("src.downloader.generic.yt_dlp.YoutubeDL")
    def test_detected_platform_set_after_download(self, mock_ydl_class,
                                                  generic_downloader):
        mock_info = MagicMock()
        mock_info.extract_info.return_value = {
            "extractor_key": "Instagram",
            "extractor": "instagram",
            "title": "Reel",
            "duration": 30,
            "uploader": "User"
        }
        mock_download = MagicMock()
        mock_ydl_class.return_value.__enter__.side_effect = [
            mock_info, mock_download
        ]

        assert generic_downloader.detected_platform is None
        generic_downloader.download("https://www.instagram.com/reel/abc")
        assert generic_downloader.detected_platform == "Instagram"
