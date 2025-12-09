# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-10-19

### Added
- 🌐 **REST API**: FastAPI-based REST API for programmatic access
  - Interactive API documentation at `/docs`
  - Background download processing
  - JSON request/response format
  - Comprehensive error handling

- 📡 **API Endpoints**:
  - `GET /` - API information and navigation
  - `GET /formats/{url}` - List available video formats
  - `POST /download` - Download videos with customizable options

- 🔧 **Enhanced Architecture**:
  - Modular API design ready for expansion
  - Background task processing for downloads
  - Improved error responses and logging
  - Type hints throughout codebase

### Changed
- **Project Structure**: Updated to reflect current architecture
- **Dependencies**: Added FastAPI and Uvicorn
- **Documentation**: Updated README and changelog for API features

### Technical Details
- FastAPI framework for modern API development
- Uvicorn ASGI server for production deployment
- Background task processing for non-blocking downloads
- Enhanced type safety with Pydantic models

---

## [1.0.0] - 2024-01-XX

### Added
- 🎯 **Universal downloader**: Single downloader supporting 1000+ platforms via yt-dlp
- 🎵 **Audio extraction**: Download audio-only as MP3 format
- ✂️ **Time slicing**: Extract specific segments using start/end times
- 🚀 **Smart features**: Automatic platform detection and fallback
- 📊 **Progress tracking**: Real-time download progress bars
- 🧪 **Testing**: Comprehensive test suite with pytest
- 🔧 **Developer features**: Abstract base class and modular architecture
- 📝 **Documentation**: Comprehensive README with examples

### Technical Details
- Python 3.7+ support
- yt-dlp integration for video extraction
- FFmpeg support for audio/video processing
- Virtual environment support

---

## [Unreleased]

### Planned Features
- [ ] Batch download from file list
- [ ] Subtitle/caption downloads
- [ ] Quality selection UI
- [ ] Download history tracking
- [ ] Resume interrupted downloads
- [ ] Proxy support
- [ ] Rate limiting options
- [ ] GUI interface (optional)
- [ ] Cookie support for authenticated content
- [ ] Thumbnail downloads
- [ ] Metadata extraction to JSON

### Under Consideration
- [ ] Docker containerization
- [ ] Web API interface
- [ ] Download scheduler
- [ ] Video format conversion
- [ ] Playlist filtering options

---

## Version History

### [1.0.0] - Initial Release
First stable release with core functionality for multi-platform video downloading.

---

**Note:** Dates are in YYYY-MM-DD format