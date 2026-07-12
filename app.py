# app.py

import os
import sys
import tempfile
import streamlit as st

# Ensure current directory is in system path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils import extract_text_from_file
from src.language_detector import detect_language
from src.translator import translate_text
from src.summarizer import summarize_text
from src.simplifier import simplify_text
from src.word_explainer import explain_difficult_words
from src.lang_map import LANGUAGES, get_flag, get_iso_code

# Set page configuration with premium title and icon
st.set_page_config(
    page_title="Multilingual AI Translator + Summarizer",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom premium CSS for styling, dark mode, glassmorphism, and custom buttons
st.markdown("""
<style>
/* Import modern fonts */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif;
}

/* Background gradient matching modern dashboards */
.stApp {
    background: radial-gradient(circle at 50% 50%, #0F172A 0%, #020617 100%);
    color: #F8FAFC;
}

/* Header Container */
.header-card {
    background: rgba(30, 41, 59, 0.4);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.header-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    letter-spacing: -0.025em;
}

.header-subtitle {
    color: #94A3B8;
    font-size: 1.1rem;
    font-weight: 400;
}

/* Styled Container Box */
.content-box {
    background: rgba(30, 41, 59, 0.25);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}

/* Gradient buttons with micro-animation */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.025em !important;
    box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.4) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    width: 100% !important;
    cursor: pointer;
}

div.stButton > button:first-child:hover {
    background: linear-gradient(135deg, #5E52FF 0%, #8E52FF 100%);
    box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.6) !important;
    transform: translateY(-2px);
}

div.stButton > button:first-child:active {
    transform: translateY(0);
}

/* Styled Sidebar */
[data-testid="stSidebar"] {
    background-color: #030712 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

/* Customize Text Inputs & Areas */
.stTextArea textarea {
    background-color: rgba(15, 23, 42, 0.65) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #F8FAFC !important;
    border-radius: 12px !important;
    font-size: 0.95rem !important;
}

.stTextArea textarea:focus {
    border-color: #8B5CF6 !important;
    box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.25) !important;
}

/* Customize Select Boxes */
div[data-baseweb="select"] {
    background-color: rgba(15, 23, 42, 0.65) !important;
    border-radius: 10px !important;
}

/* Custom File Uploader */
.stFileUploader {
    background: rgba(30, 41, 59, 0.15);
    border: 2px dashed rgba(99, 102, 241, 0.25) !important;
    border-radius: 14px;
    padding: 1.5rem;
    transition: border 0.3s ease;
}

.stFileUploader:hover {
    border-color: rgba(99, 102, 241, 0.5) !important;
}

/* Status indicator badge */
.status-badge {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #34D399;
    padding: 0.3rem 0.8rem;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
}

.status-badge.inactive {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #F87171;
}

/* Footer Section */
.footer-text {
    text-align: center;
    color: #64748B;
    font-size: 0.85rem;
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
}
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("### ⚙️ Engine Control Panel")
    
    # Custom API Key input
    api_key_override = st.text_input(
        "Groq API Key Override:",
        value=os.getenv("GROQ_API_KEY", ""),
        type="password",
        help="Paste your Groq API key here. By default, it loads from the environment or .env file."
    )
    
    # Update environment variable dynamically
    if api_key_override:
        os.environ["GROQ_API_KEY"] = api_key_override
        
    # Model Selection
    model_choice = st.selectbox(
        "Select LLM Engine:",
        options=[
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "gemma2-9b-it",
            "mixtral-8x7b-32768"
        ],
        index=0,
        help="Select the model target for processing. llama-3.3-70b offers superior quality, while llama-3.1-8b is faster."
    )
    
    st.markdown("---")
    
    # Connection Check
    st.markdown("### ⚡ Connection Status")
    try:
        from src.groq_client import get_groq_client
        client = get_groq_client()
        # Trigger minor request to check auth
        st.markdown(
            '<div class="status-badge">🟢 Groq Cloud Active</div>', 
            unsafe_allow_html=True
        )
    except Exception as e:
        st.markdown(
            '<div class="status-badge inactive">🔴 API Connection Error</div>', 
            unsafe_allow_html=True
        )
        st.warning(f"Error details: {e}")
        
    st.markdown("---")
    st.markdown("### 🌍 Available Languages")
    st.info(f"Currently supporting {len(LANGUAGES)} curated languages including Hindi, Bengali, English, French, Spanish, Russian, Chinese, Japanese, and more.")

# ----------------- MAIN UI -----------------

# Beautiful Glass Header
st.markdown("""
<div class="header-card">
    <div class="header-title">🌐 Multilingual AI Translator & Summarizer</div>
    <div class="header-subtitle">State-of-the-Art Language Detection, Translation, Summarization, and Text Simplification using Groq Cloud</div>
</div>
""", unsafe_allow_html=True)

# Application Layout
col_left, col_right = st.columns([1, 1], gap="large")

# Text Extraction Helper
def process_uploaded_file(uploaded_file):
    suffix = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name
    try:
        extracted = extract_text_from_file(temp_path)
        return extracted
    except Exception as err:
        st.error(f"Error parsing file: {err}")
        return ""
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

with col_left:
    st.markdown('### 📝 Source Content Input', unsafe_allow_html=True)
    
    # Input Mode Tabs (Paste Text vs File Upload)
    input_tab1, input_tab2 = st.tabs(["✍️ Paste Text", "📤 Upload File"])
    
    source_text = ""
    
    with input_tab1:
        source_text_area = st.text_area(
            "Enter text to analyze/translate:",
            height=280,
            placeholder="Type or paste your text here (in Hindi, English, French, etc.)..."
        )
        if source_text_area:
            source_text = source_text_area
            
    with input_tab2:
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["txt", "pdf", "docx"],
            help="Supports standard text, PDFs, and Word documents."
        )
        if uploaded_file:
            with st.spinner("Extracting file text..."):
                source_text = process_uploaded_file(uploaded_file)
            st.success(f"Successfully extracted content from '{uploaded_file.name}'")
            # Text preview
            st.text_area("Extracted file preview:", value=source_text[:1000] + ("..." if len(source_text) > 1000 else ""), height=150, disabled=True)

    # If we have source text, run background language detection immediately
    detected_lang = "Unknown"
    detected_iso = "en"
    detected_conf = 0.0
    
    if source_text.strip():
        with st.spinner("Detecting language..."):
            try:
                detection = detect_language(source_text)
                detected_lang = detection["language"]
                detected_iso = detection["iso_code"]
                detected_conf = detection["confidence"]
            except Exception as e:
                pass
                
        # Draw Language detection badge
        st.markdown(f"""
        <div class="content-box" style="margin-top: 1rem; padding: 1rem;">
            🔍 <b>Detected Language:</b> {detected_lang} {get_flag(detected_lang)} 
            <span style="color: #64748B; margin-left: 10px;">| ISO: {detected_iso} | Confidence: {detected_conf * 100:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

    # Action parameters
    st.markdown("### 🛠️ Choose Action & Parameters")
    
    action = st.selectbox(
        "Select Action:",
        options=["Translate", "Summarize", "Simplify", "Explain Difficult Words"],
        index=0
    )
    
    target_language = "English"
    summary_type = "bullet"
    
    if action == "Translate":
        # Let's populate the target languages
        lang_list = sorted(list(LANGUAGES.keys()))
        default_index = lang_list.index("Spanish") if "Spanish" in lang_list else 0
        target_language = st.selectbox(
            "Select Target Language:",
            options=lang_list,
            index=default_index,
            format_func=lambda x: f"{get_flag(x)} {x}"
        )
        
    elif action == "Summarize":
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            summary_type = st.selectbox(
                "Summary Style:",
                options=["Key Bullet Points", "Cohesive Paragraph", "Detailed Structured Overview"],
                index=0
            )
            # Map selection to internal names
            summary_mapping = {
                "Key Bullet Points": "bullet",
                "Cohesive Paragraph": "paragraph",
                "Detailed Structured Overview": "detailed"
            }
            summary_type = summary_mapping[summary_type]
        with col_s2:
            lang_list = ["Original Language"] + sorted(list(LANGUAGES.keys()))
            target_lang_sel = st.selectbox(
                "Output Language (Optional):",
                options=lang_list,
                index=0
            )
            target_language = None if target_lang_sel == "Original Language" else target_lang_sel
            
    elif action == "Simplify":
        lang_list = ["Original Language"] + sorted(list(LANGUAGES.keys()))
        target_lang_sel = st.selectbox(
            "Output Language (Optional):",
            options=lang_list,
            index=0
        )
        target_language = None if target_lang_sel == "Original Language" else target_lang_sel
        
    elif action == "Explain Difficult Words":
        lang_list = ["Original Language"] + sorted(list(LANGUAGES.keys()))
        target_lang_sel = st.selectbox(
            "Definitions Language (Optional):",
            options=lang_list,
            index=0
        )
        target_language = None if target_lang_sel == "Original Language" else target_lang_sel
        
    # Trigger processing
    run_button = st.button("🔥 Process Content")

with col_right:
    st.markdown('### ⚡ Analysis & Output', unsafe_allow_html=True)
    
    # Placeholder box before processing
    if not run_button:
        st.markdown("""
        <div class="content-box" style="height: 480px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; color: #64748B;">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">⚙️</div>
            <div style="font-size: 1.2rem; font-weight: 600; color: #94A3B8;">System Ready</div>
            <div style="font-size: 0.9rem; max-width: 320px; margin-top: 0.5rem;">Provide input text on the left, choose your settings, and click "Process Content" to run LLM diagnostics.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        if not source_text.strip():
            st.error("Please enter some text or upload a file first!")
        else:
            with st.spinner(f"Running '{action}' engine on {model_choice}..."):
                try:
                    result_text = ""
                    
                    if action == "Translate":
                        result_text = translate_text(
                            source_text, 
                            target_language=target_language,
                            source_language=detected_lang if detected_lang != "Unknown" else None
                        )
                        header_label = f"🔁 Translation ({target_language})"
                        
                    elif action == "Summarize":
                        result_text = summarize_text(
                            source_text,
                            target_language=target_language,
                            summary_type=summary_type
                        )
                        label = target_language if target_language else detected_lang
                        header_label = f"📝 Summary ({label})"
                        
                    elif action == "Simplify":
                        result_text = simplify_text(
                            source_text,
                            target_language=target_language
                        )
                        label = target_language if target_language else detected_lang
                        header_label = f"✏️ Simplified Content ({label})"
                        
                    elif action == "Explain Difficult Words":
                        result_text = explain_difficult_words(
                            source_text,
                            target_language=target_language
                        )
                        label = target_language if target_language else detected_lang
                        header_label = f"📖 Vocabulary Explanations ({label})"
                        
                    # Output presentation in card
                    st.markdown(f"#### {header_label}")
                    st.markdown(f'<div class="content-box" style="background: rgba(15, 23, 42, 0.4); border-color: rgba(99, 102, 241, 0.2); min-height: 380px;">', unsafe_allow_html=True)
                    st.markdown(result_text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Download Actions
                    col_dl1, col_dl2 = st.columns(2)
                    with col_dl1:
                        st.download_button(
                            label="📥 Download Output (.txt)",
                            data=result_text,
                            file_name=f"groq_{action.lower().replace(' ', '_')}.txt",
                            mime="text/plain"
                        )
                    with col_dl2:
                        st.download_button(
                            label="📥 Download Output (.md)",
                            data=f"# {header_label}\n\n{result_text}",
                            file_name=f"groq_{action.lower().replace(' ', '_')}.md",
                            mime="text/markdown"
                        )
                        
                except Exception as e:
                    st.error(f"An error occurred during API processing: {e}")
                    st.exception(e)

# Footer
st.markdown("""
<div class="footer-text">
    Made with ❤️ using Streamlit & Groq API • High-speed Multilingual AI Infrastructure
</div>
""", unsafe_allow_html=True)




