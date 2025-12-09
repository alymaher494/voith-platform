#!/usr/bin/env python3
"""
Command-line interface for text translation.

Usage:
    python translate_text.py input.txt en --output translated.txt
    python translate_text.py input.txt fr
"""

import sys
import argparse
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from src.translation import translate_file_cli


def main():
    parser = argparse.ArgumentParser(
        description="Translate text file to a specified language.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python translate_text.py document.txt en
    python translate_text.py story.txt fr --output histoire.txt
    python translate_text.py article.txt es
        """
    )

    parser.add_argument('file_path', help='Path to the text file to translate')
    parser.add_argument('target_language',
                        help='Target language code (e.g., en, fr, es, de)')
    parser.add_argument('--output', '-o',
                        help='Output file path (optional, defaults to translated_{lang}.txt)')
    parser.add_argument('--context', action='store_true',
                        help='Use contextual NLLB translation (better quality, slower)')

    args = parser.parse_args()

    # Validate input file
    input_file = Path(args.file_path)
    if not input_file.exists():
        print(f"❌ Error: Input file '{args.file_path}' not found")
        sys.exit(1)

    print(f"🌐 Translating {args.file_path} to {args.target_language}...")

    # Perform translation
    result = translate_file_cli(args.file_path, args.target_language, args.output, args.context)

    if result:
        print(f"✅ Translation completed: {result}")
        sys.exit(0)
    else:
        print("❌ Translation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()