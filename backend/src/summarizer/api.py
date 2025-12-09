"""
FastAPI router for summarizer endpoints.
"""

import logging
from typing import Optional
from pydantic import BaseModel

from fastapi import APIRouter, HTTPException

from .core import ContentProcessor

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/summarizer", tags=["Summarizer"])

# Global processor instance (lazy loaded)
_processor = None


def get_processor(model_size: str = "small") -> ContentProcessor:
    """Get or create the global content processor instance with specified model size."""
    global _processor
    if _processor is None or getattr(_processor, 'model_size', None) != model_size:
        try:
            _processor = ContentProcessor()
            logger.info(f"Initialized ContentProcessor for API with {model_size} model")
        except Exception as e:
            logger.error(f"Failed to initialize ContentProcessor: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Summarizer service initialization failed: {str(e)}"
            )
    return _processor


class QnARequest(BaseModel):
    """Request model for Q&A."""
    question: str
    context: str
    max_answer_length: Optional[int] = 100
    model: str = "small"


class QnAResponse(BaseModel):
    """Response model for Q&A."""
    question: str
    context: str
    answer: str
    model: str


@router.post("/ask", response_model=QnAResponse)
async def answer_question(request: QnARequest):
    """
    Answer a question based on the provided context.

    - **question**: The question to answer
    - **context**: The context text containing relevant information
    - **max_answer_length**: Maximum length of the answer (default: 100)
    - **model**: mT5 model size ('small', 'base', 'large')
    """
    try:
        processor = get_processor(request.model)

        answer = processor.answer_question(
            question=request.question,
            context=request.context,
            max_length=request.max_answer_length
        )

        if answer is None:
            raise HTTPException(status_code=500, detail="Failed to generate answer")

        return QnAResponse(
            question=request.question,
            context=request.context,
            answer=answer,
            model=processor.model_name
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Q&A failed: {e}")
        raise HTTPException(status_code=500, detail=f"Q&A failed: {str(e)}")


@router.get("/models")
async def get_available_models():
    """Get information about available mT5 models."""
    return {
        "models": [
            {
                "size": "small",
                "model_id": "google/mt5-small",
                "description": "Fastest model, good quality for most use cases",
                "parameters": "~300M",
                "size_mb": "~300MB",
                "use_cases": ["Real-time processing", "Cost-effective", "Development"]
            },
            {
                "size": "base",
                "model_id": "google/mt5-base",
                "description": "Balanced quality and speed",
                "parameters": "~580M",
                "size_mb": "~1.2GB",
                "use_cases": ["Production applications", "Better accuracy", "Professional use"]
            },
            {
                "size": "large",
                "model_id": "google/mt5-large",
                "description": "Highest quality, slower processing",
                "parameters": "~1.2B",
                "size_mb": "~2.3GB",
                "use_cases": ["Critical applications", "Maximum accuracy", "Research"]
            }
        ],
        "recommended": "small",
        "note": "Larger models provide better quality but require more resources and processing time"
    }


@router.get("/health")
async def summarizer_health_check():
    """Health check for summarizer service."""
    try:
        processor = get_processor()
        return {
            "status": "healthy",
            "current_model": processor.model_name,
            "model_size": processor.model_size,
            "device": "cuda" if processor.model.device.type == "cuda" else "cpu"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }