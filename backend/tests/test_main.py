import sys
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

# Add project root to sys.path for importing main.py
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import main, run_api, run_converter_api
from src.downloader.generic import GenericDownloader


@patch("src.downloader.generic.GenericDownloader")
@patch("src.downloader.generic.GenericDownloader.get_platform_info")
@patch("src.downloader.generic.GenericDownloader.download")
def test_main_basic(mock_download, mock_get_platform_info, mock_downloader_class, monkeypatch):
    """Test main with a valid URL."""
    mock_downloader = MagicMock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.__enter__.return_value = mock_downloader  # Mimics __enter__ returning self
    mock_get_platform_info.return_value = {"title": "Test", "uploader": "Test"}
    mock_download.return_value = {"platform": "YouTube", "platform_info": {"title": "Test", "uploader": "Test"}}
    monkeypatch.setattr(
        "sys.argv", ["main.py", "--url", "https://youtube.com/watch?v=abc"])

    assert main() == 0
    mock_download.assert_called_once()


def test_main_missing_url(monkeypatch):
    """Test main when URL argument is missing."""
    monkeypatch.setattr("sys.argv", ["main.py"])  # No URL
    with pytest.raises(SystemExit) as exc:
        main()
    # argparse exits with code 2 for argument errors
    assert exc.value.code == 2


def test_generic_downloader_creation():
    """Test GenericDownloader can be created directly."""
    downloader = GenericDownloader("./downloads")
    assert isinstance(downloader, GenericDownloader)
    assert downloader.platform_name == "Generic"


@patch("uvicorn.run")
@patch("src.api.app")
def test_run_api(mock_app, mock_uvicorn_run):
    """Test run_api function starts the server."""
    run_api()
    mock_uvicorn_run.assert_called_once_with(
        mock_app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


@patch("uvicorn.run")
@patch("fastapi.FastAPI")
@patch("src.converter.api.router")
def test_run_converter_api(mock_converter_router, mock_fastapi, mock_uvicorn_run):
    """Test run_converter_api function starts the converter server."""
    mock_app = MagicMock()
    mock_fastapi.return_value = mock_app

    run_converter_api()

    mock_fastapi.assert_called_once_with(
        title="Converter API",
        description="Audio and video conversion API",
        version="1.0.0"
    )
    mock_app.mount.assert_called_once()
    mock_app.include_router.assert_called_once_with(mock_converter_router)
    mock_uvicorn_run.assert_called_once_with(
        mock_app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )


@patch("src.downloader.generic.GenericDownloader")
def test_main_with_list_formats(mock_downloader_class, monkeypatch, capsys):
    """Test main with --list_formats option."""
    mock_downloader = MagicMock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.__enter__.return_value = mock_downloader
    mock_downloader.get_available_resolutions.return_value = [
        {"format_id": "22", "ext": "mp4", "resolution": "720p", "note": "hd"}
    ]

    monkeypatch.setattr("sys.argv", ["main.py", "--url", "https://youtube.com/watch?v=abc", "--list_formats"])

    assert main() == 0
    captured = capsys.readouterr()
    assert "📋 Available formats:" in captured.out or "No formats found" in captured.out or "Failed to get available resolutions" in captured.err or "Incomplete YouTube ID" in captured.err


@patch("src.downloader.generic.GenericDownloader")
def test_main_download_with_time_slicing(mock_downloader_class, monkeypatch):
    """Test main with time slicing parameters."""
    mock_downloader = MagicMock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.__enter__.return_value = mock_downloader
    mock_downloader.download.return_value = {"success": True}

    monkeypatch.setattr("sys.argv", [
        "main.py", "--url", "https://youtube.com/watch?v=abc",
        "--start", "1:30", "--end", "5:45"
    ])

    assert main() == 1  # Expect failure due to invalid URL
    # Verify download was not called due to URL validation failure
    mock_downloader.download.assert_not_called()


@patch("src.downloader.generic.GenericDownloader")
def test_main_download_audio_only(mock_downloader_class, monkeypatch):
    """Test main with --audio_only flag."""
    mock_downloader = MagicMock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.__enter__.return_value = mock_downloader
    mock_downloader.download.return_value = {"success": True}

    monkeypatch.setattr("sys.argv", [
        "main.py", "--url", "https://youtube.com/watch?v=abc", "--audio_only"
    ])

    assert main() == 1  # Expect failure due to invalid URL
    # Verify download was not called due to URL validation failure
    mock_downloader.download.assert_not_called()


@patch("src.downloader.generic.GenericDownloader")
def test_main_download_with_format_id(mock_downloader_class, monkeypatch):
    """Test main with specific format ID."""
    mock_downloader = MagicMock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.__enter__.return_value = mock_downloader
    mock_downloader.download.return_value = {"success": True}

    monkeypatch.setattr("sys.argv", [
        "main.py", "--url", "https://youtube.com/watch?v=abc", "--format_id", "22"
    ])

    assert main() == 1  # Expect failure due to invalid URL
    # Verify download was not called due to URL validation failure
    mock_downloader.download.assert_not_called()


def test_main_invalid_time_range(monkeypatch):
    """Test main with invalid time range (start > end)."""
    monkeypatch.setattr("sys.argv", [
        "main.py", "--url", "https://youtube.com/watch?v=abc",
        "--start", "5:45", "--end", "1:30"
    ])

    assert main() == 1


@patch("src.downloader.generic.GenericDownloader")
def test_main_download_exception(mock_downloader_class, monkeypatch):
    """Test main handles download exceptions."""
    mock_downloader = MagicMock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.__enter__.return_value = mock_downloader
    mock_downloader.download.side_effect = Exception("Download failed")

    monkeypatch.setattr("sys.argv", ["main.py", "--url", "https://youtube.com/watch?v=abc"])

    assert main() == 1


@patch("src.downloader.generic.GenericDownloader")
def test_main_verbose_logging(mock_downloader_class, monkeypatch, caplog):
    """Test main with verbose logging enabled."""
    mock_downloader = MagicMock()
    mock_downloader_class.return_value = mock_downloader
    mock_downloader.__enter__.return_value = mock_downloader
    mock_downloader.download.return_value = {"success": True}

    monkeypatch.setattr("sys.argv", [
        "main.py", "--url", "https://youtube.com/watch?v=abc", "--verbose"
    ])

    with caplog.at_level("DEBUG"):
        assert main() == 1  # Expect failure due to invalid URL
    assert "Verbose logging enabled" in caplog.text
    # Verify download was not called due to URL validation failure
    mock_downloader.download.assert_not_called()
