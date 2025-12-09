"""
OCR API endpoints for FastAPI integration.

This module provides REST API endpoints for OCR text extraction
from uploaded images and documents.
"""

import logging
import tempfile
import os
from typing import List, Optional
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .core import OCREngine
from ..translation import TextTranslator
from ..summarizer import ContentProcessor

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize engines (lazy loading)
ocr_engine = None
translator = None
summarizer = None

def get_ocr_engine() -> OCREngine:
    """Get or create OCR engine instance."""
    global ocr_engine
    if ocr_engine is None:
        try:
            ocr_engine = OCREngine()
            logger.info("OCR engine initialized for API")
        except Exception as e:
            logger.error(f"Failed to initialize OCR engine: {e}")
            raise HTTPException(status_code=500, detail="OCR engine initialization failed")
    return ocr_engine

def get_translator() -> TextTranslator:
    """Get or create translator instance."""
    global translator
    if translator is None:
        try:
            translator = TextTranslator()
            logger.info("Translator initialized for API")
        except Exception as e:
            logger.error(f"Failed to initialize translator: {e}")
            raise HTTPException(status_code=500, detail="Translator initialization failed")
    return translator

def get_summarizer(model_size: str = "small") -> ContentProcessor:
    """Get or create summarizer instance with specified model size."""
    global summarizer
    if summarizer is None or getattr(summarizer, 'model_size', None) != model_size:
        try:
            summarizer = ContentProcessor()
            logger.info(f"Summarizer initialized for API with {model_size} model")
        except Exception as e:
            logger.error(f"Failed to initialize summarizer: {e}")
            raise HTTPException(status_code=500, detail="Summarizer initialization failed")
    return summarizer


class OCRResult(BaseModel):
    """OCR result model."""
    text: str
    image_path: Optional[str] = None
    model: str
    processing_time: float
    device: str
    translated_text: Optional[str] = None
    target_language: Optional[str] = None
    summarized_content: Optional[str] = None


class BatchOCRResult(BaseModel):
    """Batch OCR result model."""
    results: List[OCRResult]
    total_images: int
    successful: int
    failed: int


@router.post("/ocr/extract", response_model=OCRResult)
async def extract_text_from_image(
    file: UploadFile = File(...),
    ocr_type: str = Form("handwritten", description="OCR type for processing (handwritten text)"),
    translate: bool = Form(False, description="Whether to translate the extracted text"),
    target_language: str = Form("en", description="Target language for translation (e.g., 'en', 'fr', 'es')"),
    context: bool = Form(False, description="Use contextual NLLB translation (better quality, slower)"),
    summarize_content: bool = Form(False, description="Whether to summarize the extracted content"),
    summarizer_model: str = Form("small", description="mT5 model size for summarization ('small', 'base', 'large')")
):
    """
    Extract handwritten text from an uploaded image using TrOCR Large model.

    - **file**: Image file to process (JPEG, PNG, etc.)
    - **ocr_type**: OCR processing type (default: "handwritten" - optimized for handwritten text)
    - **translate**: Whether to translate the extracted text to another language
    - **target_language**: Target language code for translation (default: "en")
    - **context**: Use contextual NLLB translation for better quality (slower)
    - **summarize_content**: Whether to summarize the extracted content using mT5
    - **summarizer_model**: mT5 model size for summarization ('small', 'base', 'large')
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    # Validate file extension
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            # Process with OCR
            engine = get_ocr_engine()
            result = engine.extract_text(temp_file_path, ocr_type)

            # Handle translation if requested
            translated_text = None
            if translate and result['text'].strip():
                try:
                    translator_engine = get_translator()
                    translated_text = translator_engine.translate_text(
                        result['text'],
                        target_language,
                        context=context
                    )
                    logger.info(f"Successfully translated text to {target_language}")
                except Exception as e:
                    logger.warning(f"Translation failed: {e}")
                    # Continue without translation rather than failing the whole request

            # Handle summarization if requested
            summarized_content = None
            if summarize_content and result['text'].strip():
                try:
                    summarizer_engine = get_summarizer(summarizer_model)
                    # Use translated text if available, otherwise original text
                    text_to_summarize = translated_text if translated_text else result['text']
                    summarized_content = summarizer_engine.summarize(text_to_summarize)
                    logger.info("Successfully summarized content")
                except Exception as e:
                    logger.warning(f"Summarization failed: {e}")
                    # Continue without summarization rather than failing the whole request

            # Return result with optional translation and summarization
            return OCRResult(
                **result,
                translated_text=translated_text,
                target_language=target_language if translate else None,
                summarized_content=summarized_content
            )

        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass

    except Exception as e:
        logger.error(f"OCR processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")


@router.post("/ocr/extract/batch", response_model=BatchOCRResult)
async def extract_text_from_images(
    files: List[UploadFile] = File(...),
    ocr_type: str = Form("handwritten", description="OCR type for processing (handwritten text)"),
    translate: bool = Form(False, description="Whether to translate the extracted text"),
    target_language: str = Form("en", description="Target language for translation (e.g., 'en', 'fr', 'es')"),
    context: bool = Form(False, description="Use contextual NLLB translation (better quality, slower)"),
    summarize_content: bool = Form(False, description="Whether to summarize the extracted content"),
    summarizer_model: str = Form("small", description="mT5 model size for summarization ('small', 'base', 'large')")
):
    """
    Extract handwritten text from multiple uploaded images using TrOCR Large model.

    - **files**: List of image files to process
    - **ocr_type**: OCR processing type (default: "handwritten" - optimized for handwritten text)
    - **translate**: Whether to translate the extracted text to another language
    - **target_language**: Target language code for translation (default: "en")
    - **context**: Use contextual NLLB translation for better quality (slower)
    - **summarize_content**: Whether to summarize the extracted content
    - **summarizer_model**: mT5 model size for summarization ('small', 'base', 'large')
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    if len(files) > 10:  # Limit batch size
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed for batch processing")

    temp_files = []

    try:
        # Save all uploaded files temporarily
        for file in files:
            if not file.filename:
                continue

            file_ext = Path(file.filename).suffix.lower()
            allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}

            if file_ext not in allowed_extensions:
                continue  # Skip invalid files

            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
                content = await file.read()
                temp_file.write(content)
                temp_files.append(temp_file.name)

        if not temp_files:
            raise HTTPException(status_code=400, detail="No valid image files provided")

        # Process batch with OCR
        engine = get_ocr_engine()
        results = engine.extract_text_batch(temp_files, ocr_type)

        # Handle translation and summarization if requested
        if translate:
            translator_engine = get_translator()
        if summarize_content:
            summarizer_engine = get_summarizer(summarizer_model)

        # Convert to response model
        ocr_results = []
        for result in results:
            if 'error' not in result:
                translated_text = None
                if translate and result['text'].strip():
                    try:
                        translated_text = translator_engine.translate_text(
                            result['text'],
                            target_language,
                            context=context
                        )
                    except Exception as e:
                        logger.warning(f"Translation failed for {result.get('image_path')}: {e}")

                summarized_content = None
                if summarize_content and result['text'].strip():
                    try:
                        # Use translated text if available, otherwise original text
                        text_to_summarize = translated_text if translated_text else result['text']
                        summarized_content = summarizer_engine.summarize(text_to_summarize)
                    except Exception as e:
                        logger.warning(f"Summarization failed for {result.get('image_path')}: {e}")

                ocr_results.append(OCRResult(
                    **result,
                    translated_text=translated_text,
                    target_language=target_language if translate else None,
                    summarized_content=summarized_content
                ))
            else:
                # Create error result
                ocr_results.append(OCRResult(
                    text="",
                    image_path=result.get('image_path'),
                    model=result.get('model', 'unknown'),
                    processing_time=0.0,
                    device='unknown',
                    translated_text=None,
                    target_language=None
                ))

        response = BatchOCRResult(
            results=ocr_results,
            total_images=len(results),
            successful=sum(1 for r in results if 'error' not in r),
            failed=sum(1 for r in results if 'error' in r)
        )

        return response

    except Exception as e:
        logger.error(f"Batch OCR processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Batch OCR processing failed: {str(e)}")

    finally:
        # Clean up temporary files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except OSError:
                pass


@router.get("/ocr/models")
async def get_available_models():
    """Get information about available OCR models."""
    return {
        "models": [
            {
                "name": "Microsoft TrOCR Large Handwritten",
                "model_id": "microsoft/trocr-large-handwritten",
                "description": "Optimized Microsoft TrOCR Large Model for English Handwriting Recognition with highest accuracy for poor/unclear handwriting",
                "supported_languages": "English (handwritten text)",
                "features": ["Handwritten text recognition", "High accuracy on poor handwriting", "Segmentation-based processing", "Fallback to base model"]
            }
        ],
        "current_model": "Microsoft TrOCR Large Handwritten"
    }


@router.get("/ocr/health")
async def ocr_health_check():
    """Health check for OCR service."""
    try:
        engine = get_ocr_engine()
        return {
            "status": "healthy",
            "model": engine.model_name,
            "device": engine.device
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }