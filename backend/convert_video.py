#!/usr/bin/env python3
"""
Video converter script with tqdm progress display and automatic output to 'converted' folder.

Usage:
    python convert_video.py input.mp4 --format webm
    python convert_video.py input.mp4 --action extract_audio --format wav
    python convert_video.py input.mp4 --action compress --quality medium
    python convert_video.py input.mp4 --action change_resolution --resolution 1280x720
"""

import sys
import time
import argparse
from pathlib import Path
from tqdm import tqdm

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from src.converter.video import VideoConverter


def main():
    parser = argparse.ArgumentParser(
        description="Video converter with automatic output to 'converted' folder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Convert video format (output to converted/ folder)
    python convert_video.py input.mp4 --format webm

    # Extract audio from video
    python convert_video.py video.mp4 --action extract_audio --format wav

    # Compress video
    python convert_video.py video.mp4 --action compress --quality medium

    # Change resolution
    python convert_video.py video.mp4 --action change_resolution --resolution 1280x720
        """
    )

    parser.add_argument('input_video', help='Path to input video file')

    parser.add_argument('--action', choices=['convert', 'extract_audio', 'compress', 'change_resolution'],
                       default='convert', help='Action to perform (default: convert)')

    parser.add_argument('--format', help='Output format (e.g., mp4, webm, wav, mp3)')
    parser.add_argument('--quality', choices=['high', 'medium', 'low'], default='medium',
                       help='Compression quality (default: medium)')
    parser.add_argument('--resolution', help='Target resolution (e.g., 1920x1080, 1280x720)')

    args = parser.parse_args()

    # Validate input file exists
    input_file = Path(args.input_video)
    if not input_file.exists():
        print(f"❌ Error: Input file '{args.input_video}' not found")
        sys.exit(1)

    # Initialize converter
    converter = VideoConverter()

    print(f"🎬 Processing {args.input_video}...")
    print(f"📁 Input size: {input_file.stat().st_size / 1024 / 1024:.1f} MB")

    # Determine output path and format
    if args.action == 'convert':
        output_format = args.format or 'webm'  # Default to webm if not specified
        output_path = f"converted/{input_file.stem}.{output_format}"
        print(f"🎯 Converting to {output_format} format...")

    elif args.action == 'extract_audio':
        output_format = args.format or 'wav'
        output_path = f"converted/{input_file.stem}_audio.{output_format}"
        print(f"🎵 Extracting audio to {output_format}...")

    elif args.action == 'compress':
        output_path = f"converted/{input_file.stem}_compressed{input_file.suffix}"
        print(f"🗜️  Compressing with {args.quality} quality...")

    elif args.action == 'change_resolution':
        if not args.resolution:
            print("❌ Error: --resolution required for resolution change")
            sys.exit(1)
        output_path = f"converted/{input_file.stem}_{args.resolution}{input_file.suffix}"
        print(f"📐 Changing resolution to {args.resolution}...")

    # Create progress bar
    with tqdm(total=100, desc="Converting", unit="%", bar_format='{desc}: {percentage:3.0f}%|{bar}| {elapsed} elapsed') as pbar:
        start_time = time.time()

        # Perform the operation
        if args.action == 'convert':
            result = converter.convert_video_format(str(input_file), output_format, output_path)
        elif args.action == 'extract_audio':
            result = converter.extract_audio_from_video(str(input_file), output_format, output_path)
        elif args.action == 'compress':
            result = converter.compress_video(str(input_file), args.quality, output_path)
        elif args.action == 'change_resolution':
            result = converter.change_resolution(str(input_file), args.resolution, output_path)

        # Simulate progress (since we can't easily monitor FFmpeg progress)
        for i in range(10):
            time.sleep(0.1)
            pbar.update(10)

        pbar.update(100 - pbar.n)  # Complete the progress bar

    if result:
        output_file = Path(result)
        if output_file.exists():
            size_mb = output_file.stat().st_size / 1024 / 1024
            print(f"✅ Operation successful: {result}")
            print(f"📁 Output size: {size_mb:.1f} MB")
        else:
            print(f"✅ Operation completed: {result}")
        sys.exit(0)
    else:
        print("❌ Operation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()