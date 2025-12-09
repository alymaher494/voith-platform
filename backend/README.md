# Media Processing Studio

A comprehensive media processing platform that combines video downloading, format conversion, audio processing, and AI-powered content analysis into a unified API suite.

## 🎯 Features

### Current Services
- **🎬 Downloader**: Download videos from various platforms (YouTube, Vimeo, etc.)
- **🔄 Converter**: Convert between audio/video formats, compress media files
- **🗣️ ASR**: Automatic speech recognition and transcription with word-level timestamps
- **🌍 Translator**: Multi-language text translation
- **📝 Summarizer**: Content summarization and Q&A using mT5 models

### Planned Services
- **💬 Chat**: AI-powered Q&A with video/audio content
- **✏️ Editor**: Video editing, audio enhancement, subtitle generation

## 🚀 Quick Start

### Using Docker (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd media-processing-studio

# Start all services
docker-compose up -d

# Access the API documentation
open http://localhost:8000/docs
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the unified API server
python main.py --api

# Or run individual services
python main.py --converter-api  # Port 8001
```

## 📖 API Documentation

### Main API Server (Port 8000)
- **Interactive Docs**: http://localhost:8000/docs
- **Reference Docs**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Converter API Server (Port 8001)
- **Interactive Docs**: http://localhost:8001/docs
- **File Access**: http://localhost:8001/files

## 🔧 Services Overview

### 🎬 Video Downloader
Download videos from multiple platforms with format selection and time slicing.

```bash
# CLI usage
python main.py --url "https://youtube.com/watch?v=VIDEO_ID" --format_id 22

# API usage
POST /downloader/download
{
  "url": "https://youtube.com/watch?v=VIDEO_ID",
  "format_id": "22"
}
```

### 🔄 Media Converter
Convert between audio/video formats with compression options.

```bash
# CLI usage
python convert_video.py input.mp4 --format webm --quality medium

# API usage
POST /converter/convert/video
{
  "input_path": "input.mp4",
  "output_format": "webm",
  "quality": "medium"
}
```

### 🗣️ Speech Recognition (ASR)
Transcribe audio/video files with word-level timestamps.

```bash
# CLI usage
python transcribe_audio.py audio.wav --language en --model base

# API usage
POST /asr/transcribe/audio
{
  "audio_path": "audio.wav",
  "language": "en",
  "model_size": "base"
}
```

### 🌍 Text Translation
Translate text files between languages.

```bash
# CLI usage
python translate_text.py document.txt fr

# API usage (planned)
POST /translator/translate
{
  "text": "Hello world",
  "target_language": "fr"
}
```

### 📝 Content Summarizer
Summarize text content and answer questions using multilingual mT5 models.

#### mT5 Model Sizes
Choose the appropriate model size based on your needs:

| Model Size | Parameters | Size | Speed | Quality | Best For |
|------------|------------|------|-------|---------|----------|
| **small** | 300M | ~300MB | ⚡ Fastest | Good | Real-time, cost-effective |
| **base** | 580M | ~1.2GB | Fast | Better | Production, balanced |
| **large** | 1.2B | ~2.3GB | Slow | Best | Critical, maximum accuracy |

```bash
# API usage - Q&A
POST /summarizer/ask
{
  "question": "What is the main topic?",
  "context": "Long text content here...",
  "model": "small"
}

# Integrated with OCR/ASR
POST /ocr/extract
{
  "file": "document.jpg",
  "summarize_content": true,
  "summarizer_model": "base"
}
```

## 🏗️ Architecture

```
media-processing-studio/
├── main.py                 # CLI entry point and API server
├── src/
│   ├── api.py             # Main FastAPI application
│   ├── translation.py     # Text translation service
│   ├── asr/               # Speech recognition module
│   ├── converter/         # Media conversion module
│   └── downloader/        # Video downloading module
├── tests/                 # Comprehensive test suite
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Multi-service orchestration
└── requirements.txt      # Python dependencies
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run specific test categories
pytest tests/test_asr/      # ASR tests
pytest tests/test_converter/  # Converter tests
pytest tests/test_api.py    # API tests
```

## 🔧 Development

### Setting up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest

# Start development server
python main.py --api
```

### Adding New Features
1. Create feature branch: `git checkout -b feature/new-feature`
2. Add tests for new functionality
3. Implement the feature
4. Update documentation
5. Submit pull request

## 📋 API Endpoints

### Downloader Service
- `GET /downloader/formats/{url}` - Get available formats
- `POST /downloader/download` - Download video

### Converter Service
- `POST /converter/convert/audio` - Convert audio formats
- `POST /converter/convert/video` - Convert video formats
- `POST /converter/extract/audio` - Extract audio from video
- `POST /converter/compress/video` - Compress video files

### ASR Service
- `POST /asr/transcribe/audio` - Transcribe audio file
- `POST /asr/transcribe/video` - Transcribe video file
- `POST /asr/transcribe/audio/upload` - Upload and transcribe audio
- `POST /asr/transcribe/video/upload` - Upload and transcribe video
- `GET /asr/languages` - List supported languages
- `GET /asr/models` - List available models

### Summarizer Service
- `POST /summarizer/ask` - Answer questions about text content
- `GET /summarizer/models` - List available mT5 models
- `GET /summarizer/health` - Service health check

## 🤝 Contributing

Please read [CONTRIBUTING.md](contributing.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](license.md) file for details.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Video downloading
- [WhisperX](https://github.com/m-bain/whisperX) - Speech recognition
- [FFmpeg](https://ffmpeg.org/) - Media processing
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [langdetect](https://pypi.org/project/langdetect/) - Language detection
## GPU Setup (Automatic)

To enable GPU support on any fresh machine:

1. Run the setup script:


./install-gpu-deps.sh


2. Restart the terminal.

3. Run the app normally:


python3 your_script.py


This script installs cuDNN for CUDA 12 and configures LD_LIBRARY_PATH automatically.
- [deep_translator](https://pypi.org/project/deep_translator/) - Translation service