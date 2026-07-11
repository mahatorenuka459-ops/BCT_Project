# src/utils.py

import os
from pypdf import PdfReader
from docx import Document

def read_text_file(file_path: str) -> str:
    """Reads a plain text file."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def read_pdf_file(file_path: str) -> str:
    """Reads and extracts text from a PDF file using pypdf."""
    reader = PdfReader(file_path)
    text = []
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text.append(extracted)
    return "\n".join(text)

def read_docx_file(file_path: str) -> str:
    """Reads and extracts text from a DOCX file using python-docx."""
    doc = Document(file_path)
    text = []
    for para in doc.paragraphs:
        if para.text:
            text.append(para.text)
    return "\n".join(text)

def extract_text_from_file(file_path: str) -> str:
    """
    Extracts text from a file based on its extension.
    Supports .txt, .pdf, and .docx.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".txt":
        return read_text_file(file_path)
    elif ext == ".pdf":
        return read_pdf_file(file_path)
    elif ext == ".docx":
        return read_docx_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}. Only .txt, .pdf, and .docx are supported.")
