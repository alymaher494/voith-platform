"""
Multi-platform video downloader package.

This package provides a unified interface for downloading videos from various platforms
using yt-dlp as the underlying extraction engine.
"""

from .base import BaseDownloader
from .generic import GenericDownloader
from .utils import parse_time, validate_time_range

__version__ = "1.1.0"

# Core downloader classes
__all__ = [
    'BaseDownloader',      # Abstract base class for all downloaders
    'GenericDownloader',   # Universal downloader using yt-dlp
    'parse_time',          # Time string parsing utility
    'validate_time_range'  # Time range validation utility
]

# Future expansion: Add specialized downloaders here
# __all__.extend(['YouTubeDownloader', 'InstagramDownloader', ...])
