"""
Unit tests for translation functionality.
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.translation import TextTranslator


class TestTextTranslator(unittest.TestCase):
    """Test cases for TextTranslator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.translator = TextTranslator()

    def test_initialization(self):
        """Test translator initialization."""
        self.assertIsInstance(self.translator, TextTranslator)
        self.assertIsNotNone(self.translator._nllb_tokenizer)
        self.assertIsNotNone(self.translator._nllb_model)
        self.assertFalse(self.translator._nllb_loaded)

    @patch('src.translation.GoogleTranslator')
    def test_translate_google_short_text(self, mock_google):
        """Test Google Translate for short text."""
        mock_instance = MagicMock()
        mock_instance.translate.return_value = "Hola mundo"
        mock_google.return_value = mock_instance

        result = self.translator._translate_google("Hello world", "es")
        self.assertEqual(result, "Hola mundo")
        mock_google.assert_called_once_with(target="es")
        mock_instance.translate.assert_called_once_with("Hello world")

    @patch('src.translation.GoogleTranslator')
    def test_translate_google_long_text_truncation(self, mock_google):
        """Test Google Translate truncates long text."""
        long_text = "A" * 6000  # Longer than 5000 chars
        truncated_text = "A" * 5000

        mock_instance = MagicMock()
        mock_instance.translate.return_value = "Translated text"
        mock_google.return_value = mock_instance

        result = self.translator._translate_google(long_text, "es")
        self.assertEqual(result, "Translated text")
        mock_instance.translate.assert_called_once_with(truncated_text)

    @patch('src.translation.GoogleTranslator')
    def test_translate_google_failure(self, mock_google):
        """Test Google Translate handles failures gracefully."""
        mock_google.side_effect = Exception("API Error")

        result = self.translator._translate_google("Hello", "es")
        self.assertIsNone(result)

    def test_should_use_context_short_text(self):
        """Test context detection for short text."""
        short_text = "Hello world"
        self.assertFalse(self.translator._should_use_context(short_text))

    def test_should_use_context_long_text(self):
        """Test context detection for long text."""
        long_text = "A" * 5000  # Longer than 4000 chars
        self.assertTrue(self.translator._should_use_context(long_text))

    def test_translate_text_auto_context_short(self):
        """Test automatic context selection for short text uses Google."""
        with patch.object(self.translator, '_translate_google') as mock_google:
            mock_google.return_value = "Hola"

            result = self.translator.translate_text("Hello", "es")
            mock_google.assert_called_once_with("Hello", "es")
            self.assertEqual(result, "Hola")

    def test_translate_text_auto_context_long(self):
        """Test automatic context selection for long text uses NLLB."""
        long_text = "A" * 5000

        with patch.object(self.translator, '_translate_nllb') as mock_nllb:
            mock_nllb.return_value = "Translated long text"

            result = self.translator.translate_text(long_text, "es")
            mock_nllb.assert_called_once_with(long_text, "es")
            self.assertEqual(result, "Translated long text")

    def test_translate_text_explicit_context_true(self):
        """Test explicit context flag overrides auto-detection."""
        short_text = "Hello"

        with patch.object(self.translator, '_translate_nllb') as mock_nllb:
            mock_nllb.return_value = "Contextual translation"

            result = self.translator.translate_text(short_text, "es", context=True)
            mock_nllb.assert_called_once_with(short_text, "es")
            self.assertEqual(result, "Contextual translation")

    def test_translate_text_explicit_context_false(self):
        """Test explicit context=False uses Google even for long text."""
        long_text = "A" * 5000

        with patch.object(self.translator, '_translate_google') as mock_google:
            mock_google.return_value = "Google translation"

            result = self.translator.translate_text(long_text, "es", context=False)
            mock_google.assert_called_once_with(long_text, "es")
            self.assertEqual(result, "Google translation")

    def test_detect_language_success(self):
        """Test successful language detection."""
        with patch('src.translation.detect') as mock_detect:
            mock_detect.return_value = 'es'

            result = self.translator.detect_language("Hola mundo")
            self.assertEqual(result, 'es')
            mock_detect.assert_called_once_with("Hola mundo")

    def test_detect_language_short_text(self):
        """Test language detection for very short text."""
        result = self.translator.detect_language("Hi")
        self.assertIsNone(result)

    def test_detect_language_failure(self):
        """Test language detection handles failures."""
        with patch('src.translation.detect') as mock_detect:
            mock_detect.side_effect = Exception("Detection failed")

            result = self.translator.detect_language("Some text")
            self.assertIsNone(result)

    def test_map_to_nllb_lang_supported(self):
        """Test NLLB language mapping for supported languages."""
        test_cases = [
            ('en', 'eng_Latn'),
            ('es', 'spa_Latn'),
            ('fr', 'fra_Latn'),
            ('de', 'deu_Latn'),
            ('zh', 'zho_Hans'),
            ('ar', 'ara_Arab'),
        ]

        for input_lang, expected in test_cases:
            result = self.translator._map_to_nllb_lang(input_lang)
            self.assertEqual(result, expected, f"Failed for {input_lang}")

    def test_map_to_nllb_lang_unsupported(self):
        """Test NLLB language mapping defaults to English for unsupported languages."""
        result = self.translator._map_to_nllb_lang("unsupported_lang")
        self.assertEqual(result, 'eng_Latn')

    @patch('src.translation.AutoTokenizer')
    @patch('src.translation.AutoModelForSeq2SeqLM')
    def test_load_nllb_model_success(self, mock_model, mock_tokenizer):
        """Test successful NLLB model loading."""
        mock_tokenizer.from_pretrained.return_value = MagicMock()
        mock_model.from_pretrained.return_value = MagicMock()

        self.translator._load_nllb_model()

        self.assertTrue(self.translator._nllb_loaded)
        mock_tokenizer.from_pretrained.assert_called_once_with("facebook/nllb-200-distilled-600M")
        mock_model.from_pretrained.assert_called_once_with("facebook/nllb-200-distilled-600M")

    @patch('src.translation.AutoTokenizer')
    @patch('src.translation.AutoModelForSeq2SeqLM')
    def test_load_nllb_model_failure(self, mock_model, mock_tokenizer):
        """Test NLLB model loading failure."""
        mock_tokenizer.from_pretrained.side_effect = Exception("Download failed")

        self.translator._load_nllb_model()

        self.assertFalse(self.translator._nllb_loaded)

    def test_translate_nllb_fallback_on_import_error(self):
        """Test NLLB translation falls back to Google when NLLB unavailable."""
        # Simulate NLLB not available
        self.translator._nllb_loaded = False

        with patch.object(self.translator, '_translate_google') as mock_google:
            mock_google.return_value = "Fallback translation"

            result = self.translator._translate_nllb("Test text", "es")
            mock_google.assert_called_once_with("Test text", "es")
            self.assertEqual(result, "Fallback translation")

    def test_translate_file_success(self):
        """Test successful file translation."""
        import tempfile
        import os

        # Create temporary input file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Hello world")
            input_file = f.name

        try:
            with patch.object(self.translator, 'translate_text') as mock_translate:
                mock_translate.return_value = "Hola mundo"

                result = self.translator.translate_file(input_file, "es")

                self.assertIsNotNone(result)
                self.assertTrue(Path(result).exists())

                # Check content
                with open(result, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.assertEqual(content, "Hola mundo")

                # Clean up output file
                Path(result).unlink()

        finally:
            # Clean up input file
            Path(input_file).unlink()

    def test_translate_file_input_not_found(self):
        """Test file translation with non-existent input file."""
        result = self.translator.translate_file("/nonexistent/file.txt", "es")
        self.assertIsNone(result)

    def test_translate_file_translation_failure(self):
        """Test file translation when translation fails."""
        import tempfile

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Hello world")
            input_file = f.name

        try:
            with patch.object(self.translator, 'translate_text') as mock_translate:
                mock_translate.return_value = None

                result = self.translator.translate_file(input_file, "es")
                self.assertIsNone(result)

        finally:
            Path(input_file).unlink()


if __name__ == '__main__':
    unittest.main()