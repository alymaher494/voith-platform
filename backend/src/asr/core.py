"""
Core ASR functionality using WhisperX for accurate transcription with word-level timestamps.
"""

import logging
import time
import pickle
from pathlib import Path
from typing import Optional, Dict, Any, List, Iterator
import torch

# Import WhisperX components
try:
    import torch
    import whisperx

    WHISPERX_AVAILABLE = True
except ImportError:
    WHISPERX_AVAILABLE = False
    torch = None
    whisperx = None

from .models import (
    TranscriptionResult,
    TranscriptionSegment,
    WordTimestamp,
    TranscribeRequest,
    TranscribeVideoRequest,
)

# Import translation for optional integration
try:
    from ..translation import TextTranslator

    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    TextTranslator = None

logger = logging.getLogger(__name__)


def print_iterator(message: str, iterator: Iterator) -> Iterator:
    """Print each item from iterator with a message and yield it."""
    for item in iterator:
        print(f"{message}: {item}")
        yield item


class AudioTranscriber:
    """
    Audio transcription service using WhisperX.

    Provides high-accuracy speech-to-text transcription with word-level timestamps,
    supporting multiple languages and various audio formats.
    """

    def __init__(self, device: str = "auto", compute_type: str = "auto"):
        """
        Initialize the transcriber.

        Args:
            device: Device to use ('auto', 'cpu', 'cuda')
            compute_type: Compute precision ('auto', 'float16', 'float32', 'int8')
        """
        if not WHISPERX_AVAILABLE:
            raise ImportError(
                "WhisperX is not installed. Install with: "
                "pip install git+https://github.com/m-bain/whisperx.git")

        self.device = self._get_device(device)
        self.compute_type = self._get_compute_type(compute_type)
        self.models = {}  # Cache loaded models

        logger.info(
            f"Initialized AudioTranscriber with device: {self.device}, compute_type: {self.compute_type}"
        )

    def _get_device(self, device: str) -> str:
        """Determine the appropriate device to use."""
        if device == "auto":
            if torch and torch.cuda.is_available():
                return "cuda"
            else:
                return "cpu"
        return device

    def _get_compute_type(self, compute_type: str) -> str:
        """Determine the appropriate compute type based on device capabilities."""
        if compute_type == "auto":
            # Use float32 for CPU, float16 for CUDA
            if self.device == "cuda":
                return "float16"
            else:
                return "float32"
        return compute_type

    def _load_model(self, model_size: str, language: Optional[str] = None):
        """
        Load or retrieve cached WhisperX model.

        Args:
            model_size: Model size ('tiny', 'base', 'small', 'medium', 'large')
            language: Language code for language-specific models
        """
        model_key = f"{model_size}_{language or 'multilingual'}"

        if model_key not in self.models:
            logger.info(f"Loading WhisperX model: {model_key}")
            try:
                model = whisperx.load_model(
                    model_size,
                    device=self.device,
                    compute_type=self.compute_type,
                    language=language,
                )
                self.models[model_key] = model
                logger.info(f"Successfully loaded model: {model_key}")
            except Exception as e:
                logger.error(f"Failed to load model {model_key}: {e}")
                raise

        return self.models[model_key]

    def transcribe_audio(
        self,
        audio_path: str,
        language: Optional[str] = None,
        model_size: str = "base",
        batch_size: int = 16,
        show_progress: bool = True,
        translate_to: Optional[str] = None,
        context: bool = False,
        correct_typos: bool = False,
    ) -> TranscriptionResult:
        """
        Transcribe audio file with word-level timestamps.

        Args:
            audio_path: Path to audio file
            language: Language code (auto-detect if None)
            model_size: Whisper model size
            batch_size: Batch size for alignment
            translate_to: Target language code for translation (optional)
            context: Use contextual translation (optional)
            correct_typos: Apply typo correction to transcription (optional)

        Returns:
            TranscriptionResult with full transcription and timestamps
        """
        start_time = time.time()
        print(f"🎯 Starting transcription at {time.strftime('%H:%M:%S')}")

        # Validate input file
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        logger.info(f"Starting transcription of: {audio_path}")

        try:
            # Load audio
            audio = whisperx.load_audio(str(audio_path))

            # Load model
            model = self._load_model(model_size, language)

            # Transcribe with streaming output
            logger.info("Running WhisperX transcription...")
            print("🎯 Running WhisperX transcription...")

            # Transcribe and get segments
            result = model.transcribe(audio,
                                      batch_size=batch_size,
                                      print_progress=True,
                                      verbose=False)

            # Translate segments immediately if requested
            if translate_to and TRANSLATION_AVAILABLE:
                print(
                    f"🌐 Translating segments to {translate_to} in real-time..."
                )
                translator = TextTranslator()

                translated_segments = []
                for segment in result["segments"]:
                    # Print original with timestamps
                    print(
                        f"📝 [{segment['start']:.2f}-{segment['end']:.2f}] {segment['text']}"
                    )

                    # Translate
                    translated_text = translator.translate_text(
                        segment["text"], translate_to, context)

                    if translated_text:
                        segment["translated_text"] = translated_text
                        # Print translated text with timestamps
                        print(f"✅ [{segment['start']:.2f}-{segment['end']:.2f}] Translation: {translated_text}")
                    else:
                        segment["translated_text"] = "NA"
                        print(f"❌ [{segment['start']:.2f}-{segment['end']:.2f}] Translation failed")

                    print()  # Empty line for readability
                    translated_segments.append(segment)

                result["segments"] = translated_segments
            else:
                # No translation, just print segments
                result["segments"] = list(
                    print_iterator("Whisper", result["segments"]))

            # Align for word-level timestamps with streaming
            logger.info("Aligning for word-level timestamps...")
            print("🎯 Starting alignment...")

            model_a, metadata = whisperx.load_align_model(
                language_code=result["language"], device=self.device)

            # Use regular align but wrap with progress tracking
            result = whisperx.align(
                result["segments"],
                model_a,
                metadata,
                str(audio_path),
                self.device,
                return_char_alignments=False,
            )

            # Wrap result with print_iterator for streaming output
            result = list(print_iterator("Aligned", [result]))[0]

            print(f"⏱️  First line time: {time.time() - start_time:.2f}s")


            # Convert to our model format
            transcription_result = self._convert_to_result_format(
                result, audio_path,
                time.time() - start_time)

            # Apply typo correction if requested
            if correct_typos and TYPO_CORRECTOR_AVAILABLE:
                logger.info("Applying typo correction to transcription...")
                try:
                    corrector = MultilingualTypoCorrector()
                    corrected_text = corrector.correct_text(transcription_result.text, language=language)
                    original_text = transcription_result.text
                    transcription_result.text = corrected_text

                    # Also correct individual segments
                    for segment in transcription_result.segments:
                        if segment.text.strip():
                            segment.text = corrector.correct_text(segment.text, language=language)

                    logger.info(f"Typo correction applied: {len(original_text)} → {len(corrected_text)} characters")
                except Exception as e:
                    logger.warning(f"Typo correction failed: {e}")
                    # Continue without correction rather than failing

            # Optional translation
            if translate_to and TRANSLATION_AVAILABLE:
                print(f"🌐 Translating transcription to {translate_to}...")
                translator = TextTranslator()

                translated_segments = []

                for i, segment in enumerate(transcription_result.segments, 1):
                    print(
                        f"🔄 Translating segment {i}/{len(transcription_result.segments)}..."
                    )
                    translated_text = translator.translate_text(
                        segment.text, translate_to, context)

                    if translated_text:
                        segment.translated_text = translated_text
                        print(
                            f"✅ [{segment.start:.2f}-{segment.end:.2f}] {segment.text} → {translated_text}"
                        )
                    else:
                        segment.translated_text = "NA"
                        print(
                            f"❌ [{segment.start:.2f}-{segment.end:.2f}] Translation failed: {segment.text}"
                        )

                    translated_segments.append(segment.translated_text)

                # Set the full translated text
                transcription_result.translated_text = " ".join(
                    translated_segments)
                print(
                    f"✅ Translation completed ({len(translated_segments)} segments)"
                )
                logger.info(f"Translation completed for {len(translated_segments)} segments")
            else:
                # No translation requested
                print("📝 Final transcription segments (no translation):")
                for segment in transcription_result.segments:
                    print(
                        f"[{segment.start:.2f}-{segment.end:.2f}] {segment.text}"
                    )

            logger.info(
                f"Transcription completed in {transcription_result.processing_time:.2f}s"
            )
            return transcription_result

        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise

    def transcribe_video(
        self,
        video_path: str,
        language: Optional[str] = None,
        model_size: str = "base",
        extract_audio_format: str = "wav",
        batch_size: int = 16,
        translate_to: Optional[str] = None,
        context: bool = False,
        correct_typos: bool = False,
    ) -> TranscriptionResult:
        """
        Transcribe video by first extracting audio, then transcribing.

        Args:
            video_path: Path to video file
            language: Language code (auto-detect if None)
            model_size: Whisper model size
            extract_audio_format: Audio format to extract ('wav', 'mp3', etc.)
            batch_size: Batch size for alignment
            translate_to: Target language code for translation (optional)
            context: Use contextual translation (optional)
            correct_typos: Apply typo correction to transcription (optional)

        Returns:
            TranscriptionResult with full transcription and timestamps
        """
        from ..converter.video import VideoConverter

        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        logger.info(f"Processing video for transcription: {video_path}")

        # Extract audio from video
        converter = VideoConverter()
        temp_audio_path = None

        try:
            # Extract audio to temporary file
            temp_audio_path = converter.extract_audio_from_video(
                str(video_path), audio_format=extract_audio_format)

            if not temp_audio_path:
                raise RuntimeError("Failed to extract audio from video")

            logger.info(f"Extracted audio to: {temp_audio_path}")

            # Transcribe the extracted audio
            result = self.transcribe_audio(
                temp_audio_path,
                language=language,
                model_size=model_size,
                batch_size=batch_size,
                translate_to=translate_to,
                context=context,
                correct_typos=correct_typos,
            )

            # Update metadata to reflect video source
            result.text = f"[Video: {video_path.name}] {result.text}"

            return result

        finally:
            # Clean up temporary audio file
            if temp_audio_path and Path(temp_audio_path).exists():
                try:
                    Path(temp_audio_path).unlink()
                    logger.info(
                        f"Cleaned up temporary audio file: {temp_audio_path}")
                except Exception as e:
                    logger.warning(
                        f"Failed to clean up temporary file {temp_audio_path}: {e}"
                    )

    def _convert_to_result_format(
            self, whisperx_result: Dict[str, Any], source_path: Path,
            processing_time: float) -> TranscriptionResult:
        """Convert WhisperX result to our TranscriptionResult format."""
        segments = []

        for segment in whisperx_result.get("segments", []):
            words = []
            for word_info in segment.get("words", []):
                words.append(
                    WordTimestamp(
                        word=word_info.get("word", ""),
                        start=word_info.get("start", 0.0),
                        end=word_info.get("end", 0.0),
                        confidence=word_info.get("score", None),
                    ))

            segments.append(
                TranscriptionSegment(
                    text=segment.get("text", ""),
                    start=segment.get("start", 0.0),
                    end=segment.get("end", 0.0),
                    words=words,
                ))

        # Calculate overall confidence if available
        overall_confidence = None
        if segments:
            word_confidences = [
                word.confidence for segment in segments
                for word in segment.words if word.confidence is not None
            ]
            if word_confidences:
                overall_confidence = sum(word_confidences) / len(
                    word_confidences)

        # Build full text from segments
        full_text = " ".join([seg.text for seg in segments])

        return TranscriptionResult(
            text=full_text,
            language=whisperx_result.get("language", "unknown"),
            segments=segments,
            processing_time=processing_time,
            model=f"whisperx-{whisperx_result.get('model_size', 'unknown')}",
            confidence=overall_confidence,
        )

    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        if not WHISPERX_AVAILABLE:
            return []

        # WhisperX supports all Whisper languages
        return [
            "en",
            "zh",
            "de",
            "es",
            "ru",
            "ko",
            "fr",
            "ja",
            "pt",
            "tr",
            "pl",
            "ca",
            "nl",
            "ar",
            "sv",
            "it",
            "id",
            "hi",
            "fi",
            "vi",
            "he",
            "uk",
            "el",
            "ms",
            "cs",
            "ro",
            "da",
            "hu",
            "ta",
            "no",
            "th",
            "ur",
            "hr",
            "bg",
            "lt",
            "la",
            "mi",
            "ml",
            "cy",
            "sk",
            "te",
            "fa",
            "lv",
            "bn",
            "sr",
            "az",
            "sl",
            "kn",
            "et",
            "mk",
            "br",
            "eu",
            "is",
            "hy",
            "ne",
            "mn",
            "bs",
            "kk",
            "sq",
            "sw",
            "gl",
            "mr",
            "pa",
            "si",
            "km",
            "sn",
            "yo",
            "so",
            "af",
            "oc",
            "ka",
            "be",
            "tg",
            "sd",
            "gu",
            "am",
            "yi",
            "lo",
            "uz",
            "fo",
            "ht",
            "ps",
            "tk",
            "nn",
            "mt",
            "sa",
            "lb",
            "my",
            "bo",
            "tl",
            "mg",
            "as",
            "tt",
            "haw",
            "ln",
            "ha",
            "ba",
            "jw",
            "su",
        ]

    def get_model_sizes(self) -> List[str]:
        """Get available model sizes."""
        return ["tiny", "base", "small", "medium", "large"]

