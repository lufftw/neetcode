#!/usr/bin/env python3
# =============================================================================
# Standalone Translation Script
# =============================================================================
# Translates an existing Markmap without running the full pipeline.
# Useful for re-translating or translating manually edited files.
#
# Usage:
#   python translate_only.py                          # Translate latest version
#   python translate_only.py --input path/to/file.md  # Translate specific file
#   python translate_only.py --source en --target zh-TW
#
# =============================================================================

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config_loader import ConfigLoader, load_config, request_api_keys
from src.agents.translator import TranslatorAgent
from src.output.html_converter import MarkMapHTMLConverter


def find_latest_english_output(config: dict) -> Path | None:
    """Find the latest English output from version history or final output."""
    converter = MarkMapHTMLConverter(config)
    
    # Try version history first
    latest = converter._get_latest_version_path("en")
    if latest and latest.exists():
        return latest
    
    # Try final output directory
    output_config = config.get("output", {})
    naming = output_config.get("naming", {})
    prefix = naming.get("prefix", "neetcode")
    template = naming.get("template", "{prefix}_ontology_agent_evolved_{lang}")
    filename = template.format(prefix=prefix, lang="en") + ".md"
    
    final_dirs = output_config.get("final_dirs", {})
    base_dir = Path(__file__).parent
    md_dir = (base_dir / final_dirs.get("markdown", "outputs/final")).resolve()
    
    final_path = md_dir / filename
    if final_path.exists():
        return final_path
    
    return None


def translate_file(
    input_path: Path,
    output_path: Path,
    source_lang: str,
    target_lang: str,
    model: str,
    config: dict,
) -> str:
    """Translate a file and save the result."""
    print(f"\n📄 Input: {input_path}")
    print(f"🌐 Translation: {source_lang} → {target_lang}")
    print(f"🤖 Model: {model}")
    
    # Read input
    content = input_path.read_text(encoding="utf-8")
    print(f"   Read {len(content)} chars, {len(content.splitlines())} lines")
    
    # Create translator
    translator = TranslatorAgent(
        source_language=source_lang,
        target_language=target_lang,
        model=model,
        config=config,
    )
    
    # Translate
    print("\n⏳ Translating...")
    translated = translator.translate(content, "general")
    print(f"   ✓ Translated to {len(translated)} chars")
    
    # Save output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(translated, encoding="utf-8")
    print(f"\n💾 Saved: {output_path}")
    
    return translated


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Translate Markmap without running full pipeline"
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        default=None,
        help="Input file to translate (default: latest English output)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output file path (default: auto-generate based on input)"
    )
    parser.add_argument(
        "--source", "-s",
        type=str,
        default="en",
        help="Source language (default: en)"
    )
    parser.add_argument(
        "--target", "-t",
        type=str,
        default="zh-TW",
        help="Target language (default: zh-TW)"
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default=None,
        help="Model to use (default: from config)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to config file"
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Also generate HTML output"
    )
    
    args = parser.parse_args()
    
    try:
        print("\n" + "=" * 60)
        print("🌐 Markmap Translation Tool")
        print("=" * 60)
        
        # Load config
        config = load_config(args.config)
        
        # Request API key
        request_api_keys(["openai"])
        
        if not ConfigLoader.has_api_key("openai"):
            print("\n❌ Error: OpenAI API key is required.")
            return 1
        
        # Determine input file
        if args.input:
            input_path = Path(args.input)
            if not input_path.exists():
                print(f"\n❌ Error: Input file not found: {args.input}")
                return 1
        else:
            input_path = find_latest_english_output(config)
            if not input_path:
                print("\n❌ Error: No English output found to translate.")
                print("   Use --input to specify a file.")
                return 1
            print(f"\n📂 Found latest output: {input_path}")
        
        # Determine output file
        if args.output:
            output_path = Path(args.output)
        else:
            # Replace language in filename
            stem = input_path.stem
            if f"_{args.source}" in stem:
                new_stem = stem.replace(f"_{args.source}", f"_{args.target}")
            else:
                new_stem = f"{stem}_{args.target}"
            output_path = input_path.parent / f"{new_stem}.md"
        
        # Determine model
        model = args.model
        if not model:
            naming = config.get("output", {}).get("naming", {})
            languages = naming.get("languages", {})
            target_config = languages.get(args.target, {})
            model = target_config.get("translator_model", "gpt-4o")
        
        # Translate
        translated = translate_file(
            input_path=input_path,
            output_path=output_path,
            source_lang=args.source,
            target_lang=args.target,
            model=model,
            config=config,
        )
        
        # Generate HTML if requested
        if args.html:
            print("\n📊 Generating HTML...")
            converter = MarkMapHTMLConverter(config)
            html_content = converter.convert(
                translated,
                title=f"NeetCode Agent Evolved Mindmap ({args.target.upper()})"
            )
            html_path = output_path.with_suffix(".html")
            html_path.write_text(html_content, encoding="utf-8")
            print(f"   ✓ Saved: {html_path}")
        
        print("\n" + "=" * 60)
        print("✅ Translation complete!")
        print("=" * 60)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user.")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        ConfigLoader.clear_api_keys()
        print("\n🔒 API keys cleared from memory.")


if __name__ == "__main__":
    sys.exit(main())

