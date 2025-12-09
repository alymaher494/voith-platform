#!/usr/bin/env python3
"""
Command-line script to extract handwritten text from images using Microsoft TrOCR Large model.

Usage:
    python ocr_image.py /path/to/image.jpg [--output output.txt] [--format json]

This script will:
1. Load the Microsoft TrOCR Large Handwritten model
2. Extract handwritten text from the provided image using segmentation
3. Save the extracted text to a file or print to stdout
"""

import argparse
import json
import logging
import sys
from pathlib import Path

# Add project root to sys.path for proper imports
sys.path.insert(0, str(Path(__file__).parent))

from src.ocr.core import OCREngine
from src.translation import TextTranslator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Extract handwritten text from images using Microsoft TrOCR Large model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
 Examples:
     # Basic handwritten text extraction
     python ocr_image.py image.jpg

     # Extract and translate to French
     python ocr_image.py image.jpg --translate --target-language fr

     # Extract and translate with contextual translation
     python ocr_image.py image.jpg --translate --context

     # Full pipeline: OCR → Translation
     python ocr_image.py image.jpg --translate --target-language ar --context

     # Save translated results as JSON (includes both original and translated text)
     python ocr_image.py image.jpg --translate --format json --output result.json

     # Save translated results as formatted text
     python ocr_image.py image.jpg --translate --output result.txt

     # Batch processing with full pipeline
     python ocr_image.py image1.jpg image2.jpg --correct-typos --translate --target-language es --output results.json --format json

     # Enable verbose logging
     python ocr_image.py image.jpg --verbose
         """
    )

    parser.add_argument(
        'image_paths',
        nargs='+',
        help='Path(s) to image file(s) to process'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output file path (prints to stdout if not specified)'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--ocr-type',
        default='handwritten',
        help='OCR type for TrOCR (default: handwritten - optimized for handwritten text)'
    )

    parser.add_argument(
        '--translate', '-t',
        action='store_true',
        help='Translate the extracted text to another language'
    )

    parser.add_argument(
        '--target-language', '-l',
        default='en',
        help='Target language for translation (default: en)'
    )


    parser.add_argument(
        '--context',
        action='store_true',
        help='Use contextual NLLB translation (better quality, slower)'
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

    # Validate input files
    invalid_files = []
    for image_path in args.image_paths:
        path = Path(image_path)
        if not path.exists():
            invalid_files.append(image_path)
        elif not path.is_file():
            invalid_files.append(image_path)

    if invalid_files:
        logger.error(f"Invalid file(s): {', '.join(invalid_files)}")
        sys.exit(1)

    try:
        logger.info("Initializing OCR engine...")
        ocr_engine = OCREngine()
        translator = None
        if args.translate:
            logger.info("Initializing translator...")
            translator = TextTranslator()

        if len(args.image_paths) == 1:
            # Single image processing
            logger.info(f"Processing image: {args.image_paths[0]}")
            result = ocr_engine.extract_text(args.image_paths[0], args.ocr_type)

            # Handle translation if requested
            if args.translate and result['text'].strip():
                try:
                    translated_text = translator.translate_text(
                        result['text'],
                        args.target_language,
                        context=args.context
                    )
                    result['translated_text'] = translated_text
                    result['target_language'] = args.target_language
                    logger.info(f"Successfully translated text to {args.target_language}")
                except Exception as e:
                    logger.warning(f"Translation failed: {e}")
                    result['translated_text'] = None
                    result['target_language'] = None

            if args.format == 'json':
                output_data = result
            else:
                if args.translate and 'translated_text' in result and result['translated_text']:
                    # For text format with translation, format as readable text
                    output_data = f"Original Text: {result['text']}\n\nTranslated Text: {result['translated_text']}"
                else:
                    output_data = result['text']

        else:
            # Batch processing
            logger.info(f"Processing {len(args.image_paths)} images...")
            results = ocr_engine.extract_text_batch(args.image_paths, args.ocr_type)

            # Handle translation for batch results
            if args.translate:
                for result in results:
                    if 'error' not in result and result['text'].strip():
                        try:
                            translated_text = translator.translate_text(
                                result['text'],
                                args.target_language,
                                context=args.context
                            )
                            result['translated_text'] = translated_text
                            result['target_language'] = args.target_language
                        except Exception as e:
                            logger.warning(f"Translation failed for {result.get('image_path')}: {e}")
                            result['translated_text'] = None
                            result['target_language'] = None

            if args.format == 'json':
                output_data = {
                    "results": results,
                    "total_images": len(results),
                    "successful": sum(1 for r in results if 'error' not in r),
                    "failed": sum(1 for r in results if 'error' in r)
                }
            else:
                # Combine all text results
                successful_results = [r for r in results if 'error' not in r]
                if args.translate:
                    output_data = "\n\n".join([
                        f"=== {Path(r['image_path']).name} ===\nOriginal: {r['text']}\nTranslated: {r.get('translated_text', 'Translation failed')}"
                        for r in successful_results
                    ])
                else:
                    output_data = "\n\n".join([
                        f"=== {Path(r['image_path']).name} ===\n{r['text']}"
                        for r in successful_results
                    ])

                if any('error' in r for r in results):
                    failed_count = sum(1 for r in results if 'error' in r)
                    output_data += f"\n\n⚠️  {failed_count} image(s) failed to process"

        # Output handling
        if args.output:
            logger.info(f"Saving results to: {args.output}")
            with open(args.output, 'w', encoding='utf-8') as f:
                if args.format == 'json':
                    json.dump(output_data, f, indent=2, ensure_ascii=False)
                else:
                    f.write(output_data)
        else:
            # Print to stdout
            if args.format == 'json':
                print(json.dumps(output_data, indent=2, ensure_ascii=False))
            else:
                if isinstance(output_data, dict):
                    # Handle dict output_data (shouldn't happen with the fix above, but safety check)
                    print(json.dumps(output_data, indent=2, ensure_ascii=False))
                else:
                    print(output_data)

        # Print summary
        if len(args.image_paths) == 1:
            logger.info("✅ OCR extraction completed successfully!")
            logger.info(f"📝 Extracted text length: {len(result['text'])} characters")
            logger.info(f"⏱️  Processing time: {result['processing_time']}s")
        else:
            successful = sum(1 for r in results if 'error' not in r)
            logger.info("✅ Batch OCR processing completed!")
            logger.info(f"📊 Successfully processed: {successful}/{len(args.image_paths)} images")

        sys.exit(0)

    except Exception as e:
        logger.error(f"❌ OCR processing failed: {str(e)}")
        if args.verbose:
            logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()