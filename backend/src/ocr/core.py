"""
OCR core functionality using Microsoft TrOCR Large Model for handwritten text recognition.

This module provides text extraction from images using
the Microsoft TrOCR Large Handwritten model for highest accuracy on poor/unclear handwriting.
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any
import time
import os

try:
    from transformers import TrOCRProcessor, VisionEncoderDecoderModel
    from PIL import Image
    import torch
    import cv2
    import numpy as np
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    TrOCRProcessor = None
    VisionEncoderDecoderModel = None
    Image = None
    torch = None
    cv2 = None
    np = None


logger = logging.getLogger(__name__)


class OCREngine:
    """
    OCR Engine using Microsoft TrOCR Large Handwritten model for text extraction from images.

    This class provides high-accuracy OCR capabilities specifically optimized for
    handwritten text recognition, with focus on poor/unclear handwriting.
    """

    def __init__(self, model_name: str = "microsoft/trocr-large-handwritten", device: str = "auto"):
        """
        Initialize the OCR engine.

        Args:
            model_name: HuggingFace model name for TrOCR (default: microsoft/trocr-large-handwritten)
            device: Device to run the model on ('auto', 'cpu', 'cuda')
        """
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "transformers, PIL, torch, opencv-python, and numpy are required for OCR. "
                "Install with: pip install transformers pillow torch opencv-python numpy"
            )

        self.model_name = model_name
        self.device = device
        self.model = None
        self.processor = None
        self._initialized = False

    def _initialize_model(self):
        """Initialize the TrOCR Large Handwritten model and processor."""
        if self._initialized:
            return

        try:
            logger.info(f"Loading Microsoft TrOCR Large Handwritten model: {self.model_name}")

            # Determine device
            if self.device == "auto":
                self.device = "cuda" if torch.cuda.is_available() else "cpu"

            # Load the large handwritten model - best accuracy for poor handwriting
            # Use fast processor to suppress warnings and improve performance
            self.processor = TrOCRProcessor.from_pretrained(self.model_name, use_fast=True)
            self.model = VisionEncoderDecoderModel.from_pretrained(self.model_name)

            # Move to GPU if available for faster inference
            self.model = self.model.to(self.device)

            self._initialized = True
            logger.info(f"TrOCR Large Handwritten model loaded successfully on {self.device}")

        except Exception as e:
            logger.error(f"Failed to load TrOCR Large Handwritten model: {e}")
            # Try fallback to base model
            try:
                logger.info("Trying fallback to TrOCR Base Handwritten model...")
                self.processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten', use_fast=True)
                self.model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
                self.model = self.model.to(self.device)
                self._initialized = True
                logger.info(f"TrOCR Base Handwritten model loaded as fallback on {self.device}")
            except Exception as e2:
                logger.error(f"Failed to load any TrOCR model: {e2}")
                raise

    def _enhance_image_for_poor_handwriting(self, image_path: str):
        """
        Gentle preprocessing for handwriting - optimized for TrOCR.

        Args:
            image_path (str): Path to the image file

        Returns:
            tuple: (enhanced PIL.Image, original PIL.Image)
        """
        try:
            logger.info("Applying gentle preprocessing for handwriting...")

            # Load image
            image = cv2.imread(image_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Convert to grayscale for minimal preprocessing
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply gentle adaptive thresholding
            binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

            # Apply minimal Gaussian blur
            blurred = cv2.GaussianBlur(binary, (1, 1), 0)

            # Convert back to PIL Image with RGB channels
            pil_image = Image.fromarray(blurred).convert('RGB')

            logger.info("Gentle preprocessing completed")
            return pil_image, Image.fromarray(image_rgb)

        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            logger.info("Using original image...")
            return Image.open(image_path).convert('RGB'), Image.open(image_path).convert('RGB')

    def extract_text(self, image_path: str, ocr_type: str = "ocr") -> Dict[str, Any]:
        """
        Extract handwritten text from an image using TrOCR Large model with segmentation.

        Args:
            image_path: Path to the image file
            ocr_type: Type of OCR to perform (ignored, always uses handwritten segmentation)

        Returns:
            Dictionary containing extracted text and metadata
        """
        self._initialize_model()

        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")

        start_time = time.time()

        try:
            logger.info(f"Processing handwritten image: {image_path}")

            # Use segmented extraction approach (like the working original)
            extracted_text = self._extract_handwritten_text_segmented(str(image_path))

            processing_time = time.time() - start_time

            # Format result
            ocr_result = {
                "text": extracted_text,
                "image_path": str(image_path),
                "model": self.model_name,
                "processing_time": round(processing_time, 2),
                "device": self.device
            }

            logger.info(f"OCR completed in {processing_time:.2f}s")
            return ocr_result

        except Exception as e:
            logger.error(f"OCR processing failed: {e}")
            raise

    def _extract_handwritten_text_segmented(self, image_path: str) -> str:
        """
        Extract handwritten text using segmentation approach.

        Args:
            image_path (str): Path to the image file

        Returns:
            str: Combined extracted text from all segments
        """
        try:
            logger.info("Using segmented extraction approach for handwritten text...")

            # Load image
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Find contours to identify text regions
            binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Filter and sort contours by area
            text_contours = [c for c in contours if cv2.contourArea(c) > 100]
            text_contours = sorted(text_contours, key=lambda c: cv2.boundingRect(c)[1])  # Sort by y-coordinate

            segment_texts = []

            logger.info(f"Found {len(text_contours)} potential text regions")

            for i, contour in enumerate(text_contours):
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)

                # Skip very small regions
                if w < 50 or h < 20:
                    continue

                logger.debug(f"Processing segment {i+1}/{len(text_contours)} - Size: {w}x{h}")

                # Extract region
                roi = image[y:y+h, x:x+w]
                roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                roi_pil = Image.fromarray(roi_rgb)

                # Process with TrOCR Large model
                try:
                    pixel_values = self.processor(roi_pil, return_tensors="pt").pixel_values
                    pixel_values = pixel_values.to(self.device)

                    with torch.no_grad():
                        generated_ids = self.model.generate(pixel_values)

                    text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

                    if text.strip():
                        segment_texts.append(text.strip())
                        logger.debug(f"  ✓ Segment {i+1} text: {text.strip()}")
                    else:
                        logger.debug(f"  ✗ Segment {i+1}: No text detected")

                except Exception as e:
                    logger.error(f"  ✗ Error processing segment {i+1}: {str(e)}")
                    continue

            # Combine all segments
            combined_text = " ".join(segment_texts)

            logger.info(f"Segmented extraction completed! Found {len(segment_texts)} text segments")
            return combined_text

        except Exception as e:
            logger.error(f"Error in segmented extraction: {str(e)}")
            # Try full image extraction as fallback
            try:
                logger.info("Trying full image extraction as fallback...")
                enhanced_image, _ = self._enhance_image_for_poor_handwriting(image_path)

                pixel_values = self.processor(enhanced_image, return_tensors="pt").pixel_values
                pixel_values = pixel_values.to(self.device)

                with torch.no_grad():
                    generated_ids = self.model.generate(pixel_values)

                extracted_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
                extracted_text = extracted_text.strip()

                logger.info(f"Full image extraction result: {len(extracted_text)} characters")
                return extracted_text

            except Exception as e2:
                logger.error(f"Full image extraction also failed: {str(e2)}")
                return ""

    def extract_text_batch(self, image_paths: list, ocr_type: str = "ocr") -> list:
        """
        Extract text from multiple images.

        Args:
            image_paths: List of paths to image files
            ocr_type: Type of OCR to perform
            correct_typos: Whether to apply typo correction to extracted text

        Returns:
            List of OCR results for each image
        """
        results = []
        for image_path in image_paths:
            try:
                result = self.extract_text(image_path, ocr_type)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process {image_path}: {e}")
                results.append({
                    "text": "",
                    "image_path": str(image_path),
                    "error": str(e),
                    "model": self.model_name
                })

        return results

    def __del__(self):
        """Cleanup resources."""
        if hasattr(self, 'model') and self.model is not None:
            del self.model
        if hasattr(self, 'processor') and self.processor is not None:
            del self.processor