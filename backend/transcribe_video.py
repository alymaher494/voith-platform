#!/usr/bin/env python3
"""
Command-line script to transcribe video files with word-level timestamps.

Usage:
    python transcribe_video.py /path/to/video/file.mp4 [--output output.json] [--language en] [--model base]

This script will:
1. Extract audio from the video file
2. Transcribe the audio using WhisperX
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
from src.summarizer import ContentProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)




def main():
    parser = argparse.ArgumentParser(
        description="Transcribe video files with word-level timestamps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic video transcription
    python transcribe_video.py video.mp4

    # Specify output file and language
    python transcribe_video.py video.mp4 --output transcription.json --language en

    # Use different model size and audio format
    python transcribe_video.py video.mp4 --model small --audio-format wav

    # Enable verbose logging
    python transcribe_video.py video.mp4 --verbose

    # Translate transcription to French
    python transcribe_video.py video.mp4 --translate fr

    # Use contextual translation for better quality
    python transcribe_video.py video.mp4 --translate fr --context

    # Summarize the transcription
    python transcribe_video.py video.mp4 --summarize

    # Summarize with different styles
    python transcribe_video.py video.mp4 --summarize --summary-style bullet_points

        """
    )

    parser.add_argument(
        'video_path',
        help='Path to the video file to transcribe'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output JSON file path (default: <video_name>_transcription.json)'
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
        '--audio-format',
        default='wav',
        choices=['wav', 'mp3', 'flac', 'aac'],
        help='Audio format to extract from video (default: wav)'
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

    parser.add_argument(
        '--summarize', '-s',
        action='store_true',
        help='Summarize the transcribed content using mT5-XLSum'
    )

    parser.add_argument(
        '--summary-style',
        default='structured',
        choices=['structured', 'bullet_points', 'paragraph', 'both'],
        help='Summary output style (default: structured)'
    )




    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate input file
    video_path = Path(args.video_path)
    if not video_path.exists():
        logger.error(f"Video file not found: {video_path}")
        sys.exit(1)

    if not video_path.is_file():
        logger.error(f"Path is not a file: {video_path}")
        sys.exit(1)

    # Determine output file
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = video_path.parent / f"{video_path.stem}_transcription.json"

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        logger.info(f"Initializing AudioTranscriber...")
        transcriber = AudioTranscriber()

        logger.info(f"Starting video transcription of: {video_path}")
        logger.info(f"Using model: {args.model}")
        logger.info(f"Audio extraction format: {args.audio_format}")
        if args.language:
            logger.info(f"Language: {args.language}")
        if args.translate:
            logger.info(f"Translation: {args.translate} (context: {args.context})")
        if args.summarize:
            logger.info(f"Summarization: enabled (style: {args.summary_style})")

        # Perform transcription
        result = transcriber.transcribe_video(
            video_path=str(video_path),
            language=args.language,
            model_size=args.model,
            extract_audio_format=args.audio_format,
            translate_to=args.translate,
            context=args.context
        )

        # Handle summarization if requested
        summarized_content = None
        if args.summarize and result.text.strip():
            try:
                logger.info(f"Summarizing content (style: {args.summary_style})...")
                summarizer = ContentProcessor()
                # Use translated text if available, otherwise original text
                text_to_summarize = getattr(result, 'translated_text', None) or result.text
                summarized_content = summarizer.summarize(text_to_summarize, summary_style=args.summary_style)
                logger.info("Content summarization completed")
            except Exception as e:
                logger.warning(f"Summarization failed: {e}")

        # Convert result to dictionary for JSON serialization
        result_dict = {
            "text": result.text,
            "translated_text": getattr(result, 'translated_text', None),
            "summarized_content": summarized_content,
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
        logger.info("✅ Video transcription completed successfully!")
        logger.info(f"📄 Full text: {result.text[:100]}{'...' if len(result.text) > 100 else ''}")
        logger.info(f"🎯 Language: {result.language}")
        logger.info(f"⏱️  Processing time: {result.processing_time:.2f}s")
        logger.info(f"📊 Segments: {len(result.segments)}")
        if summarized_content:
            logger.info(f"📝 Summary: {summarized_content[:100]}{'...' if len(summarized_content) > 100 else ''}")
        logger.info(f"� Saved to: {output_path}")

        sys.exit(0)

    except Exception as e:
        logger.error(f"❌ Video transcription failed: {str(e)}")
        if args.verbose:
            logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()