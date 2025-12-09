"""
Tests for convert_video.py script.
"""
import sys
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from convert_video import main


@patch('convert_video.VideoConverter')
@patch('convert_video.Path')
def test_main_convert_format(mock_path_class, mock_video_converter_class, monkeypatch, capsys):
    """Test main function with format conversion."""
    # Mock Path
    mock_input_path = MagicMock()
    mock_input_path.exists.return_value = True
    mock_input_path.stat.return_value.st_size = 1024 * 1024  # 1MB
    mock_input_path.stem = "test_video"
    mock_input_path.suffix = ".avi"
    mock_path_class.return_value = mock_input_path

    # Mock VideoConverter
    mock_converter = MagicMock()
    mock_video_converter_class.return_value = mock_converter
    mock_converter.convert_video_format.return_value = "converted/test_video.webm"

    monkeypatch.setattr("sys.argv", ["convert_video.py", "input.avi", "--format", "webm"])

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0

    captured = capsys.readouterr()
    assert "Converting to webm format..." in captured.out
    assert "Operation successful" in captured.out
    mock_converter.convert_video_format.assert_called_once()


@patch('convert_video.VideoConverter')
@patch('convert_video.Path')
def test_main_extract_audio(mock_path_class, mock_video_converter_class, monkeypatch, capsys):
    """Test main function with audio extraction."""
    mock_input_path = MagicMock()
    mock_input_path.exists.return_value = True
    mock_input_path.stat.return_value.st_size = 2048 * 1024  # 2MB
    mock_input_path.stem = "test_video"
    mock_input_path.suffix = ".mp4"
    mock_path_class.return_value = mock_input_path

    mock_converter = MagicMock()
    mock_video_converter_class.return_value = mock_converter
    mock_converter.extract_audio_from_video.return_value = "converted/test_video_audio.wav"

    monkeypatch.setattr("sys.argv", ["convert_video.py", "video.mp4", "--action", "extract_audio", "--format", "wav"])

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0

    captured = capsys.readouterr()
    assert "Extracting audio to wav..." in captured.out
    mock_converter.extract_audio_from_video.assert_called_once()


@patch('convert_video.VideoConverter')
@patch('convert_video.Path')
def test_main_compress_video(mock_path_class, mock_video_converter_class, monkeypatch, capsys):
    """Test main function with video compression."""
    mock_input_path = MagicMock()
    mock_input_path.exists.return_value = True
    mock_input_path.stat.return_value.st_size = 10240 * 1024  # 10MB
    mock_input_path.stem = "large_video"
    mock_input_path.suffix = ".mp4"
    mock_path_class.return_value = mock_input_path

    mock_converter = MagicMock()
    mock_video_converter_class.return_value = mock_converter
    mock_converter.compress_video.return_value = "converted/large_video_compressed.mp4"

    monkeypatch.setattr("sys.argv", ["convert_video.py", "large.mp4", "--action", "compress", "--quality", "medium"])

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0

    captured = capsys.readouterr()
    assert "Compressing with medium quality..." in captured.out
    mock_converter.compress_video.assert_called_once()


@patch('convert_video.VideoConverter')
@patch('convert_video.Path')
def test_main_change_resolution(mock_path_class, mock_video_converter_class, monkeypatch, capsys):
    """Test main function with resolution change."""
    mock_input_path = MagicMock()
    mock_input_path.exists.return_value = True
    mock_input_path.stat.return_value.st_size = 5120 * 1024  # 5MB
    mock_input_path.stem = "hd_video"
    mock_input_path.suffix = ".mp4"
    mock_path_class.return_value = mock_input_path

    mock_converter = MagicMock()
    mock_video_converter_class.return_value = mock_converter
    mock_converter.change_resolution.return_value = "converted/hd_video_1280x720.mp4"

    monkeypatch.setattr("sys.argv", ["convert_video.py", "hd.mp4", "--action", "change_resolution", "--resolution", "1280x720"])

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0

    captured = capsys.readouterr()
    assert "Changing resolution to 1280x720..." in captured.out
    mock_converter.change_resolution.assert_called_once()


def test_main_input_file_not_found(monkeypatch, capsys):
    """Test main function with non-existent input file."""
    monkeypatch.setattr("sys.argv", ["convert_video.py", "nonexistent.mp4", "--format", "webm"])

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1

    captured = capsys.readouterr()
    assert "❌ Error: Input file 'nonexistent.mp4' not found" in captured.out


@patch('convert_video.VideoConverter')
@patch('convert_video.Path')
def test_main_missing_resolution_for_change(mock_path_class, mock_video_converter_class, monkeypatch, capsys):
    """Test main function with resolution change but no resolution specified."""
    mock_input_path = MagicMock()
    mock_input_path.exists.return_value = True
    mock_input_path.stat.return_value.st_size = 1024 * 1024
    mock_path_class.return_value = mock_input_path

    monkeypatch.setattr("sys.argv", ["convert_video.py", "video.mp4", "--action", "change_resolution"])

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1

    captured = capsys.readouterr()
    assert "--resolution required for resolution change" in captured.out


@patch('convert_video.VideoConverter')
@patch('convert_video.Path')
def test_main_operation_failure(mock_path_class, mock_video_converter_class, monkeypatch, capsys):
    """Test main function when operation fails."""
    mock_input_path = MagicMock()
    mock_input_path.exists.return_value = True
    mock_input_path.stat.return_value.st_size = 1024 * 1024
    mock_input_path.stem = "test"
    mock_input_path.suffix = ".mp4"
    mock_path_class.return_value = mock_input_path

    mock_converter = MagicMock()
    mock_video_converter_class.return_value = mock_converter
    mock_converter.convert_video_format.return_value = None  # Operation failed

    monkeypatch.setattr("sys.argv", ["convert_video.py", "test.mp4", "--format", "webm"])

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1

    captured = capsys.readouterr()
    assert "❌ Operation failed" in captured.out


@patch('convert_video.VideoConverter')
@patch('convert_video.Path')
def test_main_default_format_conversion(mock_path_class, mock_video_converter_class, monkeypatch):
    """Test main function with default format (webm) when no format specified."""
    mock_input_path = MagicMock()
    mock_input_path.exists.return_value = True
    mock_input_path.stat.return_value.st_size = 1024 * 1024
    mock_input_path.stem = "test"
    mock_input_path.suffix = ".avi"
    mock_path_class.return_value = mock_input_path

    mock_converter = MagicMock()
    mock_video_converter_class.return_value = mock_converter
    mock_converter.convert_video_format.return_value = "converted/test.webm"

    monkeypatch.setattr("sys.argv", ["convert_video.py", "test.avi"])

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0

    # Verify it was called with webm format
    call_args = mock_converter.convert_video_format.call_args
    assert call_args[0][1] == "webm"


@patch('convert_video.VideoConverter')
@patch('convert_video.Path')
def test_main_default_audio_format(mock_path_class, mock_video_converter_class, monkeypatch):
    """Test main function with default audio format (wav) when extracting audio."""
    mock_input_path = MagicMock()
    mock_input_path.exists.return_value = True
    mock_input_path.stat.return_value.st_size = 1024 * 1024
    mock_input_path.stem = "test"
    mock_input_path.suffix = ".mp4"
    mock_path_class.return_value = mock_input_path

    mock_converter = MagicMock()
    mock_video_converter_class.return_value = mock_converter
    mock_converter.extract_audio_from_video.return_value = "converted/test_audio.wav"

    monkeypatch.setattr("sys.argv", ["convert_video.py", "test.mp4", "--action", "extract_audio"])

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0

    # Verify it was called with wav format
    call_args = mock_converter.extract_audio_from_video.call_args
    assert call_args[0][1] == "wav"


@patch('convert_video.VideoConverter')
@patch('convert_video.Path')
def test_main_default_compression_quality(mock_path_class, mock_video_converter_class, monkeypatch):
    """Test main function with default compression quality (medium)."""
    mock_input_path = MagicMock()
    mock_input_path.exists.return_value = True
    mock_input_path.stat.return_value.st_size = 1024 * 1024
    mock_input_path.stem = "test"
    mock_input_path.suffix = ".mp4"
    mock_path_class.return_value = mock_input_path

    mock_converter = MagicMock()
    mock_video_converter_class.return_value = mock_converter
    mock_converter.compress_video.return_value = "converted/test_compressed.mp4"

    monkeypatch.setattr("sys.argv", ["convert_video.py", "test.mp4", "--action", "compress"])

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0

    # Verify it was called with medium quality
    call_args = mock_converter.compress_video.call_args
    assert call_args[0][1] == "medium"