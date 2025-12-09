"""
Tests for ASR functionality.
"""
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.asr.core import AudioTranscriber
from src.asr.models import TranscriptionResult, WordTimestamp


@pytest.fixture
def temp_audio_file(tmp_path):
    """Create a temporary audio file for testing."""
    audio_file = tmp_path / "test.wav"
    # Create a minimal WAV file header (44 bytes)
    wav_header = b'RIFF\x24\x08\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00}\x00\x00\x02\x00\x10\x00data\x00\x08\x00\x00'
    audio_file.write_bytes(wav_header + b'\x00\x01\x02\x03\x04\x05\x06\x07')  # Add some dummy audio data
    return str(audio_file)


@pytest.fixture
def mock_whisperx():
    """Mock WhisperX to avoid actual model loading."""
    with patch('src.asr.core.whisperx') as mock_whisperx:
        # Mock the load_audio function
        mock_whisperx.load_audio.return_value = MagicMock()

        # Mock the load_model function
        mock_model = MagicMock()
        mock_whisperx.load_model.return_value = mock_model

        # Mock the load_align_model function
        mock_align_model = MagicMock()
        mock_metadata = MagicMock()
        mock_whisperx.load_align_model.return_value = (mock_align_model, mock_metadata)

        # Mock the align function
        mock_whisperx.align.return_value = {
            "text": "This is a test transcription.",
            "language": "en",
            "segments": [
                {
                    "text": "This is a test transcription.",
                    "start": 0.0,
                    "end": 3.0,
                    "words": [
                        {"word": "This", "start": 0.0, "end": 0.5, "score": 0.9},
                        {"word": "is", "start": 0.5, "end": 0.8, "score": 0.95},
                        {"word": "a", "start": 0.8, "end": 1.0, "score": 0.85},
                        {"word": "test", "start": 1.0, "end": 1.5, "score": 0.92},
                        {"word": "transcription", "start": 1.5, "end": 3.0, "score": 0.88}
                    ]
                }
            ]
        }

        yield mock_whisperx


class TestAudioTranscriber:
    """Test suite for AudioTranscriber class."""

    def test_initialization(self):
        """Test AudioTranscriber initialization."""
        with patch('src.asr.core.torch.cuda.is_available', return_value=True):
            transcriber = AudioTranscriber()
            assert transcriber.device == "cuda"
            assert transcriber.compute_type == "float16"

    def test_initialization_cpu_fallback(self):
        """Test AudioTranscriber initialization with CPU fallback."""
        with patch('src.asr.core.torch.cuda.is_available', return_value=False):
            transcriber = AudioTranscriber()
            assert transcriber.device == "cpu"

    def test_initialization_custom_device(self):
        """Test AudioTranscriber initialization with custom device."""
        transcriber = AudioTranscriber(device="cpu", compute_type="float32")
        assert transcriber.device == "cpu"
        assert transcriber.compute_type == "float32"

    @patch('src.asr.core.whisperx')
    def test_transcribe_audio_success(self, mock_whisperx, temp_audio_file):
        """Test successful audio transcription."""
        # Setup mocks
        mock_model = MagicMock()
        mock_whisperx.load_model.return_value = mock_model
        mock_whisperx.load_audio.return_value = MagicMock()

        mock_align_model = MagicMock()
        mock_metadata = MagicMock()
        mock_whisperx.load_align_model.return_value = (mock_align_model, mock_metadata)

        mock_whisperx.align.return_value = {
            "text": "Hello world",
            "language": "en",
            "segments": [
                {
                    "text": "Hello world",
                    "start": 0.0,
                    "end": 2.0,
                    "words": [
                        {"word": "Hello", "start": 0.0, "end": 1.0, "score": 0.9},
                        {"word": "world", "start": 1.0, "end": 2.0, "score": 0.95}
                    ]
                }
            ]
        }

        transcriber = AudioTranscriber()
        result = transcriber.transcribe_audio(temp_audio_file)

        assert isinstance(result, TranscriptionResult)
        assert result.text == "Hello world"
        assert result.language == "en"
        assert len(result.segments) == 1
        assert len(result.segments[0].words) == 2
        assert result.processing_time > 0

    def test_transcribe_audio_file_not_found(self):
        """Test transcription with non-existent file."""
        transcriber = AudioTranscriber()

        with pytest.raises(FileNotFoundError):
            transcriber.transcribe_audio("nonexistent.wav")

    @patch('src.asr.core.whisperx')
    @patch('src.converter.video.VideoConverter')
    def test_transcribe_video_success(self, mock_video_converter, mock_whisperx, tmp_path):
        """Test successful video transcription."""
        # Create a dummy video file
        video_file = tmp_path / "test.mp4"
        video_file.write_bytes(b'dummy video content')

        # Mock the video converter to return a valid audio file path
        mock_converter_instance = MagicMock()
        mock_video_converter.return_value = mock_converter_instance
        temp_audio_path = tmp_path / "test_audio.wav"
        temp_audio_path.write_bytes(b'dummy audio content')
        mock_converter_instance.extract_audio_from_video.return_value = str(temp_audio_path)

        # Setup mocks similar to audio test
        mock_model = MagicMock()
        mock_whisperx.load_model.return_value = mock_model
        mock_whisperx.load_audio.return_value = MagicMock()

        mock_align_model = MagicMock()
        mock_metadata = MagicMock()
        mock_whisperx.load_align_model.return_value = (mock_align_model, mock_metadata)

        mock_whisperx.align.return_value = {
            "text": "Video transcription test",
            "language": "en",
            "segments": [
                {
                    "text": "Video transcription test",
                    "start": 0.0,
                    "end": 3.0,
                    "words": [
                        {"word": "Video", "start": 0.0, "end": 1.0, "score": 0.9},
                        {"word": "transcription", "start": 1.0, "end": 2.0, "score": 0.95},
                        {"word": "test", "start": 2.0, "end": 3.0, "score": 0.88}
                    ]
                }
            ]
        }

        transcriber = AudioTranscriber()
        result = transcriber.transcribe_video(str(video_file))

        assert isinstance(result, TranscriptionResult)
        assert "Video transcription test" in result.text
        assert result.language == "en"
        assert len(result.segments) == 1

    def test_get_supported_languages(self):
        """Test getting supported languages."""
        transcriber = AudioTranscriber()
        languages = transcriber.get_supported_languages()

        assert isinstance(languages, list)
        assert len(languages) > 0
        assert "en" in languages

    def test_get_model_sizes(self):
        """Test getting available model sizes."""
        transcriber = AudioTranscriber()
        models = transcriber.get_model_sizes()

        assert isinstance(models, list)
        assert "base" in models
        assert "small" in models
        assert "large" in models


class TestTranscriptionResult:
    """Test TranscriptionResult model."""

    def test_transcription_result_creation(self):
        """Test creating a TranscriptionResult."""
        words = [
            WordTimestamp(word="Hello", start=0.0, end=1.0, confidence=0.9),
            WordTimestamp(word="world", start=1.0, end=2.0, confidence=0.95)
        ]

        result = TranscriptionResult(
            text="Hello world",
            language="en",
            segments=[],
            processing_time=1.5,
            model="whisperx-base",
            confidence=0.92
        )

        assert result.text == "Hello world"
        assert result.language == "en"
        assert result.processing_time == 1.5
        assert result.model == "whisperx-base"
        assert result.confidence == 0.92

    def test_word_timestamp_creation(self):
        """Test creating a WordTimestamp."""
        word = WordTimestamp(
            word="test",
            start=1.0,
            end=2.0,
            confidence=0.85
        )

        assert word.word == "test"
        assert word.start == 1.0
        assert word.end == 2.0
        assert word.confidence == 0.85