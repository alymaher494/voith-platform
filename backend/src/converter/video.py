"""
Video conversion utilities.

This module provides functionality for converting between different video formats
and performing video processing operations using FFmpeg.
"""
import logging
import subprocess
import os
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

logger = logging.getLogger(__name__)


class VideoConverter:
    """
    Video format converter using FFmpeg.

    Provides methods for converting between various video formats with
    customizable quality settings, resolution changes, and compression options.
    """

    def __init__(self, output_dir: str = './converted'):
        """
        Initialize the video converter.

        Args:
            output_dir (str): Directory where converted files will be saved
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _run_ffmpeg(self, input_file: str, output_file: str, ffmpeg_args: list) -> bool:
        """
        Run FFmpeg command with the specified arguments.

        Args:
            input_file (str): Input file path
            output_file (str): Output file path
            ffmpeg_args (list): Additional FFmpeg arguments

        Returns:
            bool: True if conversion successful, False otherwise
        """
        cmd = ['ffmpeg', '-i', input_file] + ffmpeg_args + ['-y', output_file]

        try:
            logger.info(f"Running FFmpeg command: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            logger.info("FFmpeg conversion completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg conversion failed: {e.stderr}")
            return False
        except FileNotFoundError:
            logger.error("FFmpeg not found. Please install FFmpeg.")
            return False

    def convert_video_format(self, input_file: str, output_format: str,
                           output_file: Optional[str] = None, **kwargs) -> Optional[str]:
        """
        Convert video file to specified format.

        Args:
            input_file (str): Path to input video file
            output_format (str): Target format (e.g., 'mp4', 'avi', 'mkv', 'webm')
            output_file (Optional[str]): Path for output file. If None, auto-generated.
            **kwargs: Additional conversion options (resolution, bitrate, etc.)

        Returns:
            Optional[str]: Path to converted file, or None if conversion failed
        """
        input_path = Path(input_file)
        if not input_path.exists():
            logger.error(f"Input file does not exist: {input_file}")
            return None

        if output_file:
            output_path = Path(output_file)
        else:
            output_path = self.output_dir / f"{input_path.stem}.{output_format}"

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Get format-specific FFmpeg arguments
        format_args = self._get_video_format_args(output_format, **kwargs)

        success = self._run_ffmpeg(str(input_path), str(output_path), format_args)

        return str(output_path) if success else None

    def change_resolution(self, input_file: str, resolution: str,
                         output_file: Optional[str] = None) -> Optional[str]:
        """
        Change video resolution.

        Args:
            input_file (str): Path to input video file
            resolution (str): Target resolution (e.g., '1920x1080', '1280x720', '854x480')
            output_file (Optional[str]): Path for output file. If None, auto-generated.

        Returns:
            Optional[str]: Path to resized video, or None if conversion failed
        """
        input_path = Path(input_file)
        if not input_path.exists():
            logger.error(f"Input file does not exist: {input_file}")
            return None

        if output_file:
            output_path = Path(output_file)
        else:
            output_path = self.output_dir / f"{input_path.stem}_{resolution}{input_path.suffix}"

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # FFmpeg arguments for resolution change
        ffmpeg_args = [
            '-vf', f'scale={resolution}',
            '-c:v', 'libx264',  # Re-encode video
            '-preset', 'medium',
            '-crf', '23'
        ]

        success = self._run_ffmpeg(str(input_path), str(output_path), ffmpeg_args)

        return str(output_path) if success else None

    def extract_audio_from_video(self, input_file: str, audio_format: str = 'mp3',
                               output_file: Optional[str] = None) -> Optional[str]:
        """
        Extract audio track from video file.

        Args:
            input_file (str): Path to input video file
            audio_format (str): Audio format ('mp3', 'wav', 'aac', etc.)
            output_file (Optional[str]): Path for output audio file. If None, auto-generated.

        Returns:
            Optional[str]: Path to extracted audio file, or None if extraction failed
        """
        input_path = Path(input_file)
        if not input_path.exists():
            logger.error(f"Input file does not exist: {input_file}")
            return None

        if output_file:
            output_path = Path(output_file)
        else:
            output_path = self.output_dir / f"{input_path.stem}_audio.{audio_format}"

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # FFmpeg arguments for audio extraction
        ffmpeg_args = []

        if audio_format.lower() == 'mp3':
            ffmpeg_args.extend([
                '-vn',  # No video
                '-acodec', 'libmp3lame',
                '-ab', '192k',
                '-ar', '44100'
            ])
        elif audio_format.lower() == 'wav':
            ffmpeg_args.extend([
                '-vn',  # No video
                '-acodec', 'pcm_s16le'
            ])
        elif audio_format.lower() == 'aac':
            ffmpeg_args.extend([
                '-vn',  # No video
                '-acodec', 'aac',
                '-ab', '128k'
            ])

        success = self._run_ffmpeg(str(input_path), str(output_path), ffmpeg_args)

        return str(output_path) if success else None

    def compress_video(self, input_file: str, quality: str = 'medium',
                      output_file: Optional[str] = None) -> Optional[str]:
        """
        Compress video file to reduce file size.

        Args:
            input_file (str): Path to input video file
            quality (str): Compression quality ('high', 'medium', 'low')
            output_file (Optional[str]): Path for output file. If None, auto-generated.

        Returns:
            Optional[str]: Path to compressed video, or None if compression failed
        """
        input_path = Path(input_file)
        if not input_path.exists():
            logger.error(f"Input file does not exist: {input_file}")
            return None

        if output_file:
            output_path = Path(output_file)
        else:
            output_path = self.output_dir / f"{input_path.stem}_compressed{input_path.suffix}"

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Quality settings
        quality_settings = {
            'high': {'crf': '18', 'preset': 'slow'},
            'medium': {'crf': '23', 'preset': 'medium'},
            'low': {'crf': '28', 'preset': 'fast'}
        }

        settings = quality_settings.get(quality, quality_settings['medium'])

        # FFmpeg arguments for compression
        ffmpeg_args = [
            '-c:v', 'libx264',
            '-preset', settings['preset'],
            '-crf', settings['crf'],
            '-c:a', 'aac',
            '-b:a', '128k'
        ]

        success = self._run_ffmpeg(str(input_path), str(output_path), ffmpeg_args)

        return str(output_path) if success else None

    def _get_video_format_args(self, output_format: str, **kwargs) -> list:
        """
        Get FFmpeg arguments for specific video format.

        Args:
            output_format (str): Target video format
            **kwargs: Additional format options

        Returns:
            list: FFmpeg arguments for the format
        """
        format_args = []

        if output_format.lower() == 'mp4':
            format_args.extend([
                '-c:v', 'libx264',
                '-preset', kwargs.get('preset', 'medium'),
                '-crf', str(kwargs.get('crf', 23)),
                '-c:a', 'aac',
                '-b:a', kwargs.get('audio_bitrate', '128k')
            ])
        elif output_format.lower() == 'webm':
            format_args.extend([
                '-c:v', 'libvpx-vp9',
                '-crf', str(kwargs.get('crf', 30)),
                '-b:v', '0',
                '-c:a', 'libopus',
                '-b:a', kwargs.get('audio_bitrate', '128k')
            ])
        elif output_format.lower() == 'avi':
            format_args.extend([
                '-c:v', 'libx264',
                '-c:a', 'mp3',
                '-b:a', kwargs.get('audio_bitrate', '128k')
            ])
        elif output_format.lower() == 'mkv':
            format_args.extend([
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-b:a', kwargs.get('audio_bitrate', '128k')
            ])
        else:
            # Default settings for other formats
            logger.warning(f"Using default settings for format: {output_format}")
            format_args.extend([
                '-c:v', 'libx264',
                '-c:a', 'aac'
            ])

        return format_args

    def get_video_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Get video file information using FFmpeg.

        Args:
            file_path (str): Path to video file

        Returns:
            Optional[Dict[str, Any]]: Video file information, or None if failed
        """
        if not Path(file_path).exists():
            logger.error(f"File does not exist: {file_path}")
            return None

        try:
            cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            import json
            info = json.loads(result.stdout)
            return info

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get video info: {e.stderr}")
            return None
        except FileNotFoundError:
            logger.error("ffprobe not found. Please install FFmpeg.")
            return None
        except json.JSONDecodeError:
            logger.error("Failed to parse ffprobe output")
            return None