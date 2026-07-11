# src/translator.py

from src.groq_client import get_completion
from src.language_detector import detect_language

def translate_text(text: str, target_language: str, source_language: str = None) -> str:
    """
    Translates text from source_language to target_language using Groq API.
    If source_language is not provided, it detects it automatically.
    """
    if not text or not text.strip():
        return ""
        
    # Auto-detect source language if not specified
    if not source_language:
        detection = detect_language(text)
        source_language = detection["language"]
        
    # If languages are the same, return text directly
    if source_language.lower() == target_language.lower():
        return text
        
    system_instruction = (
        f"You are a professional translator fluent in {source_language} and {target_language}. "
        f"Translate the provided text from {source_language} to {target_language}. "
        "Maintain the exact original tone, formatting, structure, paragraphs, and list layout of the text. "
        "Do not explain the translation, do not add introductory remarks (like 'Here is the translation:'), "
        "and do not write any additional notes. Output ONLY the translated text."
    )
    
    prompt = f"Text to translate:\n\n{text}"
    
    translated_text = get_completion(
        prompt=prompt,
        system_instruction=system_instruction,
        temperature=0.3
    )
    
    return translated_text
