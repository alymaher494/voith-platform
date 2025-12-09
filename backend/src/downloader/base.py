"""
Base downloader class for all platform downloaders.

This abstract base class provides common functionality and interface for all video
downloaders in the system. It handles progress tracking, output directory management,
and resource cleanup through context manager support.
"""
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from tqdm import tqdm

logger = logging.getLogger(__name__)


class BaseDownloader(ABC):
    """
    Abstract base class for all platform-specific video downloaders.

    This class defines the interface that all downloaders must implement and provides
    common functionality like progress tracking and resource management.
    """

    def __init__(self, output_dir='./downloads'):
        """
        Initialize the base downloader with output directory setup.

        Args:
            output_dir (str): Directory path where downloaded files will be saved.
                            Defaults to './downloads'. Will be created if it doesn't exist.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.pbar = None  # Progress bar instance for download visualization

        # Future expansion: Add configuration options
        # self.config = {}  # For storing downloader-specific settings
        # self.retry_count = 3  # For implementing retry logic
        # self.timeout = 300  # Download timeout in seconds

    @abstractmethod
    def validate_url(self, url):
        """
        Validate if the URL is supported by this downloader.

        This method should implement platform-specific URL validation logic.

        Args:
            url (str): The URL to validate

        Returns:
            bool: True if the URL is valid and supported by this downloader,
                  False otherwise
        """
        pass

    @abstractmethod
    def download(self, url, **kwargs):
        """
        Download content from the given URL.

        This is the main download method that subclasses must implement with
        platform-specific download logic.

        Args:
            url (str): The URL to download content from
            **kwargs: Additional platform-specific options such as:
                     - start_time: Start time for video slicing (int seconds)
                     - end_time: End time for video slicing (int seconds)
                     - audio_only: Extract audio only (bool)
                     - format_id: Specific format ID to download (str)

        Returns:
            dict: Download result containing:
                 - 'output_dir': Output directory path
                 - 'platform': Detected platform name
                 - 'platform_info': Platform metadata
                 - 'success': Download success status
        """
        pass

    def progress_hook(self, d):
        """
        Handle download progress updates from yt-dlp.

        This method creates and updates a progress bar during downloads,
        providing real-time feedback on download progress.

        Args:
            d (dict): Progress information dictionary from yt-dlp containing:
                     - 'status': Current download status
                     - 'total_bytes': Total file size in bytes
                     - 'total_bytes_estimate': Estimated total size
                     - 'downloaded_bytes': Bytes downloaded so far
        """
        if d['status'] == 'downloading':
            # Get total size (prefer exact over estimate)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)

            if total > 0:
                # Create or recreate progress bar if total size changed
                if self.pbar is None or self.pbar.total != total:
                    if self.pbar:
                        self.pbar.close()
                    self.pbar = tqdm(
                        total=total,
                        unit='B',
                        unit_scale=True,
                        desc="Downloading",
                        bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
                    )
                self.pbar.n = downloaded
                self.pbar.refresh()

        elif d['status'] == 'finished':
            # Clean up progress bar on completion
            if self.pbar:
                self.pbar.close()
                self.pbar = None
            logger.info("Download completed!")

    def cleanup(self):
        """
        Clean up resources and close progress bars.

        This method ensures proper cleanup of progress bars and other resources
        when the downloader is finished or encounters an error.
        """
        if self.pbar:
            self.pbar.close()
            self.pbar = None

    def __enter__(self):
        """
        Context manager entry point.

        Returns:
            BaseDownloader: Self instance for use in with statements
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point with automatic cleanup.

        Ensures resources are properly cleaned up even if an exception occurs
        during the download process.

        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        self.cleanup()
