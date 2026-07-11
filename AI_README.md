# 🌐 Multilingual AI Translator + Summarizer

A web app that lets you **upload or paste text** in Hindi, Bengali, English, French, and 25+ other languages, then:

- 🌍 **Detect** the language automatically
- 🔁 **Translate** it into any supported language
- 📝 **Summarize** long text into a short summary
- ✏️ **Simplify** text into plain, easy-to-read language
- 📖 **Explain difficult words** in plain-language definitions

Powered by **[mBART-50](https://huggingface.co/facebook/mbart-large-50-many-to-many-mmt)** (`facebook/mbart-large-50-many-to-many-mmt`), a many-to-many multilingual translation model from Meta AI covering 50 languages.

---

## ✨ Features

| Feature | Description |
|---|---|
| **File upload** | Supports `.txt`, `.pdf`, `.docx` |
| **Language detection** | Auto-detects input language with a confidence score |
| **Translation** | Many-to-many translation across 30 curated languages (full mBART-50 list extendable) |
| **Summarization** | Pivot-translation + `facebook/bart-large-cnn` for accurate summaries in any language |
| **Simplification** | Shortens long sentences and swaps rare words for simpler synonyms |
| **Difficult word explainer** | Flags rare/complex words and explains them in plain English or the original language |

---

## 🗂️ Project Structure

```
multilingual-ai-translator/
├── app.py                    # Streamlit web UI (main entry point)
├── cli.py                    # Command-line interface (alternative to the UI)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── src/
│   ├── __init__.py
│   ├── lang_map.py           # Language name <-> ISO code <-> mBART code mapping
│   ├── language_detector.py  # Auto-detects input language
│   ├── translator.py         # mBART-50 translation engine
│   ├── summarizer.py         # English-pivot summarization
│   ├── simplifier.py         # Sentence splitting + word simplification
│   ├── word_explainer.py     # Difficult-word detection + WordNet definitions
│   └── utils.py              # File readers (txt / pdf / docx)
├── data/
│   └── sample_uploads/
│       └── sample_hindi.txt  # Example file to try the app with
└── tests/
    └── test_basic.py         # Fast unit tests (no model download needed)
```

---

## ⚙️ How It Works

```
                 ┌─────────────────┐
   Upload/Paste  │   Input Text     │
   ────────────► │  (any language)  │
                 └────────┬─────────┘
                          │
                 ┌────────▼─────────┐
                 │ Language Detector │  (langdetect)
                 └────────┬─────────┘
                          │
        ┌─────────────────┼──────────────────┬────────────────┐
        ▼                 ▼                  ▼                ▼
   ┌─────────┐      ┌───────────┐      ┌────────────┐   ┌────────────┐
   │Translate │      │Summarize  │      │ Simplify   │   │  Explain   │
   │ (mBART)  │      │(pivot via │      │ (pivot via │   │  Words     │
   │          │      │ English + │      │  English)  │   │ (WordNet + │
   │          │      │ BART-CNN) │      │            │   │  pivot)    │
   └─────────┘      └───────────┘      └────────────┘   └────────────┘
```

Since mBART-50 is a **translation-only** model, summarization/simplification/word-explanation all reuse it as a **pivot**: non-English text is translated to English first, processed with the right tool, then (optionally) translated back — so every feature works uniformly across all 30 supported languages.

---

## 🚀 Setup

### 1. Clone / download the project
```bash
cd multilingual-ai-translator
```

### 2. Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

> ⚠️ First run downloads the mBART-50 model (~2.4 GB) and BART-CNN (~1.6 GB) from Hugging Face — this requires internet access and may take a few minutes. They're cached locally afterward.

### 4. Run the web app
```bash
streamlit run app.py
```
Then open the URL Streamlit prints (usually `http://localhost:8501`).

### 5. (Optional) Use the CLI instead
```bash
python cli.py --file data/sample_uploads/sample_hindi.txt --action translate --target English
python cli.py --text "यह एक परीक्षण है" --action summarize
python cli.py --file report.pdf --action explain
```

---

## 🧪 Running Tests
```bash
pip install pytest
pytest tests/ -v
```
`tests/test_basic.py` covers language mapping and detection logic and runs in under a second — it does **not** download the large translation model, so it's safe to run in CI.

---

## 🌍 Supported Languages (default set)

English, Hindi, Bengali, French, German, Spanish, Arabic, Chinese, Russian, Japanese, Tamil, Telugu, Marathi, Gujarati, Urdu, Malayalam, Nepali, Sinhala, Portuguese, Italian, Dutch, Korean, Turkish, Vietnamese, Thai, Indonesian, Swahili, Persian, Polish, Ukrainian.

Add more by extending the `LANGUAGES` dictionary in `src/lang_map.py` — mBART-50 supports 50 languages total; see the [model card](https://huggingface.co/facebook/mbart-large-50-many-to-many-mmt) for the full list of codes.

---

## 🔧 Models Used

| Task | Model |
|---|---|
| Translation | `facebook/mbart-large-50-many-to-many-mmt` |
| Summarization | `facebook/bart-large-cnn` |
| Language detection | `langdetect` (statistical n-gram detector) |
| Word definitions | NLTK WordNet |

---

## 🛣️ Roadmap / Ideas for Extension
- [ ] Add speech-to-text input (e.g. Whisper) for spoken translation
- [ ] Add OCR support for scanned/image-based PDFs
- [ ] Fine-tune a dedicated multilingual summarization model to avoid the English pivot
- [ ] Add a REST API (FastAPI) wrapper around `src/` for integration into other apps
- [ ] Deploy to Streamlit Community Cloud / Hugging Face Spaces

---

## 📄 License
This project is provided as a starting template — add your preferred license (MIT recommended) before distribution.
