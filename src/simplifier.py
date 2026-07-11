# src/simplifier.py

from src.groq_client import get_completion
from src.language_detector import detect_language

def simplify_text(text: str, target_language: str = None) -> str:
    """
    Simplifies the text using the Groq API.
    
    Rewrites complex sentences to be shorter, swaps difficult/rare vocabulary 
    with plain-language synonyms, and structures the prose for maximum readability.
    
    If target_language is not provided, the output remains in the detected source language.
    """
    if not text or not text.strip():
        return ""
        
    # Auto-detect language if target_language is not specified
    if not target_language:
        detection = detect_language(text)
        target_language = detection["language"]
        
    system_instruction = (
        f"You are an expert communicator specializing in Plain Language writing. "
        f"Your task is to simplify the provided text and output it in {target_language}. "
        "Rules for simplification:\n"
        "1. Split long, complex sentences into shorter, punchy ones.\n"
        "2. Replace obscure, technical, or academic terms with simple, everyday vocabulary.\n"
        "3. Maintain the core meaning and details of the original text, but make it extremely easy to read.\n"
        "4. Keep the same general paragraph structure where appropriate.\n"
        "5. Output ONLY the simplified text. Do not add introductions, explanations, or notes."
    )
    
    prompt = f"Text to simplify:\n\n{text}"
    
    simplified = get_completion(
        prompt=prompt,
        system_instruction=system_instruction,
        temperature=0.3
    )
    
    return simplified
