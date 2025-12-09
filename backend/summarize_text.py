#!/usr/bin/env python3
"""
Command-line script to summarize text from a file (text or JSON).

Usage:
    python summarize_text.py /path/to/text/file.txt [--output summary.txt]
    python summarize_text.py input.json --field text --output output.json

This script will:
1. Read text from the input file (plain text or JSON)
2. Summarize the text using mT5-XLSum
3. Save the summary to a file or print to stdout
"""

import argparse
import json
import logging
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from src.summarizer import ContentProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Summarize text from a file (text or JSON) using mT5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic text file summarization
    python summarize_text.py document.txt

    # JSON file summarization
    python summarize_text.py input.json --field text --output output.json

    # Specify max length and style
    python summarize_text.py document.txt --max-length 200 --style bullet_points

    # JSON with custom field and paragraph style
    python summarize_text.py data.json --field content --output summary.json --style paragraph
        """
    )

    parser.add_argument(
        'file_path',
        help='Path to the text or JSON file to summarize'
    )

    parser.add_argument(
        '--field', '-f',
        help='Field name in JSON file to summarize (required for JSON files)'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output file path (optional, prints to stdout if not specified)'
    )


    parser.add_argument(
        '--max-length',
        type=int,
        default=150,
        help='Maximum length of summary (default: 150)'
    )

    parser.add_argument(
        '--style',
        default='structured',
        choices=['structured', 'bullet_points', 'paragraph', 'both'],
        help='Summary style (default: structured)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate input file
    input_file = Path(args.file_path)
    if not input_file.exists():
        logger.error(f"Input file not found: {input_file}")
        sys.exit(1)

    if not input_file.is_file():
        logger.error(f"Path is not a file: {input_file}")
        sys.exit(1)

    try:
        # Determine if file is JSON based on extension or content
        is_json = input_file.suffix.lower() == '.json'

        if is_json or args.field:
            # Handle JSON file
            if not args.field:
                logger.error("--field is required when processing JSON files")
                sys.exit(1)

            logger.info(f"Reading JSON from: {input_file}")
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if args.field not in data:
                logger.error(f"Field '{args.field}' not found in JSON file")
                sys.exit(1)

            text = str(data[args.field]).strip()
            logger.info(f"Extracted text from field '{args.field}' (length: {len(text)} characters)")
        else:
            # Handle plain text file
            logger.info(f"Reading text from: {input_file}")
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read().strip()

        if not text:
            logger.error("Input text is empty")
            sys.exit(1)

        # Initialize summarizer
        logger.info("Initializing ContentProcessor...")
        summarizer = ContentProcessor()

        # Perform summarization
        logger.info("Starting text summarization...")
        summary = summarizer.summarize(text, max_length=args.max_length, summary_style=args.style)

        if summary is None:
            logger.error("Summarization failed")
            sys.exit(1)

        # Prepare output data
        output_data = {
            "original_text": text,
            "summarized_text": summary
        }

        # Output result
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Summary saved to: {output_path}")
        else:
            print(json.dumps(output_data, indent=2, ensure_ascii=False))

        logger.info("✅ Text summarization completed successfully!")

        sys.exit(0)

    except json.JSONDecodeError as e:
        logger.error(f"❌ Invalid JSON file: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Text summarization failed: {str(e)}")
        if args.verbose:
            logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()