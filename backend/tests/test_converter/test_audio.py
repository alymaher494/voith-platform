"""
Tests for audio converter functionality.
"""
import pytest
import tempfile
import os
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.converter.audio import AudioConverter


@pytest.fixture
def audio_converter(tmp_path):
    """Create an AudioConverter instance with temporary directory."""
    converter = AudioConverter(output_dir=str(tmp_path / "converted"))
    yield converter
    # Cleanup is handled by tmp_path fixture


class TestAudioConverter:
    """Test suite for AudioConverter class."""

    def test_initialization(self, tmp_path):
        """Test AudioConverter initialization."""
        output_dir = tmp_path / "test_output"
        converter = AudioConverter(output_dir=str(output_dir))

        assert converter.output_dir == output_dir
        assert output_dir.exists()

    def test_initialization_default_dir(self):
        """Test AudioConverter with default output directory."""
        converter = AudioConverter()
        assert converter.output_dir == Path("./converted")

    @patch('subprocess.run')
    def test_run_ffmpeg_success(self, mock_subprocess, audio_converter):
        """Test successful FFmpeg execution."""
        mock_subprocess.return_value = MagicMock(returncode=0)

        result = audio_converter._run_ffmpeg("input.mp3", "output.wav", [])
        assert result is True
        mock_subprocess.assert_called_once()

    @patch('subprocess.run')
    def test_run_ffmpeg_failure(self, mock_subprocess, audio_converter):
        """Test FFmpeg execution failure."""
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'ffmpeg', stderr="FFmpeg failed")

        result = audio_converter._run_ffmpeg("input.mp3", "output.wav", [])
        assert result is False

    @patch('subprocess.run')
    def test_run_ffmpeg_file_not_found(self, mock_subprocess, audio_converter):
        """Test FFmpeg not found."""
        mock_subprocess.side_effect = FileNotFoundError()

        result = audio_converter._run_ffmpeg("input.mp3", "output.wav", [])
        assert result is False

    def test_convert_mp3_to_wav_file_not_exists(self, audio_converter):
        """Test MP3 to WAV conversion with non-existent file."""
        result = audio_converter.convert_mp3_to_wav("nonexistent.mp3")
        assert result is None

    @patch('src.converter.audio.AudioConverter._run_ffmpeg')
    def test_convert_mp3_to_wav_success(self, mock_run_ffmpeg, audio_converter, tmp_path):
        """Test successful MP3 to WAV conversion."""
        # Create a dummy input file
        input_file = tmp_path / "test.mp3"
        input_file.write_text("dummy mp3 content")

        mock_run_ffmpeg.return_value = True

        result = audio_converter.convert_mp3_to_wav(str(input_file))

        assert result is not None
        assert result.endswith(".wav")
        mock_run_ffmpeg.assert_called_once()

    @patch('src.converter.audio.AudioConverter._run_ffmpeg')
    def test_convert_mp3_to_wav_failure(self, mock_run_ffmpeg, audio_converter, tmp_path):
        """Test failed MP3 to WAV conversion."""
        input_file = tmp_path / "test.mp3"
        input_file.write_text("dummy mp3 content")

        mock_run_ffmpeg.return_value = False

        result = audio_converter.convert_mp3_to_wav(str(input_file))
        assert result is None

    def test_convert_wav_to_mp3_file_not_exists(self, audio_converter):
        """Test WAV to MP3 conversion with non-existent file."""
        result = audio_converter.convert_wav_to_mp3("nonexistent.wav")
        assert result is None

    @patch('src.converter.audio.AudioConverter._run_ffmpeg')
    def test_convert_wav_to_mp3_success(self, mock_run_ffmpeg, audio_converter, tmp_path):
        """Test successful WAV to MP3 conversion."""
        input_file = tmp_path / "test.wav"
        input_file.write_text("dummy wav content")

        mock_run_ffmpeg.return_value = True

        result = audio_converter.convert_wav_to_mp3(str(input_file))

        assert result is not None
        assert result.endswith(".mp3")
        mock_run_ffmpeg.assert_called_once()

    def test_convert_audio_format_file_not_exists(self, audio_converter):
        """Test audio format conversion with non-existent file."""
        result = audio_converter.convert_audio_format("nonexistent.mp3", "wav")
        assert result is None

    @patch('src.converter.audio.AudioConverter._run_ffmpeg')
    def test_convert_audio_format_mp3(self, mock_run_ffmpeg, audio_converter, tmp_path):
        """Test audio format conversion to MP3."""
        input_file = tmp_path / "test.wav"
        input_file.write_text("dummy content")

        mock_run_ffmpeg.return_value = True

        result = audio_converter.convert_audio_format(str(input_file), "mp3")

        assert result is not None
        assert result.endswith(".mp3")
        # Check that MP3-specific arguments were used
        args = mock_run_ffmpeg.call_args[0][2]
        assert "-acodec" in args
        assert "libmp3lame" in args

    @patch('src.converter.audio.AudioConverter._run_ffmpeg')
    def test_convert_audio_format_flac(self, mock_run_ffmpeg, audio_converter, tmp_path):
        """Test audio format conversion to FLAC."""
        input_file = tmp_path / "test.wav"
        input_file.write_text("dummy content")

        mock_run_ffmpeg.return_value = True

        result = audio_converter.convert_audio_format(str(input_file), "flac")

        assert result is not None
        assert result.endswith(".flac")
        args = mock_run_ffmpeg.call_args[0][2]
        assert "-acodec" in args
        assert "flac" in args

    def test_get_audio_info_file_not_exists(self, audio_converter):
        """Test getting audio info for non-existent file."""
        result = audio_converter.get_audio_info("nonexistent.mp3")
        assert result is None

    @patch('subprocess.run')
    @patch('json.loads')
    def test_get_audio_info_success(self, mock_json_loads, mock_subprocess, audio_converter, tmp_path):
        """Test successful audio info retrieval."""
        input_file = tmp_path / "test.mp3"
        input_file.write_text("dummy content")

        mock_subprocess.return_value = MagicMock(returncode=0, stdout='{"test": "data"}')
        mock_json_loads.return_value = {"test": "data"}

        result = audio_converter.get_audio_info(str(input_file))

        assert result == {"test": "data"}
        mock_subprocess.assert_called_once()

    @patch('subprocess.run')
    def test_get_audio_info_ffprobe_not_found(self, mock_subprocess, audio_converter, tmp_path):
        """Test audio info retrieval when ffprobe is not found."""
        input_file = tmp_path / "test.mp3"
        input_file.write_text("dummy content")

        mock_subprocess.side_effect = FileNotFoundError()

        result = audio_converter.get_audio_info(str(input_file))
        assert result is None

    @patch('subprocess.run')
    def test_get_audio_info_invalid_json(self, mock_subprocess, audio_converter, tmp_path):
        """Test audio info retrieval with invalid JSON response."""
        input_file = tmp_path / "test.mp3"
        input_file.write_text("dummy content")

        mock_subprocess.return_value = MagicMock(returncode=0, stdout='invalid json')

        result = audio_converter.get_audio_info(str(input_file))
        assert result is None