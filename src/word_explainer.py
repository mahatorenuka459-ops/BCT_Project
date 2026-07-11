# src/word_explainer.py

from src.groq_client import get_completion
from src.language_detector import detect_language

def explain_difficult_words(text: str, target_language: str = None) -> str:
    """
    Identifies difficult, technical, or rare words in the text and explains them.
    
    Returns a Markdown formatted table or list containing the words and their definitions.
    If target_language is not provided, the explanation is in the detected source language.
    """
    if not text or not text.strip():
        return ""
        
    # Auto-detect language if target_language is not specified
    if not target_language:
        detection = detect_language(text)
        target_language = detection["language"]
        
    system_instruction = (
        f"You are a helpful educational tutor. Scan the provided text and identify any "
        f"difficult, rare, jargon, academic, or complex words/phrases.\n"
        f"For each word/phrase, provide a clear, plain-language explanation/definition in {target_language}.\n"
        "Format the output as a Markdown table with two columns: "
        "| Word / Phrase | Plain Language Explanation |.\n"
        "Ensure the definitions are simple and contextual.\n"
        "If there are no complex or difficult words in the text, respond with: "
        "'No complex words detected. The text uses simple vocabulary.'\n"
        "Do not write introductory text, remarks, or notes. Output ONLY the table or the no-words message."
    )
    
    prompt = f"Text to analyze:\n\n{text}"
    
    explanations = get_completion(
        prompt=prompt,
        system_instruction=system_instruction,
        temperature=0.2
    )
    
    return explanations
