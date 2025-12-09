"""
Unit tests for summarizer functionality.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.summarizer import ContentProcessor


class TestContentProcessor(unittest.TestCase):
    """Test cases for ContentProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.processor = ContentProcessor()

    @patch('src.summarizer.MT5ForConditionalGeneration')
    @patch('src.summarizer.MT5Tokenizer')
    def test_initialization(self, mock_tokenizer, mock_model):
        """Test processor initialization."""
        mock_tokenizer.from_pretrained.return_value = MagicMock()
        mock_model.from_pretrained.return_value = MagicMock()

        processor = ContentProcessor()
        self.assertIsInstance(processor, ContentProcessor)
        self.assertEqual(processor.model_name, "google/mt5-small")

    @patch('src.summarizer.MT5ForConditionalGeneration')
    @patch('src.summarizer.MT5Tokenizer')
    def test_summarize_success(self, mock_tokenizer, mock_model):
        """Test successful summarization."""
        # Mock tokenizer and model
        mock_tokenizer_instance = MagicMock()
        mock_model_instance = MagicMock()
        mock_tokenizer.from_pretrained.return_value = mock_tokenizer_instance
        mock_model.from_pretrained.return_value = mock_model_instance

        # Mock tokenization and generation
        mock_tokenizer_instance.return_value = {"input_ids": [[1, 2, 3]]}
        mock_model_instance.generate.return_value = [[4, 5, 6]]
        mock_tokenizer_instance.decode.return_value = "Summarized text"

        processor = ContentProcessor()
        result = processor.summarize("This is a long text to summarize.")

        self.assertEqual(result, "Summarized text")
        mock_tokenizer_instance.assert_called()
        mock_model_instance.generate.assert_called()

    @patch('src.summarizer.MT5ForConditionalGeneration')
    @patch('src.summarizer.MT5Tokenizer')
    def test_summarize_failure(self, mock_tokenizer, mock_model):
        """Test summarization failure handling."""
        mock_tokenizer.from_pretrained.side_effect = Exception("Model load failed")

        processor = ContentProcessor()
        result = processor.summarize("Test text")

        self.assertIsNone(result)

    @patch('src.summarizer.MT5ForConditionalGeneration')
    @patch('src.summarizer.MT5Tokenizer')
    def test_answer_question_success(self, mock_tokenizer, mock_model):
        """Test successful Q&A."""
        # Mock tokenizer and model
        mock_tokenizer_instance = MagicMock()
        mock_model_instance = MagicMock()
        mock_tokenizer.from_pretrained.return_value = mock_tokenizer_instance
        mock_model.from_pretrained.return_value = mock_model_instance

        # Mock tokenization and generation
        mock_tokenizer_instance.return_value = {"input_ids": [[1, 2, 3]]}
        mock_model_instance.generate.return_value = [[4, 5, 6]]
        mock_tokenizer_instance.decode.return_value = "The answer is 42"

        processor = ContentProcessor()
        result = processor.answer_question("What is the answer?", "The answer is 42.")

        self.assertEqual(result, "The answer is 42")
        mock_tokenizer_instance.assert_called()
        mock_model_instance.generate.assert_called()

    @patch('src.summarizer.MT5ForConditionalGeneration')
    @patch('src.summarizer.MT5Tokenizer')
    def test_answer_question_failure(self, mock_tokenizer, mock_model):
        """Test Q&A failure handling."""
        mock_tokenizer.from_pretrained.side_effect = Exception("Model load failed")

        processor = ContentProcessor()
        result = processor.answer_question("Question?", "Context")

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()