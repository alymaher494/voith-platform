"""
Universal video downloader using yt-dlp.

This module provides a generic downloader that can handle videos from any platform
supported by yt-dlp, including YouTube, Vimeo, TikTok, Instagram, and hundreds more.
"""
import re
import logging
import yt_dlp
from .base import BaseDownloader

logger = logging.getLogger(__name__)


class GenericDownloader(BaseDownloader):
    """
    Universal video downloader supporting all yt-dlp compatible platforms.

    This downloader uses yt-dlp's extensive platform support to download videos
    from any website that hosts video content. It automatically detects the platform
    and applies the appropriate extraction method.
    """

    def __init__(self, output_dir='./downloads'):
        """
        Initialize the generic downloader.

        Args:
            output_dir (str): Directory where downloaded files will be saved
        """
        super().__init__(output_dir)
        self.platform_name = "Generic"
        self.detected_platform = None  # Will be set during download

        # Future expansion hooks for enhanced functionality
        # self.max_retries = 3  # Retry failed downloads
        # self.timeout = 300  # Download timeout in seconds
        # self.proxy_settings = None  # Proxy configuration
        # self.cookies_file = None  # Cookies for authenticated sites
        # self.user_agent = None  # Custom user agent string

    def validate_url(self, url: str) -> bool:
        """
        Validate that the provided URL is a valid HTTP/HTTPS URL.

        This is a basic validation that checks for proper URL format.
        The actual platform compatibility is determined during download.

        Args:
            url (str): The URL to validate

        Returns:
            bool: True if URL format is valid, False otherwise
        """
        url_pattern = r'^https?://.+'
        return bool(re.match(url_pattern, url))

    def get_platform_info(self, url: str) -> dict:
        """
        Extract platform and video information from URL using yt-dlp.

        This method queries yt-dlp to determine the video platform and extract
        metadata without downloading the actual content.

        Args:
            url (str): Video URL to analyze

        Returns:
            dict: Platform information containing:
                - platform: Platform identifier (e.g., 'youtube', 'vimeo')
                - platform_name: Human-readable platform name
                - title: Video title
                - duration: Video duration in seconds
                - uploader: Content uploader/channel name
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'platform': info.get('extractor_key', 'Unknown'),
                    'platform_name': info.get('extractor', 'Unknown'),
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                }
        except Exception as e:
            logger.error(f"Failed to extract platform info: {str(e)}")
            return {
                'platform': 'Unknown',
                'platform_name': 'Unknown',
                'title': 'Unknown',
                'duration': 0,
                'uploader': 'Unknown',
            }

    def get_available_resolutions(self, url: str) -> list:
        """
        Retrieve all available video/audio formats for a given URL.

        This method queries yt-dlp to get comprehensive format information
        including resolutions, file types, and quality options available
        for the specified video.

        Args:
            url (str): Video URL to query for available formats

        Returns:
            list: List of format dictionaries, each containing:
                - format_id: Unique format identifier
                - ext: File extension (mp4, webm, etc.)
                - resolution: Video resolution (e.g., '720p') or 'audio'
                - note: Additional format information/notes
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = []

                for f in info.get('formats', []):
                    height = f.get('height')

                    # Determine if this is an audio-only format
                    if not height and f.get('acodec') != 'none':
                        resolution = 'audio'
                    else:
                        # Format resolution as "720p" for video formats
                        resolution = f"{height}p" if isinstance(height, int) else str(height)

                    formats.append({
                        'format_id': f.get('format_id'),
                        'ext': f.get('ext'),
                        'resolution': resolution,
                        'note': f.get('format_note', '')
                    })

                return formats

        except Exception as e:
            logger.error(f"Failed to get available resolutions: {str(e)}")
            return []

    def download(self,
                 url: str,
                 start_time: int = None,
                 end_time: int = None,
                 audio_only: bool = False,
                 format_id: str = None,
                 **kwargs) -> dict:
        """
        Download video from any yt-dlp supported platform.

        This is the main download method that handles the complete download workflow
        including platform detection, format selection, audio extraction, and time slicing.

        Args:
            url (str): Video URL to download
            start_time (int, optional): Start time in seconds for video slicing
            end_time (int, optional): End time in seconds for video slicing
            audio_only (bool): If True, extract audio as MP3 instead of video
            format_id (str, optional): Specific format ID to download
            **kwargs: Additional options (reserved for future extensions)

        Returns:
            dict: Download result containing:
                - output_dir: Directory where files were saved
                - platform: Detected platform identifier
                - platform_info: Metadata about the video/platform
                - success: Boolean indicating successful completion

        Raises:
            ValueError: If URL format is invalid
            yt_dlp.utils.DownloadError: If download fails due to yt-dlp issues
            Exception: For other unexpected errors
        """
        # Validate input URL
        if not self.validate_url(url):
            raise ValueError("Invalid URL format. Please provide a valid HTTP/HTTPS URL.")

        # Detect platform and get video information
        logger.info("🔍 Detecting platform and gathering video information...")
        platform_info = self.get_platform_info(url)
        self.detected_platform = platform_info['platform']
        logger.info(f"📺 Detected platform: {self.detected_platform}")
        logger.info(f"🎬 Starting download: {url}")

        # Configure download format based on user preferences
        if format_id:
            # Merge specific video format with best available audio
            ydl_format = f"{format_id}+bestaudio/best"
            logger.info(f"🎯 Using specific format: {format_id}")
        else:
            # Auto-select best format based on audio_only preference
            ydl_format = "bestaudio/best" if audio_only else "best"
            logger.info(f"🎯 Using format strategy: {ydl_format}")

        # Base yt-dlp configuration
        ydl_opts = {
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'no_warnings': True,
            'format': ydl_format,
        }

        # Configure audio extraction if requested
        if audio_only:
            logger.info("🎵 Audio extraction enabled - will convert to MP3")
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        # Configure time slicing if both start and end times provided
        if start_time is not None and end_time is not None:
            logger.info(f"✂️ Time slicing enabled: {start_time}s to {end_time}s")
            ydl_opts['postprocessor_args'] = [
                '-ss', str(start_time),
                '-to', str(end_time),
            ]

        # Execute download with proper error handling
        try:
            logger.info("🚀 Beginning download process...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            logger.info(f"✅ Files saved to: {self.output_dir}")
            return {
                'output_dir': str(self.output_dir),
                'platform': self.detected_platform,
                'platform_info': platform_info,
                'success': True,
            }

        except yt_dlp.utils.DownloadError as e:
            logger.error(f"❌ yt-dlp download failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"❌ Unexpected error during download: {str(e)}")
            raise
        finally:
            # Ensure cleanup happens regardless of success/failure
            self.cleanup()
