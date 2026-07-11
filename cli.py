# cli.py

import os
import argparse
import sys

# Reconfigure stdout/stderr to use UTF-8 encoding (resolves Windows encoding issues with emojis)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Ensure current directory is in system path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils import extract_text_from_file
from src.language_detector import detect_language
from src.translator import translate_text
from src.summarizer import summarize_text
from src.simplifier import simplify_text
from src.word_explainer import explain_difficult_words

def main():
    parser = argparse.ArgumentParser(description="🌐 Multilingual AI Translator & Summarizer CLI")
    
    # Text source
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Plain text to process")
    group.add_argument("--file", type=str, help="Path to a text (.txt), PDF (.pdf), or Word (.docx) file")
    
    # Processing actions
    parser.add_argument(
        "--action", 
        type=str, 
        required=True, 
        choices=["detect", "translate", "summarize", "simplify", "explain"],
        help="Action to perform on the text"
    )
    
    # Parameters
    parser.add_argument("--target", type=str, help="Target language (required for 'translate')")
    parser.add_argument(
        "--summary-type", 
        type=str, 
        choices=["bullet", "paragraph", "detailed"], 
        default="bullet",
        help="Summary format (for 'summarize' action)"
    )

    args = parser.parse_args()
    
    # 1. Retrieve the text
    if args.text:
        text = args.text
    else:
        try:
            text = extract_text_from_file(args.file)
        except Exception as e:
            print(f"❌ Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
            
    if not text.strip():
        print("❌ Error: Input text is empty.", file=sys.stderr)
        sys.exit(1)
        
    # 2. Perform the action
    try:
        if args.action == "detect":
            result = detect_language(text)
            print("\n🔍 Language Detection Result:")
            print(f"  • Language: {result['language']}")
            print(f"  • ISO Code: {result['iso_code']}")
            print(f"  • Confidence: {result['confidence'] * 100}%")
            
        elif args.action == "translate":
            if not args.target:
                print("❌ Error: --target language is required for 'translate' action.", file=sys.stderr)
                sys.exit(1)
            translated = translate_text(text, target_language=args.target)
            print(f"\n🔁 Translated Text ({args.target}):")
            print("-" * 50)
            print(translated)
            print("-" * 50)
            
        elif args.action == "summarize":
            summary = summarize_text(text, target_language=args.target, summary_type=args.summary_type)
            lang_label = args.target if args.target else "Original Language"
            print(f"\n📝 Summary ({lang_label} - {args.summary_type} format):")
            print("-" * 50)
            print(summary)
            print("-" * 50)
            
        elif args.action == "simplify":
            simplified = simplify_text(text, target_language=args.target)
            lang_label = args.target if args.target else "Original Language"
            print(f"\n✏️ Simplified Text ({lang_label}):")
            print("-" * 50)
            print(simplified)
            print("-" * 50)
            
        elif args.action == "explain":
            explanations = explain_difficult_words(text, target_language=args.target)
            lang_label = args.target if args.target else "Original Language"
            print(f"\n📖 Difficult Words Explained ({lang_label}):")
            print(explanations)
            
    except Exception as e:
        print(f"❌ Error executing action '{args.action}': {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
