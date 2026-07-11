# src/summarizer.py

from src.groq_client import get_completion
from src.language_detector import detect_language

def summarize_text(
    text: str, 
    target_language: str = None, 
    summary_type: str = "bullet"
) -> str:
    """
    Summarizes the text using the Groq API.
    
    Parameters:
    - text: The input text to summarize.
    - target_language: If provided, the summary will be returned in this language. 
                        Otherwise, it defaults to the detected input language.
    - summary_type: "bullet" (bullet points), "paragraph" (brief text), "detailed" (structured overview).
    """
    if not text or not text.strip():
        return ""
        
    # Auto-detect language if target_language is not specified
    if not target_language:
        detection = detect_language(text)
        target_language = detection["language"]
        
    # Build prompt and instruction based on type
    if summary_type == "paragraph":
        format_instruction = "Output a brief, cohesive paragraph summarizing the main points."
    elif summary_type == "detailed":
        format_instruction = "Output a detailed, structured overview of the text with headings and sub-points."
    else:  # default to bullet
        format_instruction = "Output the key takeaways as a clean list of bullet points."
        
    system_instruction = (
        f"You are a professional content summarizer. "
        f"Summarize the provided text in the {target_language} language. "
        f"Format requirement: {format_instruction} "
        "Focus on capturing the core arguments, facts, and conclusions. "
        "Do not write introductory text, do not explain the summary, and do not include personal opinions. "
        f"Output ONLY the summary text in {target_language}."
    )
    
    prompt = f"Text to summarize:\n\n{text}"
    
    summary = get_completion(
        prompt=prompt,
        system_instruction=system_instruction,
        temperature=0.3
    )
    
    return summary
