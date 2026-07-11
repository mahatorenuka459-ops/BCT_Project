# src/lang_map.py

# Supported languages mapping: Language Name -> ISO Code
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Arabic": "ar",
    "Chinese": "zh",
    "Russian": "ru",
    "Japanese": "ja",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Urdu": "ur",
    "Malayalam": "ml",
    "Nepali": "ne",
    "Sinhala": "si",
    "Portuguese": "pt",
    "Italian": "it",
    "Dutch": "nl",
    "Korean": "ko",
    "Turkish": "tr",
    "Vietnamese": "vi",
    "Thai": "th",
    "Indonesian": "id",
    "Swahili": "sw",
    "Persian": "fa",
    "Polish": "pl",
    "Ukrainian": "uk"
}

# Inverse mapping: ISO Code -> Language Name
ISO_TO_LANG = {v: k for k, v in LANGUAGES.items()}

# Emoji flag mappings for UI enhancement
FLAGS = {
    "English": "🇬🇧",
    "Hindi": "🇮🇳",
    "Bengali": "🇧🇩",
    "French": "🇫🇷",
    "German": "🇩🇪",
    "Spanish": "🇪🇸",
    "Arabic": "🇸🇦",
    "Chinese": "🇨🇳",
    "Russian": "🇷🇺",
    "Japanese": "🇯🇵",
    "Tamil": "🇮🇳",
    "Telugu": "🇮🇳",
    "Marathi": "🇮🇳",
    "Gujarati": "🇮🇳",
    "Urdu": "🇵🇰",
    "Malayalam": "🇮🇳",
    "Nepali": "🇳🇵",
    "Sinhala": "🇱🇰",
    "Portuguese": "🇵🇹",
    "Italian": "🇮🇹",
    "Dutch": "🇳🇱",
    "Korean": "🇰🇷",
    "Turkish": "🇹🇷",
    "Vietnamese": "🇻🇳",
    "Thai": "🇹🇭",
    "Indonesian": "🇮🇩",
    "Swahili": "🇰🇪",
    "Persian": "🇮🇷",
    "Polish": "🇵🇱",
    "Ukrainian": "🇺🇦"
}

def get_iso_code(lang_name: str) -> str:
    """Returns the ISO 639-1 code for a given language name."""
    return LANGUAGES.get(lang_name, "en")

def get_lang_name(iso_code: str) -> str:
    """Returns the full language name for a given ISO 639-1 code."""
    # Handle codes that might have country suffixes like 'en-US' or 'zh-CN'
    base_code = iso_code.split('-')[0].split('_')[0].lower()
    return ISO_TO_LANG.get(base_code, "English")

def get_flag(lang_name: str) -> str:
    """Returns the emoji flag for a given language name."""
    return FLAGS.get(lang_name, "🌐")
