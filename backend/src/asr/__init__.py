"""
ASR (Automatic Speech Recognition) module for Media Processing Studio.

This module provides speech-to-text transcription capabilities with word-level
timestamps using WhisperX, supporting multiple languages and high accuracy.
"""

from .core import AudioTranscriber

__all__ = ['AudioTranscriber']