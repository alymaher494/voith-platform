"""
Audio conversion utilities.

This module provides functionality for converting between different audio formats
using FFmpeg as the underlying conversion engine.
"""
import logging
import subprocess
import os
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class AudioConverter:
    """
    Audio format converter using FFmpeg.

    Provides methods for converting between various audio formats with
    customizable quality settings and metadata preservation.
    """

    def __init__(self, output_dir: str = './converted'):
        """
        Initialize the audio converter.

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

    def convert_mp3_to_wav(self, input_file: str, output_file: Optional[str] = None) -> Optional[str]:
        """
        Convert MP3 file to WAV format.

        Args:
            input_file (str): Path to input MP3 file
            output_file (Optional[str]): Path for output WAV file. If None, auto-generated.

        Returns:
            Optional[str]: Path to converted WAV file, or None if conversion failed
        """
        input_path = Path(input_file)
        if not input_path.exists():
            logger.error(f"Input file does not exist: {input_file}")
            return None

        if output_file:
            output_path = Path(output_file)
        else:
            output_path = self.output_dir / f"{input_path.stem}.wav"

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # FFmpeg arguments for MP3 to WAV conversion
        ffmpeg_args = []

        success = self._run_ffmpeg(str(input_path), str(output_path), ffmpeg_args)

        return str(output_path) if success else None

    def convert_wav_to_mp3(self, input_file: str, bitrate: str = '192k', output_file: Optional[str] = None) -> Optional[str]:
        """
        Convert WAV file to MP3 format.

        Args:
            input_file (str): Path to input WAV file
            bitrate (str): Target bitrate (e.g., '128k', '192k', '320k')
            output_file (Optional[str]): Path for output MP3 file. If None, auto-generated.

        Returns:
            Optional[str]: Path to converted MP3 file, or None if conversion failed
        """
        input_path = Path(input_file)
        if not input_path.exists():
            logger.error(f"Input file does not exist: {input_file}")
            return None

        if output_file:
            output_path = Path(output_file)
        else:
            output_path = self.output_dir / f"{input_path.stem}.mp3"

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # FFmpeg arguments for WAV to MP3 conversion
        ffmpeg_args = [
            '-acodec', 'libmp3lame',
            '-ab', bitrate,
            '-ar', '44100'  # Sample rate
        ]

        success = self._run_ffmpeg(str(input_path), str(output_path), ffmpeg_args)

        return str(output_path) if success else None

    def convert_audio_format(self, input_file: str, output_format: str, output_file: Optional[str] = None, **kwargs) -> Optional[str]:
        """
        Convert audio file to specified format.

        Args:
            input_file (str): Path to input audio file
            output_format (str): Target format (e.g., 'mp3', 'wav', 'flac', 'aac')
            output_file (Optional[str]): Path for output file. If None, auto-generated.
            **kwargs: Additional format-specific options

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

        # Format-specific FFmpeg arguments
        format_args = self._get_format_args(output_format, **kwargs)

        success = self._run_ffmpeg(str(input_path), str(output_path), format_args)

        return str(output_path) if success else None

    def _get_format_args(self, output_format: str, **kwargs) -> list:
        """
        Get FFmpeg arguments for specific audio format.

        Args:
            output_format (str): Target audio format
            **kwargs: Additional format options

        Returns:
            list: FFmpeg arguments for the format
        """
        format_args = []

        if output_format.lower() == 'mp3':
            format_args.extend([
                '-acodec', 'libmp3lame',
                '-ab', kwargs.get('bitrate', '192k'),
                '-ar', str(kwargs.get('sample_rate', 44100))
            ])
        elif output_format.lower() == 'aac':
            format_args.extend([
                '-acodec', 'aac',
                '-ab', kwargs.get('bitrate', '128k'),
                '-ar', str(kwargs.get('sample_rate', 44100))
            ])
        elif output_format.lower() == 'flac':
            format_args.extend([
                '-acodec', 'flac'
            ])
        elif output_format.lower() == 'wav':
            # WAV is essentially uncompressed
            format_args.extend([
                '-acodec', 'pcm_s16le'
            ])
        else:
            # Default settings for other formats
            logger.warning(f"Using default settings for format: {output_format}")

        return format_args

    def get_audio_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Get audio file information using FFmpeg.

        Args:
            file_path (str): Path to audio file

        Returns:
            Optional[Dict[str, Any]]: Audio file information, or None if failed
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
            logger.error(f"Failed to get audio info: {e.stderr}")
            return None
        except FileNotFoundError:
            logger.error("ffprobe not found. Please install FFmpeg.")
            return None
        except json.JSONDecodeError:
            logger.error("Failed to parse ffprobe output")
            return None