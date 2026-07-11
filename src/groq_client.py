# src/groq_client.py

import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_groq_client() -> Groq:
    """Instantiates and returns a Groq client using the API key from environment."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Groq API Key not found. Please set GROQ_API_KEY in your environment, .env file, or enter it in the Streamlit Sidebar.")
    
    return Groq(api_key=api_key)

def get_completion(
    prompt: str, 
    system_instruction: str = None, 
    model: str = "llama-3.3-70b-versatile",
    temperature: float = 0.3,
    json_mode: bool = False
) -> str:
    """
    Sends a request to Groq completion endpoint.
    Handles fallbacks and API errors.
    """
    client = get_groq_client()
    
    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.append({"role": "user", "content": prompt})
    
    # Define models to try in case of rate limits or failures
    models_to_try = [model, "llama-3.1-8b-instant", "gemma2-9b-it", "mixtral-8x7b-32768"]
    
    last_error = None
    for target_model in models_to_try:
        try:
            response_format = {"type": "json_object"} if json_mode else None
            
            chat_completion = client.chat.completions.create(
                messages=messages,
                model=target_model,
                temperature=temperature,
                response_format=response_format,
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            last_error = e
            # Print error or log, and retry with next model
            print(f"Error using model {target_model}: {e}. Trying fallback model...")
            continue
            
    raise Exception(f"Failed to generate response from Groq API after trying all models. Last error: {last_error}")
