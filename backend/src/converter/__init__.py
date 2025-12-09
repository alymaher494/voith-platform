"""
Audio and video converter library.

This package provides functionality for converting between different audio and video
formats using FFmpeg as the underlying conversion engine.
"""

from .audio import AudioConverter
from .video import VideoConverter

__version__ = "1.0.0"
__all__ = [
    'AudioConverter',
    'VideoConverter'
]