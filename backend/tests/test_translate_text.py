"""
Tests for translate_text.py script.
"""
import sys
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from translate_text import main


@patch('translate_text.translate_file_cli')
@patch('translate_text.Path')
def test_main_basic_translation(mock_path_class, mock_translate_file_cli, monkeypatch, capsys):
    """Test main function with basic text file translation."""
    # Mock Path for input file
    mock_input_path = MagicMock()
    mock_input_path.exists.return_value = True
    mock_path_class.return_value = mock_input_path

    # Mock translation result
    mock_translate_file_cli.return_value = "translated_fr.txt"

    monkeypatch.setattr("sys.argv", ["translate_text.py", "document.txt", "fr"])

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0

    captured = capsys.readouterr()
    assert "🌐 Translating document.txt to fr..." in captured.out
    assert "✅ Translation completed: translated_fr.txt" in captured.out

    mock_translate_file_cli.assert_called_once_with("document.txt", "fr", None)


@patch('translate_text.translate_file_cli')
@patch('translate_text.Path')
def test_main_translation_with_output_file(mock_path_class, mock_translate_file_cli, monkeypatch, capsys):
    """Test main function with custom output file."""
    mock_input_path = MagicMock()
    mock_input_path.exists.return_value = True
    mock_path_class.return_value = mock_input_path

    mock_translate_file_cli.return_value = "custom_output.txt"

    monkeypatch.setattr("sys.argv", ["translate_text.py", "input.txt", "es", "--output", "custom_output.txt"])

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0

    captured = capsys.readouterr()
    assert "✅ Translation completed: custom_output.txt" in captured.out

    mock_translate_file_cli.assert_called_once_with("input.txt", "es", "custom_output.txt")


def test_main_input_file_not_found(monkeypatch, capsys):
    """Test main function with non-existent input file."""
    monkeypatch.setattr("sys.argv", ["translate_text.py", "nonexistent.txt", "en"])

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1

    captured = capsys.readouterr()
    assert "❌ Error: Input file 'nonexistent.txt' not found" in captured.out


@patch('translate_text.translate_file_cli')
@patch('translate_text.Path')
def test_main_translation_failure(mock_path_class, mock_translate_file_cli, monkeypatch, capsys):
    """Test main function when translation fails."""
    mock_input_path = MagicMock()
    mock_input_path.exists.return_value = True
    mock_path_class.return_value = mock_input_path

    mock_translate_file_cli.return_value = None  # Translation failed

    monkeypatch.setattr("sys.argv", ["translate_text.py", "document.txt", "de"])

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1

    captured = capsys.readouterr()
    assert "❌ Translation failed" in captured.out


@patch('translate_text.translate_file_cli')
@patch('translate_text.Path')
def test_main_different_target_languages(mock_path_class, mock_translate_file_cli, monkeypatch):
    """Test main function with different target languages."""
    mock_input_path = MagicMock()
    mock_input_path.exists.return_value = True
    mock_path_class.return_value = mock_input_path

    mock_translate_file_cli.return_value = "translated.txt"

    # Test with French
    monkeypatch.setattr("sys.argv", ["translate_text.py", "text.txt", "fr"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
    mock_translate_file_cli.assert_called_with("text.txt", "fr", None)

    # Reset mock
    mock_translate_file_cli.reset_mock()

    # Test with Spanish
    monkeypatch.setattr("sys.argv", ["translate_text.py", "text.txt", "es"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
    mock_translate_file_cli.assert_called_with("text.txt", "es", None)

    # Reset mock
    mock_translate_file_cli.reset_mock()

    # Test with German
    monkeypatch.setattr("sys.argv", ["translate_text.py", "text.txt", "de"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
    mock_translate_file_cli.assert_called_with("text.txt", "de", None)


@patch('translate_text.translate_file_cli')
@patch('translate_text.Path')
def test_main_with_output_parameter(mock_path_class, mock_translate_file_cli, monkeypatch):
    """Test main function properly passes output parameter."""
    mock_input_path = MagicMock()
    mock_input_path.exists.return_value = True
    mock_path_class.return_value = mock_input_path

    mock_translate_file_cli.return_value = "output.txt"

    monkeypatch.setattr("sys.argv", ["translate_text.py", "input.txt", "it", "--output", "output.txt"])

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0

    # Verify the output parameter was passed correctly
    call_args = mock_translate_file_cli.call_args
    assert call_args[0] == ("input.txt", "it", "output.txt")


@patch('translate_text.translate_file_cli')
@patch('translate_text.Path')
def test_main_without_output_parameter(mock_path_class, mock_translate_file_cli, monkeypatch):
    """Test main function passes None for output when not specified."""
    mock_input_path = MagicMock()
    mock_input_path.exists.return_value = True
    mock_path_class.return_value = mock_input_path

    mock_translate_file_cli.return_value = "auto_generated.txt"

    monkeypatch.setattr("sys.argv", ["translate_text.py", "input.txt", "pt"])

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0

    # Verify None was passed for output parameter (auto-generate)
    call_args = mock_translate_file_cli.call_args
    assert call_args[0] == ("input.txt", "pt", None)