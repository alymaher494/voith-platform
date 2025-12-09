#!/usr/bin/env python3
"""
Command-line script to transcribe audio files with word-level timestamps.

Usage:
    python transcribe_audio.py /path/to/audio/file.wav [--output output.json] [--language en] [--model base]

This script will:
1. Load the audio file
2. Transcribe it using WhisperX
3. Save the transcription with word-level timestamps to a JSON file
"""

import argparse
import json
import logging
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from src.asr.core import AudioTranscriber

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)




def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio files with word-level timestamps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic transcription
    python transcribe_audio.py audio.wav

    # Specify output file and language
    python transcribe_audio.py audio.wav --output transcription.json --language en

    # Use different model size
    python transcribe_audio.py audio.wav --model small

    # Enable verbose logging
    python transcribe_audio.py audio.wav --verbose

    # Translate transcription to French
    python transcribe_audio.py audio.wav --translate fr

    # Use contextual translation for better quality
    python transcribe_audio.py audio.wav --translate fr --context

        """
    )

    parser.add_argument(
        'audio_path',
        help='Path to the audio file to transcribe'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output JSON file path (default: <audio_name>_transcription.json)'
    )

    parser.add_argument(
        '--language', '-l',
        help='Language code (auto-detect if not specified)'
    )

    parser.add_argument(
        '--model', '-m',
        default='base',
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        help='Whisper model size (default: base)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    parser.add_argument(
        '--translate', '-t',
        help='Translate transcription to target language (e.g., en, fr, es)'
    )

    parser.add_argument(
        '--context', '-c',
        action='store_true',
        help='Use contextual NLLB translation (better quality, slower)'
    )



    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate input file
    audio_path = Path(args.audio_path)
    if not audio_path.exists():
        logger.error(f"Audio file not found: {audio_path}")
        sys.exit(1)

    if not audio_path.is_file():
        logger.error(f"Path is not a file: {audio_path}")
        sys.exit(1)

    # Determine output file
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = audio_path.parent / f"{audio_path.stem}_transcription.json"

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        logger.info(f"Initializing AudioTranscriber...")
        transcriber = AudioTranscriber()

        logger.info(f"Starting transcription of: {audio_path}")
        logger.info(f"Using model: {args.model}")
        if args.language:
            logger.info(f"Language: {args.language}")

        # Perform transcription
        result = transcriber.transcribe_audio(
            audio_path=str(audio_path),
            language=args.language,
            model_size=args.model,
            translate_to=args.translate,
            context=args.context
        )

        # Convert result to dictionary for JSON serialization
        result_dict = {
            "text": result.text,
            "translated_text": getattr(result, 'translated_text', None),
            "language": result.language,
            "processing_time": result.processing_time,
            "model": result.model,
            "confidence": result.confidence,
            "segments": [
                {
                    "text": segment.text,
                    "translated_text": getattr(segment, 'translated_text', None),
                    "start": segment.start,
                    "end": segment.end,
                    "words": [
                        {
                            "word": word.word,
                            "start": word.start,
                            "end": word.end,
                            "confidence": word.confidence
                        }
                        for word in segment.words
                    ],
                }
                for segment in result.segments
            ]
        }

        # Save to JSON file
        logger.info(f"Saving transcription to: {output_path}")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)

        # Print summary
        logger.info("✅ Transcription completed successfully!")
        logger.info(f"📄 Full text: {result.text[:100]}{'...' if len(result.text) > 100 else ''}")
        logger.info(f"🎯 Language: {result.language}")
        logger.info(f"⏱️  Processing time: {result.processing_time:.2f}s")
        logger.info(f"📊 Segments: {len(result.segments)}")
        logger.info(f"📝 Format: {args.format.upper()}")
        logger.info(f"� Saved to: {output_path}")

        sys.exit(0)

    except Exception as e:
        logger.error(f"❌ Transcription failed: {str(e)}")
        if args.verbose:
            logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()