# Contributing to Multi-Platform Video Downloader

Thank you for your interest in contributing! 🎉

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- **Description**: Clear description of the bug
- **Steps to reproduce**: How to trigger the bug
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: OS, Python version, etc.
- **Logs**: Include error messages (use `--verbose` flag)

### Suggesting Features

Feature requests are welcome! Please include:
- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives**: Any alternative approaches?

### Code Contributions

#### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/video-downloader.git
cd video-downloader
```

#### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### 3. Create a Branch

```bash
# Create a descriptive branch name
git checkout -b feature/add-twitter-support
# or
git checkout -b fix/instagram-story-bug
```

#### 4. Make Your Changes

**Code Style:**
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions/classes
- Keep functions focused and small

**Example:**
```python
def validate_url(self, url):
    """
    Validate Twitter URL format.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if valid Twitter URL
    """
    pattern = r'^(https?://)?(www\.)?twitter\.com/.+/status/\d+'
    return bool(re.match(pattern, url))
```

#### 5. Add Tests

**Required for all code contributions:**
```bash
# Create test file in tests/ directory
# tests/test_newfeature.py

import pytest
from src.downloader.newfeature import NewFeatureDownloader

def test_feature():
    downloader = NewFeatureDownloader()
    assert downloader.some_method() == expected_result
```

**Run tests:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/downloader

# Run specific test
pytest tests/test_newfeature.py -v
```

#### 6. Commit Your Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: Add Twitter video downloader support

- Implement TwitterDownloader class
- Add URL validation for Twitter status URLs
- Add comprehensive test suite
- Update documentation"
```

**Commit Message Format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding/updating tests
- `refactor:` Code refactoring
- `style:` Code style changes
- `chore:` Maintenance tasks

#### 7. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/add-twitter-support

# Go to GitHub and create Pull Request
```

**Pull Request Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All existing tests pass
- [ ] Added tests for new features
- [ ] Tested manually with real URLs

## Checklist
- [ ] Code follows project style
- [ ] Added/updated documentation
- [ ] Added/updated tests
- [ ] No breaking changes (or documented)
```

## 📋 Adding a New Library

### Step-by-Step Guide for New Libraries

#### 1. Create Library Structure

**Example:** `src/converter/` for audio/video conversion library
```bash
src/converter/
├── __init__.py          # Package initialization
├── audio.py             # Audio conversion logic
├── video.py             # Video conversion logic
├── api.py               # FastAPI endpoints for converter
└── utils.py             # Conversion utilities
```

#### 2. Create Library Classes

**File:** `src/converter/audio.py`
```python
"""
Audio conversion utilities.
"""
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class AudioConverter:
    """Audio format converter using FFmpeg."""

    def __init__(self, output_dir: str = './converted'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def convert_mp3_to_wav(self, input_file: str, output_file: Optional[str] = None) -> str:
        """
        Convert MP3 file to WAV format.

        Args:
            input_file: Path to input MP3 file
            output_file: Optional output file path

        Returns:
            Path to converted WAV file
        """
        # Implementation here
        pass

    def convert_wav_to_mp3(self, input_file: str, bitrate: str = '192k') -> str:
        """
        Convert WAV file to MP3 format.

        Args:
            input_file: Path to input WAV file
            bitrate: Target bitrate (e.g., '128k', '192k', '320k')

        Returns:
            Path to converted MP3 file
        """
        # Implementation here
        pass
```

#### 3. Create API Endpoints

**File:** `src/converter/api.py`
```python
"""
FastAPI endpoints for converter library.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from .audio import AudioConverter
from .video import VideoConverter

app = FastAPI(title="Converter API")

converter = AudioConverter()

@app.post("/convert/audio/mp3-to-wav")
async def convert_mp3_to_wav(file: UploadFile = File(...)):
    """Convert uploaded MP3 file to WAV format."""
    # Implementation here
    pass
```

#### 4. Update Main Entry Point

**File:** `main.py`
```python
# Add converter API option
parser.add_argument(
    '--converter-api',
    action='store_true',
    help="Run converter API server"
)

if args.converter_api:
    from src.converter.api import app
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

#### 5. Update Documentation

- Add to README.md supported platforms
- Update CHANGELOG.md
- Add usage examples

## 🧪 Testing Guidelines

### Test Coverage Requirements
- Minimum 80% code coverage
- Test all public methods
- Test error cases
- Test edge cases

### Test Structure
```python
class TestNewFeature:
    """Test suite for NewFeature."""
    
    def test_initialization(self):
        """Test object initialization."""
        pass
    
    def test_success_case(self):
        """Test successful operation."""
        pass
    
    def test_error_handling(self):
        """Test error cases."""
        pass
```

## 📝 Documentation Guidelines

- Update README.md for user-facing changes
- Add docstrings to all functions/classes
- Include code examples
- Update CHANGELOG.md

## 🔍 Code Review Process

1. Automated tests must pass
2. Code review by maintainer
3. Address feedback
4. Final approval and merge

## ❓ Questions?

Feel free to:
- Open an issue for questions
- Ask in pull request comments
- Reach out to maintainers

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing! 🙏**