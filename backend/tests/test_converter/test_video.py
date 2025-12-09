"""
Tests for video converter functionality.
"""
import pytest
import tempfile
import os
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.converter.video import VideoConverter


@pytest.fixture
def video_converter(tmp_path):
    """Create a VideoConverter instance with temporary directory."""
    converter = VideoConverter(output_dir=str(tmp_path / "converted"))
    yield converter
    # Cleanup is handled by tmp_path fixture


class TestVideoConverter:
    """Test suite for VideoConverter class."""

    def test_initialization(self, tmp_path):
        """Test VideoConverter initialization."""
        output_dir = tmp_path / "test_output"
        converter = VideoConverter(output_dir=str(output_dir))

        assert converter.output_dir == output_dir
        assert output_dir.exists()

    def test_initialization_default_dir(self):
        """Test VideoConverter with default output directory."""
        converter = VideoConverter()
        assert converter.output_dir == Path("./converted")

    @patch('subprocess.run')
    def test_run_ffmpeg_success(self, mock_subprocess, video_converter):
        """Test successful FFmpeg execution."""
        mock_subprocess.return_value = MagicMock(returncode=0)

        result = video_converter._run_ffmpeg("input.mp4", "output.webm", [])
        assert result is True
        mock_subprocess.assert_called_once()

    @patch('subprocess.run')
    def test_run_ffmpeg_failure(self, mock_subprocess, video_converter):
        """Test FFmpeg execution failure."""
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'ffmpeg', stderr="FFmpeg failed")

        result = video_converter._run_ffmpeg("input.mp4", "output.webm", [])
        assert result is False

    def test_convert_video_format_file_not_exists(self, video_converter):
        """Test video format conversion with non-existent file."""
        result = video_converter.convert_video_format("nonexistent.mp4", "webm")
        assert result is None

    @patch('src.converter.video.VideoConverter._run_ffmpeg')
    def test_convert_video_format_mp4(self, mock_run_ffmpeg, video_converter, tmp_path):
        """Test video format conversion to MP4."""
        input_file = tmp_path / "test.avi"
        input_file.write_text("dummy video content")

        mock_run_ffmpeg.return_value = True

        result = video_converter.convert_video_format(str(input_file), "mp4")

        assert result is not None
        assert result.endswith(".mp4")
        args = mock_run_ffmpeg.call_args[0][2]
        assert "-c:v" in args
        assert "libx264" in args

    @patch('src.converter.video.VideoConverter._run_ffmpeg')
    def test_convert_video_format_webm(self, mock_run_ffmpeg, video_converter, tmp_path):
        """Test video format conversion to WebM."""
        input_file = tmp_path / "test.mp4"
        input_file.write_text("dummy video content")

        mock_run_ffmpeg.return_value = True

        result = video_converter.convert_video_format(str(input_file), "webm")

        assert result is not None
        assert result.endswith(".webm")
        args = mock_run_ffmpeg.call_args[0][2]
        assert "-c:v" in args
        assert "libvpx-vp9" in args

    def test_change_resolution_file_not_exists(self, video_converter):
        """Test resolution change with non-existent file."""
        result = video_converter.change_resolution("nonexistent.mp4", "1920x1080")
        assert result is None

    @patch('src.converter.video.VideoConverter._run_ffmpeg')
    def test_change_resolution_success(self, mock_run_ffmpeg, video_converter, tmp_path):
        """Test successful resolution change."""
        input_file = tmp_path / "test.mp4"
        input_file.write_text("dummy video content")

        mock_run_ffmpeg.return_value = True

        result = video_converter.change_resolution(str(input_file), "1280x720")

        assert result is not None
        assert "1280x720" in result
        args = mock_run_ffmpeg.call_args[0][2]
        assert "-vf" in args
        assert "scale=1280x720" in args

    def test_extract_audio_from_video_file_not_exists(self, video_converter):
        """Test audio extraction with non-existent file."""
        result = video_converter.extract_audio_from_video("nonexistent.mp4")
        assert result is None

    @patch('src.converter.video.VideoConverter._run_ffmpeg')
    def test_extract_audio_mp3(self, mock_run_ffmpeg, video_converter, tmp_path):
        """Test audio extraction to MP3."""
        input_file = tmp_path / "test.mp4"
        input_file.write_text("dummy video content")

        mock_run_ffmpeg.return_value = True

        result = video_converter.extract_audio_from_video(str(input_file), "mp3")

        assert result is not None
        assert result.endswith("_audio.mp3")
        args = mock_run_ffmpeg.call_args[0][2]
        assert "-vn" in args
        assert "libmp3lame" in args

    @patch('src.converter.video.VideoConverter._run_ffmpeg')
    def test_extract_audio_wav(self, mock_run_ffmpeg, video_converter, tmp_path):
        """Test audio extraction to WAV."""
        input_file = tmp_path / "test.mp4"
        input_file.write_text("dummy video content")

        mock_run_ffmpeg.return_value = True

        result = video_converter.extract_audio_from_video(str(input_file), "wav")

        assert result is not None
        assert result.endswith("_audio.wav")
        args = mock_run_ffmpeg.call_args[0][2]
        assert "-vn" in args
        assert "pcm_s16le" in args

    def test_compress_video_file_not_exists(self, video_converter):
        """Test video compression with non-existent file."""
        result = video_converter.compress_video("nonexistent.mp4")
        assert result is None

    @patch('src.converter.video.VideoConverter._run_ffmpeg')
    def test_compress_video_high_quality(self, mock_run_ffmpeg, video_converter, tmp_path):
        """Test video compression with high quality."""
        input_file = tmp_path / "test.mp4"
        input_file.write_text("dummy video content")

        mock_run_ffmpeg.return_value = True

        result = video_converter.compress_video(str(input_file), quality="high")

        assert result is not None
        assert result.endswith("_compressed.mp4")
        args = mock_run_ffmpeg.call_args[0][2]
        assert "-crf" in args
        assert "18" in args  # High quality CRF value
        assert "-preset" in args
        assert "slow" in args

    @patch('src.converter.video.VideoConverter._run_ffmpeg')
    def test_compress_video_medium_quality(self, mock_run_ffmpeg, video_converter, tmp_path):
        """Test video compression with medium quality (default)."""
        input_file = tmp_path / "test.mp4"
        input_file.write_text("dummy video content")

        mock_run_ffmpeg.return_value = True

        result = video_converter.compress_video(str(input_file))

        assert result is not None
        assert result.endswith("_compressed.mp4")
        args = mock_run_ffmpeg.call_args[0][2]
        assert "-crf" in args
        assert "23" in args  # Medium quality CRF value
        assert "-preset" in args
        assert "medium" in args

    @patch('src.converter.video.VideoConverter._run_ffmpeg')
    def test_compress_video_low_quality(self, mock_run_ffmpeg, video_converter, tmp_path):
        """Test video compression with low quality."""
        input_file = tmp_path / "test.mp4"
        input_file.write_text("dummy video content")

        mock_run_ffmpeg.return_value = True

        result = video_converter.compress_video(str(input_file), quality="low")

        assert result is not None
        assert result.endswith("_compressed.mp4")
        args = mock_run_ffmpeg.call_args[0][2]
        assert "-crf" in args
        assert "28" in args  # Low quality CRF value
        assert "-preset" in args
        assert "fast" in args

    def test_get_video_info_file_not_exists(self, video_converter):
        """Test getting video info for non-existent file."""
        result = video_converter.get_video_info("nonexistent.mp4")
        assert result is None

    @patch('subprocess.run')
    @patch('json.loads')
    def test_get_video_info_success(self, mock_json_loads, mock_subprocess, video_converter, tmp_path):
        """Test successful video info retrieval."""
        input_file = tmp_path / "test.mp4"
        input_file.write_text("dummy content")

        mock_subprocess.return_value = MagicMock(returncode=0, stdout='{"test": "data"}')
        mock_json_loads.return_value = {"test": "data"}

        result = video_converter.get_video_info(str(input_file))

        assert result == {"test": "data"}
        mock_subprocess.assert_called_once()

    @patch('subprocess.run')
    def test_get_video_info_ffprobe_not_found(self, mock_subprocess, video_converter, tmp_path):
        """Test video info retrieval when ffprobe is not found."""
        input_file = tmp_path / "test.mp4"
        input_file.write_text("dummy content")

        mock_subprocess.side_effect = FileNotFoundError()

        result = video_converter.get_video_info(str(input_file))
        assert result is None

    @patch('subprocess.run')
    def test_get_video_info_invalid_json(self, mock_subprocess, video_converter, tmp_path):
        """Test video info retrieval with invalid JSON response."""
        input_file = tmp_path / "test.mp4"
        input_file.write_text("dummy content")

        mock_subprocess.return_value = MagicMock(returncode=0, stdout='invalid json')

        result = video_converter.get_video_info(str(input_file))
        assert result is None