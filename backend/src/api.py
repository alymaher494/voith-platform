"""
Main FastAPI application for the multi-library media processing system.

This application serves as the central API router that combines multiple
libraries (downloader, converter) into a unified REST API interface.
"""
import logging
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Add project root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import library routers
from src.downloader.api import router as downloader_router
from src.converter.api import router as converter_router
from src.asr.api import router as asr_router
from src.ocr.api import router as ocr_router
from src.summarizer.api import router as summarizer_router

# Configure logging for the main application
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="Media Processing Studio API",
    description="""
    # Media Processing Studio

    A comprehensive media processing platform that combines video downloading,
    format conversion, audio processing, and AI-powered content analysis into
    a unified API suite.

    ## 🎯 Services

    ### Current Services
    - **🎬 Downloader**: Download videos from various platforms (YouTube, Vimeo, etc.)
    - **🔄 Converter**: Convert between audio/video formats, compress media files
    - **🗣️ ASR**: Automatic speech recognition and transcription with word-level timestamps
    - **📝 OCR**: Text extraction from images and documents using GOT-OCR2.0

    ### Planned Services
    - **🌍 Translator**: Multi-language translation of audio/video content
    - **💬 Chat**: AI-powered Q&A with video/audio content
    - **✏️ Editor**: Video editing, audio enhancement, subtitle generation

    ## 🚀 Features

    - **Background Processing**: Long-running operations handled asynchronously
    - **Microservice Architecture**: Services can run independently or unified
    - **File Upload/Download**: Direct file processing and result retrieval
    - **Interactive Documentation**: Swagger UI and ReDoc available
    - **Comprehensive Validation**: Input validation with detailed error messages
    - **Progress Tracking**: Real-time status updates for operations
    - **Frontend Ready**: CORS enabled, JSON responses optimized for web clients
    - **RESTful Design**: Clean, consistent API endpoints with proper HTTP methods

    ## 🔧 Usage

    Start the unified API server:
    ```bash
    python main.py --api
    ```

    Access documentation at: http://localhost:8000/docs
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Media Processing Studio",
        "description": "Complete media processing pipeline"
    },
)

# Mount static files directory for serving converted files
app.mount("/files", StaticFiles(directory="./converted", html=True), name="files")
app.mount("/downloads", StaticFiles(directory="./downloads", html=True), name="downloads")

# Include library routers
app.include_router(downloader_router)
app.include_router(converter_router)
app.include_router(asr_router)
app.include_router(ocr_router)
app.include_router(summarizer_router)

@app.get("/")
async def root():
    """
    Root endpoint providing API information and navigation.

    Returns comprehensive API metadata including version, available services,
    and navigation links. Useful for API discovery, health checks, and
    understanding the platform capabilities.

    Returns:
        dict: Complete API information including services, documentation links,
              and current status
    """
    return {
        "message": "🎬 Media Processing Studio API",
        "version": "2.0.0",
        "status": "running",
        "description": "Complete media processing pipeline with AI integration",

        "services": {
            "current": {
                "downloader": {
                    "description": "Video downloading from various platforms",
                    "prefix": "/downloader",
                    "status": "active"
                },
                "converter": {
                    "description": "Audio/video format conversion and processing",
                    "prefix": "/converter",
                    "status": "active"
                },
                "asr": {
                    "description": "Automatic speech recognition and transcription",
                    "prefix": "/asr",
                    "status": "active"
                },
                "ocr": {
                    "description": "Text extraction from images using GOT-OCR2.0",
                    "prefix": "/ocr",
                    "status": "active"
                },
                "summarizer": {
                    "description": "Content summarization and Q&A using mT5",
                    "prefix": "/summarizer",
                    "status": "active"
                }
            },
            "planned": {
                "translator": {
                    "description": "Multi-language translation of audio/video content",
                    "status": "planned"
                },
                "chat": {
                    "description": "AI-powered Q&A with video/audio content",
                    "status": "planned"
                },
                "editor": {
                    "description": "Video editing, audio enhancement, subtitle generation",
                    "status": "planned"
                }
            }
        },

        "documentation": {
            "interactive": "/docs",
            "reference": "/redoc",
            "schema": "/openapi.json"
        },

        "features": {
            "file_access": "/files",
            "download_access": "/downloads",
            "health_check": "/health",
            "background_processing": True,
            "microservices": True,
            "upload_support": True,
            "batch_operations": False
        },

        "usage": {
            "unified_server": "python main.py --api",
            "frontend_ready": True,
            "cors_enabled": True
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.

    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": "2025-10-21T09:57:32.836Z",
        "libraries": {
            "downloader": "available",
            "converter": "available",
            "asr": "available",
            "ocr": "available",
            "summarizer": "available"
        },
        "endpoints": {
            "total": 17,
            "active": 17
        }
    }


# Add CORS middleware for frontend compatibility
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Development server entry point
if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting Media Processing API server...")
    logger.info("📖 API documentation: http://localhost:8000/docs")
    logger.info("📁 File access: http://localhost:8000/files")
    logger.info("📁 Downloads: http://localhost:8000/downloads")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )