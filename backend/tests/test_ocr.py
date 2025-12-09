"""
Tests for OCR functionality using Microsoft TrOCR Large Handwritten model.
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to sys.path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ocr.core import OCREngine


class TestOCREngine:
    """Test cases for OCREngine class."""

    @patch('src.ocr.core.TrOCRProcessor')
    @patch('src.ocr.core.VisionEncoderDecoderModel')
    @patch('src.ocr.core.Image')
    def test_initialization(self, mock_image, mock_processor, mock_model):
        """Test OCR engine initialization."""
        mock_model.from_pretrained.return_value = MagicMock()
        mock_processor.from_pretrained.return_value = MagicMock()

        engine = OCREngine()
        assert engine.model_name == "microsoft/trocr-large-handwritten"
        assert engine.device == "auto"  # Default device setting

    @patch('src.ocr.core.TrOCRProcessor')
    @patch('src.ocr.core.VisionEncoderDecoderModel')
    @patch('src.ocr.core.Image')
    def test_extract_text_success(self, mock_image, mock_processor, mock_model):
        """Test successful text extraction."""
        # Mock the model and processor
        mock_model_instance = MagicMock()
        mock_model.from_pretrained.return_value = mock_model_instance
        mock_processor_instance = MagicMock()
        mock_processor.from_pretrained.return_value = mock_processor_instance

        # Mock the generate method to return token IDs
        mock_model_instance.generate.return_value = [[1, 2, 3]]
        mock_processor_instance.batch_decode.return_value = ["Extracted text from image"]

        # Mock cv2 for image processing
        with patch('src.ocr.core.cv2') as mock_cv2:
            mock_cv2.imread.return_value = None  # Simulate empty image for fallback
            mock_cv2.cvtColor.side_effect = Exception("OpenCV error")

        # Mock PIL Image
        mock_image_instance = MagicMock()
        mock_image.open.return_value.convert.return_value = mock_image_instance

        # Create a temporary test image file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(b'fake image data')
            temp_path = temp_file.name

        try:
            engine = OCREngine()
            result = engine.extract_text(temp_path)

            assert result['text'] == "Extracted text from image"
            assert result['model'] == "microsoft/trocr-large-handwritten"
            assert result['device'] == "cpu"
            assert 'processing_time' in result
            assert isinstance(result['processing_time'], float)

        finally:
            # Clean up
            Path(temp_path).unlink(missing_ok=True)

    @patch('src.ocr.core.TrOCRProcessor')
    @patch('src.ocr.core.VisionEncoderDecoderModel')
    @patch('src.ocr.core.Image')
    def test_extract_text_file_not_found(self, mock_image, mock_processor, mock_model):
        """Test handling of non-existent image file."""
        mock_model.from_pretrained.return_value = MagicMock()
        mock_processor.from_pretrained.return_value = MagicMock()

        engine = OCREngine()

        with pytest.raises(FileNotFoundError):
            engine.extract_text("nonexistent_image.jpg")

    @patch('src.ocr.core.TrOCRProcessor')
    @patch('src.ocr.core.VisionEncoderDecoderModel')
    @patch('src.ocr.core.Image')
    def test_batch_processing(self, mock_image, mock_processor, mock_model):
        """Test batch text extraction."""
        # Mock the model and processor
        mock_model_instance = MagicMock()
        mock_model.from_pretrained.return_value = mock_model_instance
        mock_processor_instance = MagicMock()
        mock_processor.from_pretrained.return_value = mock_processor_instance

        # Mock the generate method to return different text for each call
        mock_model_instance.generate.side_effect = [[1, 2, 3], [4, 5, 6]]
        mock_processor_instance.batch_decode.side_effect = ["Text 1", "Text 2"]

        # Mock cv2 for image processing
        with patch('src.ocr.core.cv2') as mock_cv2:
            mock_cv2.imread.return_value = None  # Simulate empty image for fallback
            mock_cv2.cvtColor.side_effect = Exception("OpenCV error")

        # Mock PIL Image
        mock_image_instance = MagicMock()
        mock_image.open.return_value.convert.return_value = mock_image_instance

        # Create temporary test files
        import tempfile
        temp_files = []
        for i in range(2):
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_file.write(f'fake image data {i}'.encode())
                temp_files.append(temp_file.name)

        try:
            engine = OCREngine()
            results = engine.extract_text_batch(temp_files)

            assert len(results) == 2
            assert results[0]['text'] == "Text 1"
            assert results[1]['text'] == "Text 2"

        finally:
            # Clean up
            for temp_file in temp_files:
                Path(temp_file).unlink(missing_ok=True)


class TestOCRCLI:
    """Test cases for OCR CLI functionality."""

    def test_cli_help(self):
        """Test CLI help output."""
        import subprocess
        result = subprocess.run(
            [sys.executable, 'ocr_image.py', '--help'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode == 0
        assert "Extract handwritten text from images using Microsoft TrOCR Large model" in result.stdout

    def test_cli_invalid_file(self):
        """Test CLI with invalid file."""
        import subprocess
        result = subprocess.run(
            [sys.executable, 'ocr_image.py', 'nonexistent.jpg'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode == 1
        assert "Invalid file" in result.stderr


if __name__ == "__main__":
    pytest.main([__file__])