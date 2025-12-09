"""
Translation utilities for text translation using deep_translator.

This module provides functionality for detecting languages and translating text
between different languages using Google Translate.
"""

import logging
from typing import Optional
from pathlib import Path

try:
    from langdetect import detect, DetectorFactory
    from deep_translator import GoogleTranslator
    LANGDETECT_AVAILABLE = True
    # Ensure consistent language detection results
    DetectorFactory.seed = 0
except ImportError:
    LANGDETECT_AVAILABLE = False
    detect = None
    DetectorFactory = None
    GoogleTranslator = None

# NLLB imports for contextual translation
try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    import torch
    NLLB_AVAILABLE = True
except ImportError:
    NLLB_AVAILABLE = False
    AutoTokenizer = None
    AutoModelForSeq2SeqLM = None
    torch = None

logger = logging.getLogger(__name__)


class TextTranslator:
    """
    Text translation service with dual translation modes.

    Provides language detection and translation capabilities for text content.
    Supports both fast Google Translate and contextual NLLB translation.
    """

    def __init__(self):
        """Initialize the translator."""
        if not LANGDETECT_AVAILABLE:
            raise ImportError(
                "langdetect and deep_translator are required for translation. "
                "Install with: pip install langdetect deep_translator")

        # NLLB model cache
        self._nllb_tokenizer = None
        self._nllb_model = None
        self._nllb_loaded = False

    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the language of the given text.

        Args:
            text: Text to detect language for

        Returns:
            Language code (e.g., 'en', 'fr', 'es') or None if detection fails
        """
        try:
            # Skip language detection for very short texts or if langdetect fails
            if len(text.strip()) < 3:
                logger.warning("Text too short for language detection")
                return None
            language = detect(text)
            logger.info(f"Detected language: {language}")
            return language
        except Exception as e:
            logger.error(f"Error detecting language: {e}")
            return None

    def translate_text(self, text: str, target_language: str, context: bool = False) -> Optional[str]:
        """
        Translate text to the target language with optional contextual translation.

        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'en', 'fr', 'es')
            context: Use contextual NLLB translation for better quality (slower)

        Returns:
            Translated text or None if translation fails
        """
        # Auto-detect if context translation should be used
        if not context and self._should_use_context(text):
            logger.info("Auto-enabling contextual translation for long text")
            context = True

        if context:
            return self._translate_nllb(text, target_language)
        else:
            return self._translate_google(text, target_language)

    def _translate_google(self, text: str, target_language: str) -> Optional[str]:
        """
        Fast translation using Google Translate.

        Args:
            text: Text to translate (max 5000 chars)
            target_language: Target language code

        Returns:
            Translated text or None if translation fails
        """
        try:
            # Check length limit
            if len(text) > 5000:
                logger.warning(f"Text length ({len(text)}) exceeds Google Translate limit (5000). Consider using context=True")
                # Truncate for Google Translate
                text = text[:5000]
                logger.info("Truncated text to 5000 characters for Google Translate")

            translated = GoogleTranslator(target=target_language).translate(text)
            logger.info(f"Successfully translated text to {target_language} using Google Translate")
            return translated
        except Exception as e:
            logger.error(f"Error translating text with Google Translate: {e}")
            return None

    def _translate_nllb(self, text: str, target_language: str) -> Optional[str]:
        """
        Contextual translation using NLLB model.

        Args:
            text: Text to translate (no length limit)
            target_language: Target language code

        Returns:
            Translated text or None if translation fails
        """
        try:
            # Load NLLB model if not already loaded
            if not self._nllb_loaded:
                self._load_nllb_model()

            if not self._nllb_loaded:
                logger.warning("NLLB model not available, falling back to Google Translate")
                return self._translate_google(text, target_language)

            # Map language codes to NLLB format
            source_lang = self._map_to_nllb_lang(self.detect_language(text) or 'en')
            target_lang = self._map_to_nllb_lang(target_language)

            # Tokenize and translate
            inputs = self._nllb_tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

            # Move to GPU if available
            if torch and torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
                self._nllb_model = self._nllb_model.cuda()

            # Generate translation
            translated_tokens = self._nllb_model.generate(
                **inputs,
                forced_bos_token_id=self._nllb_tokenizer.convert_tokens_to_ids(target_lang),
                max_length=512,
                num_beams=4,
                early_stopping=True
            )

            # Decode translation
            translated_text = self._nllb_tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

            logger.info(f"Successfully translated text to {target_language} using NLLB")
            return translated_text

        except Exception as e:
            logger.error(f"Error translating text with NLLB: {e}")
            logger.info("Falling back to Google Translate")
            return self._translate_google(text, target_language)

    def _should_use_context(self, text: str) -> bool:
        """
        Determine if contextual translation should be used based on text characteristics.

        Args:
            text: Text to analyze

        Returns:
            True if contextual translation is recommended
        """
        # Use contextual translation for long texts (>4000 chars)
        # This threshold is below Google's 5000 limit to account for safety margin
        return len(text) > 4000

    def _load_nllb_model(self):
        """Load the NLLB model and tokenizer."""
        try:
            if not NLLB_AVAILABLE:
                logger.warning("NLLB dependencies not available")
                return

            model_name = "facebook/nllb-200-distilled-600M"
            logger.info(f"Loading NLLB model: {model_name}")

            self._nllb_tokenizer = AutoTokenizer.from_pretrained(model_name)
            self._nllb_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

            # Set model to evaluation mode
            self._nllb_model.eval()
            self._nllb_loaded = True

            logger.info("NLLB model loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load NLLB model: {e}")
            self._nllb_loaded = False

    def _map_to_nllb_lang(self, lang_code: str) -> str:
        """
        Map common language codes to NLLB format.

        Args:
            lang_code: Standard language code

        Returns:
            NLLB language code
        """
        # NLLB language code mapping
        nllb_lang_map = {
            'en': 'eng_Latn',
            'es': 'spa_Latn',
            'fr': 'fra_Latn',
            'de': 'deu_Latn',
            'it': 'ita_Latn',
            'pt': 'por_Latn',
            'ru': 'rus_Cyrl',
            'zh': 'zho_Hans',
            'ja': 'jpn_Jpan',
            'ko': 'kor_Hang',
            'ar': 'ara_Arab',
            'hi': 'hin_Deva',
            'bn': 'ben_Beng',
            'ur': 'urd_Arab',
            'fa': 'pes_Arab',
            'tr': 'tur_Latn',
            'pl': 'pol_Latn',
            'nl': 'nld_Latn',
            'sv': 'swe_Latn',
            'da': 'dan_Latn',
            'no': 'nor_Latn',
            'fi': 'fin_Latn',
            'he': 'heb_Hebr',
            'th': 'tha_Thai',
            'vi': 'vie_Latn',
            'id': 'ind_Latn',
            'ms': 'zsm_Latn',
            'tl': 'tgl_Latn',
        }

        return nllb_lang_map.get(lang_code, 'eng_Latn')  # Default to English

    def translate_file(self,
                        file_path: str,
                        target_language: str,
                        output_file: Optional[str] = None,
                        context: bool = False) -> Optional[str]:
        """
        Translate a text file to the target language.

        Args:
            file_path: Path to the text file to translate
            target_language: Target language code
            output_file: Optional output file path. If None, auto-generates.

        Returns:
            Path to the translated file or None if translation fails
        """
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None

        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            # Detect source language (optional for translation)
            source_language = self.detect_language(text)
            if not source_language:
                logger.warning("Could not detect the language of the text, proceeding with translation")
                # Don't return None, continue with translation

            if source_language:
                print(f"📝 Detected language: {source_language}")

            # Translate the text
            translated_text = self.translate_text(text, target_language, context)
            if not translated_text:
                logger.error("Translation failed")
                return None

            # Determine output file path
            if output_file:
                output_path = Path(output_file)
            else:
                output_path = file_path.parent / f"translated_{target_language}.txt"

            # Write translated text
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(translated_text)

            print(f"✅ Translated text saved to {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"Error processing file: {e}")
            return None


def translate_file_cli(file_path: str,
                        target_language: str,
                        output_file: Optional[str] = None,
                        context: bool = False) -> Optional[str]:
    """
    Command-line interface for translating text files.

    Args:
        file_path: Path to the text file
        target_language: Target language code
        output_file: Optional output file path
        context: Use contextual translation

    Returns:
        Path to translated file or None
    """
    translator = TextTranslator()
    return translator.translate_file(file_path, target_language, output_file, context)


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Translate text file to a specified language.")
    parser.add_argument("file_path",
                        type=str,
                        help="Path to the text file to be translated.")
    parser.add_argument(
        "target_language",
        type=str,
        help="Target language code (e.g., 'en' for English, 'fr' for French).")
    parser.add_argument("--output",
                        "-o",
                        type=str,
                        help="Output file path (optional)")
    parser.add_argument("--context",
                        action="store_true",
                        help="Use contextual NLLB translation (better quality, slower)")

    args = parser.parse_args()

    result = translate_file_cli(args.file_path, args.target_language,
                                 args.output, args.context)
    if not result:
        exit(1)
