# api/index.py
# Vercel serverless entry point — exports `app` (FastAPI/ASGI handler)

import sys
import os

# Ensure the project root is in path so `src.*` imports resolve
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional

from src.language_detector import detect_language
from src.translator import translate_text
from src.summarizer import summarize_text
from src.simplifier import simplify_text
from src.word_explainer import explain_difficult_words
from src.lang_map import LANGUAGES, get_flag

# ---------------------------------------------------------------------------
# FastAPI app — Vercel looks for a top-level variable named `app`
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Multilingual AI Translator & Summarizer",
    description="State-of-the-art multilingual AI powered by Groq Cloud",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class TextRequest(BaseModel):
    text: str
    model: Optional[str] = "llama-3.3-70b-versatile"


class TranslateRequest(TextRequest):
    target_language: str
    source_language: Optional[str] = None


class SummarizeRequest(TextRequest):
    summary_type: Optional[str] = "bullet"   # bullet | paragraph | detailed
    target_language: Optional[str] = None


class SimplifyRequest(TextRequest):
    target_language: Optional[str] = None


class ExplainRequest(TextRequest):
    target_language: Optional[str] = None


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def root():
    """Landing page with API documentation links."""
    languages_list = "".join(
        f"<li>{get_flag(lang)} {lang}</li>" for lang in sorted(LANGUAGES.keys())
    )
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Multilingual AI Translator &amp; Summarizer</title>
        <meta name="description" content="State-of-the-art multilingual AI powered by Groq Cloud — translate, summarize, simplify text in {len(LANGUAGES)}+ languages."/>
        <link rel="preconnect" href="https://fonts.googleapis.com"/>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet"/>
        <style>
            *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                font-family: 'Plus Jakarta Sans', sans-serif;
                background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #020617 60%);
                min-height: 100vh;
                color: #f8fafc;
            }}
            .hero {{
                max-width: 860px;
                margin: 0 auto;
                padding: 5rem 2rem 3rem;
                text-align: center;
            }}
            h1 {{
                font-family: 'Outfit', sans-serif;
                font-size: clamp(2rem, 5vw, 3.2rem);
                font-weight: 800;
                background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                line-height: 1.15;
                margin-bottom: 1rem;
            }}
            .subtitle {{
                color: #94a3b8;
                font-size: 1.1rem;
                max-width: 560px;
                margin: 0 auto 3rem;
            }}
            .cards {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1.2rem;
                margin-bottom: 3rem;
            }}
            .card {{
                background: rgba(30,41,59,0.5);
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 16px;
                padding: 1.6rem;
                backdrop-filter: blur(12px);
                transition: transform .2s, border-color .2s;
            }}
            .card:hover {{ transform: translateY(-4px); border-color: rgba(99,102,241,.4); }}
            .card .icon {{ font-size: 2rem; margin-bottom: .6rem; }}
            .card h3 {{ font-family: 'Outfit', sans-serif; font-size: 1rem; font-weight: 600; color: #e2e8f0; margin-bottom: .4rem; }}
            .card p {{ font-size: .82rem; color: #64748b; }}
            .btn {{
                display: inline-block;
                background: linear-gradient(135deg, #4f46e5, #7c3aed);
                color: #fff;
                text-decoration: none;
                padding: .85rem 2.2rem;
                border-radius: 12px;
                font-weight: 600;
                font-size: 1rem;
                box-shadow: 0 4px 14px rgba(99,102,241,.4);
                transition: transform .2s, box-shadow .2s;
                margin: .4rem;
            }}
            .btn:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(99,102,241,.6); }}
            .btn.outline {{
                background: transparent;
                border: 1px solid rgba(99,102,241,.5);
                color: #a5b4fc;
                box-shadow: none;
            }}
            .endpoint-section {{
                max-width: 860px;
                margin: 0 auto 4rem;
                padding: 0 2rem;
            }}
            .endpoint-section h2 {{
                font-family: 'Outfit', sans-serif;
                font-size: 1.4rem;
                font-weight: 700;
                color: #e2e8f0;
                margin-bottom: 1rem;
            }}
            .endpoint {{
                background: rgba(15,23,42,.6);
                border: 1px solid rgba(255,255,255,.06);
                border-radius: 12px;
                padding: 1rem 1.4rem;
                margin-bottom: .8rem;
                display: flex;
                align-items: center;
                gap: 1rem;
            }}
            .method {{
                font-size: .78rem;
                font-weight: 700;
                padding: .25rem .6rem;
                border-radius: 6px;
                font-family: monospace;
                min-width: 46px;
                text-align: center;
            }}
            .get {{ background: rgba(16,185,129,.15); color: #34d399; }}
            .post {{ background: rgba(99,102,241,.15); color: #a5b4fc; }}
            .path {{ font-family: monospace; color: #cbd5e1; font-size: .9rem; }}
            .desc {{ color: #64748b; font-size: .82rem; margin-left: auto; }}
            footer {{
                text-align: center;
                color: #475569;
                font-size: .82rem;
                padding: 2rem;
                border-top: 1px solid rgba(255,255,255,.05);
            }}
        </style>
    </head>
    <body>
        <div class="hero">
            <h1>🌐 Multilingual AI<br/>Translator &amp; Summarizer</h1>
            <p class="subtitle">State-of-the-art language detection, translation, summarization, and simplification — powered by Groq Cloud LLMs at lightning speed.</p>
            <div class="cards">
                <div class="card"><div class="icon">🔁</div><h3>Translate</h3><p>Translate across {len(LANGUAGES)}+ languages with tone preservation</p></div>
                <div class="card"><div class="icon">📝</div><h3>Summarize</h3><p>Bullet points, paragraphs, or detailed structured overviews</p></div>
                <div class="card"><div class="icon">✏️</div><h3>Simplify</h3><p>Rewrite complex text into plain, accessible language</p></div>
                <div class="card"><div class="icon">📖</div><h3>Explain</h3><p>Identify and explain difficult vocabulary in any language</p></div>
            </div>
            <a href="/docs" class="btn">📚 API Documentation</a>
            <a href="/redoc" class="btn outline">📖 ReDoc</a>
        </div>
        <div class="endpoint-section">
            <h2>Available Endpoints</h2>
            <div class="endpoint"><span class="method get">GET</span><span class="path">/</span><span class="desc">This page</span></div>
            <div class="endpoint"><span class="method post">POST</span><span class="path">/api/detect</span><span class="desc">Detect language of text</span></div>
            <div class="endpoint"><span class="method post">POST</span><span class="path">/api/translate</span><span class="desc">Translate text to target language</span></div>
            <div class="endpoint"><span class="method post">POST</span><span class="path">/api/summarize</span><span class="desc">Summarize text (bullet/paragraph/detailed)</span></div>
            <div class="endpoint"><span class="method post">POST</span><span class="path">/api/simplify</span><span class="desc">Simplify complex text</span></div>
            <div class="endpoint"><span class="method post">POST</span><span class="path">/api/explain</span><span class="desc">Explain difficult words/vocabulary</span></div>
            <div class="endpoint"><span class="method get">GET</span><span class="path">/api/languages</span><span class="desc">List all supported languages</span></div>
            <div class="endpoint"><span class="method get">GET</span><span class="path">/health</span><span class="desc">Health check / API status</span></div>
        </div>
        <footer>Made with ❤️ using FastAPI &amp; Groq Cloud • Multilingual AI Infrastructure</footer>
    </body>
    </html>
    """


@app.get("/health")
async def health():
    """Health check endpoint."""
    try:
        from src.groq_client import get_groq_client
        get_groq_client()
        return {"status": "ok", "groq": "connected"}
    except Exception as e:
        return JSONResponse(status_code=503, content={"status": "error", "detail": str(e)})


@app.get("/api/languages")
async def list_languages():
    """Return all supported languages with flags."""
    return {
        "count": len(LANGUAGES),
        "languages": {lang: get_flag(lang) for lang in sorted(LANGUAGES.keys())}
    }


@app.post("/api/detect")
async def detect(req: TextRequest):
    """Detect the language of the provided text."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text field must not be empty.")
    try:
        result = detect_language(req.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/translate")
async def translate(req: TranslateRequest):
    """Translate text to the specified target language."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text field must not be empty.")
    if not req.target_language:
        raise HTTPException(status_code=400, detail="target_language is required.")
    try:
        result = translate_text(
            req.text,
            target_language=req.target_language,
            source_language=req.source_language,
        )
        return {"translated_text": result, "target_language": req.target_language}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/summarize")
async def summarize(req: SummarizeRequest):
    """Summarize text. summary_type: bullet | paragraph | detailed"""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text field must not be empty.")
    try:
        result = summarize_text(
            req.text,
            target_language=req.target_language,
            summary_type=req.summary_type or "bullet",
        )
        return {"summary": result, "summary_type": req.summary_type}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/simplify")
async def simplify(req: SimplifyRequest):
    """Rewrite text in plain, simplified language."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text field must not be empty.")
    try:
        result = simplify_text(req.text, target_language=req.target_language)
        return {"simplified_text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/explain")
async def explain(req: ExplainRequest):
    """Identify and explain difficult vocabulary in the text."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text field must not be empty.")
    try:
        result = explain_difficult_words(req.text, target_language=req.target_language)
        return {"explanation": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
