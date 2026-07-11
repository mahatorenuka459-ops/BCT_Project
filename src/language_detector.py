# src/language_detector.py

import json
from langdetect import detect_langs
from src.lang_map import get_lang_name, get_iso_code
from src.groq_client import get_completion

def detect_language_local(text: str) -> tuple[str, float]:
    """
    Detects language locally using langdetect.
    Returns a tuple of (lang_name, confidence).
    """
    try:
        # Get top predictions
        predictions = detect_langs(text)
        if predictions:
            best_match = predictions[0]
            iso_code = best_match.lang
            confidence = best_match.prob
            lang_name = get_lang_name(iso_code)
            return lang_name, confidence
    except Exception:
        pass
    return "English", 0.0

def detect_language_llm(text: str) -> tuple[str, float]:
    """
    Detects language using Groq LLM.
    Returns a tuple of (lang_name, confidence).
    """
    system_instruction = (
        "You are an expert linguist. Your task is to identify the language of the provided text. "
        "You must respond ONLY with a JSON object in the following format: "
        '{"language_name": "Name of language", "confidence": 0.95}'
    )
    
    # Send a small snippet of the text to save tokens, max 1000 characters
    sample_text = text[:1000]
    prompt = f"Identify the language of this text:\n\n{sample_text}"
    
    try:
        response = get_completion(
            prompt=prompt,
            system_instruction=system_instruction,
            temperature=0.0,
            json_mode=True
        )
        data = json.loads(response)
        lang_name = data.get("language_name", "English")
        confidence = data.get("confidence", 1.0)
        
        # Normalize language name to match our supported map if possible
        normalized_name = get_lang_name(get_iso_code(lang_name))
        return normalized_name, confidence
    except Exception as e:
        print(f"LLM language detection failed: {e}")
        return "English", 0.0

def detect_language(text: str) -> dict:
    """
    Detects language of the input text using a hybrid approach.
    Returns a dictionary with 'language', 'iso_code', and 'confidence'.
    """
    if not text or not text.strip():
        return {"language": "English", "iso_code": "en", "confidence": 1.0}
        
    # Step 1: Try local detector
    lang_name, confidence = detect_language_local(text)
    
    # Step 2: If low confidence (< 0.8) or detected as English but might not be, verify with LLM
    if confidence < 0.8:
        llm_lang, llm_conf = detect_language_llm(text)
        if llm_conf > confidence:
            lang_name = llm_lang
            confidence = llm_conf
            
    return {
        "language": lang_name,
        "iso_code": get_iso_code(lang_name),
        "confidence": round(confidence, 2)
    }
