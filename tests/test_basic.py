# tests/test_basic.py

import os
import pytest
from src.lang_map import get_iso_code, get_lang_name, get_flag
from src.utils import extract_text_from_file

def test_language_mappings():
    """Test that ISO conversion and emoji flag lookups function correctly."""
    assert get_iso_code("English") == "en"
    assert get_iso_code("Hindi") == "hi"
    assert get_iso_code("Bengali") == "bn"
    assert get_iso_code("French") == "fr"
    
    assert get_lang_name("en") == "English"
    assert get_lang_name("hi") == "Hindi"
    assert get_lang_name("bn") == "Bengali"
    assert get_lang_name("fr") == "French"
    
    # Handle country codes gracefully
    assert get_lang_name("en-US") == "English"
    assert get_lang_name("zh_CN") == "Chinese"
    
    assert get_flag("English") == "🇬🇧"
    assert get_flag("Hindi") == "🇮🇳"
    assert get_flag("French") == "🇫🇷"
    
    # Test fallback mapping
    assert get_iso_code("Atlantian") == "en"
    assert get_lang_name("xx") == "English"
    assert get_flag("Atlantian") == "🌐"

def test_text_file_extractor(tmp_path):
    """Test extracting text from plain text files."""
    test_content = "This is a test plain text content."
    temp_txt = tmp_path / "test.txt"
    temp_txt.write_text(test_content, encoding="utf-8")
    
    extracted = extract_text_from_file(str(temp_txt))
    assert extracted == test_content

def test_unsupported_file_extension(tmp_path):
    """Test that unsupported file extensions raise ValueError."""
    temp_invalid = tmp_path / "test.xyz"
    temp_invalid.write_text("dummy content")
    
    with pytest.raises(ValueError) as excinfo:
        extract_text_from_file(str(temp_invalid))
    assert "Unsupported file type" in str(excinfo.value)

def test_nonexistent_file():
    """Test that nonexistent file path raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        extract_text_from_file("nonexistent_file_path_12345.txt")
