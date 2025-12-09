"""
OCR (Optical Character Recognition) module for Media Processing Studio.

This module provides text extraction capabilities from images and documents
using state-of-the-art OCR models like GOT-OCR2.0.
"""

from .core import OCREngine

__all__ = ['OCREngine']