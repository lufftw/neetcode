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
from src.post_processing import clean_translated_content


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
    template = naming.get("template", "{prefix}-ontology-agent-evolved-{lang}")
    filename = template.format(prefix=prefix, lang="en") + ".md"
    
    final_dirs = output_config.get("final_dirs", {})
    base_dir = Path(__file__).parent
    md_dir = (base_dir / final_dirs.get("markdown", "outputs/final")).resolve()
    
    final_path = md_dir / filename
    if final_path.exists():
        return final_path
    
    # Try old format filenames (for backwards compatibility)
    old_formats = [
        f"{prefix}-general-ai-en.md",
        f"{prefix}-specialist-ai-en.md",
        f"{prefix}-ontology-ai-en.md",
    ]
    for old_filename in old_formats:
        old_path = md_dir / old_filename
        if old_path.exists():
            print(f"  ⚠ Found old format file: {old_filename}")
            return old_path
    
    return None


def translate_content(
    content: str,
    source_lang: str,
    target_lang: str,
    model: str,
    config: dict,
    output_key: str | None = None,
) -> str:
    """
    Translate content using TranslatorAgent.
    
    This is the unified translation function used by both translate_only.py
    and graph.py to ensure consistent behavior.
    
    Args:
        content: Content to translate
        source_lang: Source language code
        target_lang: Target language code
        model: Model name to use
        config: Configuration dictionary
        output_key: Optional output key for logging (used in pipeline)
        
    Returns:
        Translated content
    """
    # Create translator
    translator = TranslatorAgent(
        source_language=source_lang,
        target_language=target_lang,
        model=model,
        config=config,
    )
    
    # Translate
    if output_key:
        print(f"  ⏳ Translating {output_key} ({source_lang} → {target_lang})...")
    else:
        print(f"\n⏳ Translating ({source_lang} → {target_lang})...")
    
    try:
        translated = translator.translate(content, "general")
    except Exception as e:
        # Get debug output path if available
        debug_info = ""
        try:
            from src.debug_output import get_debug_manager
            debug = get_debug_manager(config)
            if debug.enabled and debug.run_dir.exists():
                debug_info = f"\n   📁 Debug outputs: {debug.run_dir}\n      Check LLM input/output files for details."
        except:
            pass
        
        raise RuntimeError(
            f"Translation failed with exception: {e}\n"
            f"   Model: {model}\n"
            f"   Source: {source_lang} → Target: {target_lang}\n"
            f"   Input size: {len(content)} chars, {len(content.splitlines())} lines{debug_info}\n"
            f"   Troubleshooting:\n"
            f"   1. Verify API key is set correctly (check environment variables)\n"
            f"   2. Check API key has sufficient credits/quota\n"
            f"   3. Verify model name '{model}' is valid and accessible\n"
            f"   4. Review debug output files for API response details"
        ) from e
    
    # Validate translation result
    if not translated:
        # Get debug output path if available
        debug_info = ""
        try:
            from src.debug_output import get_debug_manager
            debug = get_debug_manager(config)
            if debug.enabled and debug.run_dir.exists():
                debug_info = f"\n   📁 Debug outputs: {debug.run_dir}\n      Check 'llm_output_translator_*_translate.md' for API response."
        except:
            pass
        
        raise ValueError(
            f"Translation returned empty content (None).\n"
            f"   Model: {model}\n"
            f"   Source: {source_lang} → Target: {target_lang}\n"
            f"   Input size: {len(content)} chars, {len(content.splitlines())} lines{debug_info}\n"
            f"   Possible causes:\n"
            f"   1. API key is missing or invalid\n"
            f"   2. API returned empty response (check debug output files)\n"
            f"   3. Model '{model}' is not available or not responding\n"
            f"   4. Network/API connection issue\n"
            f"   Troubleshooting:\n"
            f"   - Verify OPENAI_API_KEY environment variable is set\n"
            f"   - Check API key has sufficient credits\n"
            f"   - Review debug output files for detailed API response"
        )
    
    if len(translated.strip()) == 0:
        # Get debug output path if available
        debug_info = ""
        try:
            from src.debug_output import get_debug_manager
            debug = get_debug_manager(config)
            if debug.enabled and debug.run_dir.exists():
                debug_info = f"\n   📁 Debug outputs: {debug.run_dir}\n      Check 'llm_output_translator_*_translate.md' for API response."
        except:
            pass
        
        raise ValueError(
            f"Translation returned only whitespace (empty after stripping).\n"
            f"   Model: {model}\n"
            f"   Source: {source_lang} → Target: {target_lang}\n"
            f"   Input size: {len(content)} chars, {len(content.splitlines())} lines\n"
            f"   Raw response length: {len(translated)} chars{debug_info}\n"
            f"   Possible causes:\n"
            f"   1. API returned whitespace-only response\n"
            f"   2. Model generated empty content\n"
            f"   3. Response parsing issue\n"
            f"   Troubleshooting:\n"
            f"   - Review debug output files to see actual API response\n"
            f"   - Check if API key has proper permissions\n"
            f"   - Verify model configuration in config file"
        )
    
    if not output_key:
        print(f"   Raw translation: {len(translated)} chars")
    
    # Clean up LLM artifacts
    translated = clean_translated_content(translated)
    
    # Validate cleaned content
    if not translated or len(translated.strip()) == 0:
        # Get debug output path if available
        debug_info = ""
        try:
            from src.debug_output import get_debug_manager
            debug = get_debug_manager(config)
            if debug.enabled and debug.run_dir.exists():
                debug_info = f"\n   📁 Debug outputs: {debug.run_dir}\n      Check 'llm_output_translator_*_translate.md' for original API response."
        except:
            pass
        
        raise ValueError(
            f"After cleaning, translation is empty.\n"
            f"   Model: {model}\n"
            f"   Source: {source_lang} → Target: {target_lang}\n"
            f"   Input size: {len(content)} chars, {len(content.splitlines())} lines{debug_info}\n"
            f"   This suggests the cleaning function (clean_translated_content) removed all content.\n"
            f"   Possible causes:\n"
            f"   1. API response format was unexpected\n"
            f"   2. Cleaning function is too aggressive\n"
            f"   3. Response contained only artifacts that were removed\n"
            f"   Troubleshooting:\n"
            f"   - Review debug output files to see raw API response\n"
            f"   - Check clean_translated_content function logic\n"
            f"   - Verify API response format matches expectations"
        )
    
    if output_key:
        print(f"  ✓ Translated: {output_key} ({len(translated)} chars, {len(translated.splitlines())} lines)")
    else:
        print(f"   ✓ Cleaned translation: {len(translated)} chars, {len(translated.splitlines())} lines")
    
    return translated


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
    
    # Check if input file exists
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Read input
    content = input_path.read_text(encoding="utf-8")
    print(f"   Read {len(content)} chars, {len(content.splitlines())} lines")
    
    # Use unified translation function
    translated = translate_content(
        content=content,
        source_lang=source_lang,
        target_lang=target_lang,
        model=model,
        config=config,
    )
    
    # Save output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(translated, encoding="utf-8")
    
    # Verify file was written
    if not output_path.exists():
        raise IOError(f"Failed to write output file: {output_path}")
    if output_path.stat().st_size == 0:
        raise IOError(f"Output file is empty: {output_path}")
    
    print(f"\n💾 Saved: {output_path} ({output_path.stat().st_size} bytes)")
    
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
        
        # Get script base directory for resolving relative paths
        script_base_dir = Path(__file__).parent
        
        # Determine input file
        if args.input:
            input_path = Path(args.input)
            # Resolve relative paths relative to script directory (CLI tool behavior)
            if not input_path.is_absolute():
                input_path = (script_base_dir / input_path).resolve()
            else:
                input_path = input_path.resolve()
            
            if not input_path.exists():
                print(f"\n❌ Error: Input file not found: {args.input}")
                print(f"   Resolved path: {input_path}")
                return 1
        else:
            input_path = find_latest_english_output(config)
            if not input_path:
                print("\n❌ Error: No English output found to translate.")
                print("   Use --input to specify a file.")
                return 1
            print(f"\n📂 Found latest output: {input_path}")
        
        # Create converter for output path resolution
        converter = MarkMapHTMLConverter(config)
        
        # Determine output file
        if args.output:
            output_path = Path(args.output)
            # Resolve relative paths relative to script directory (CLI tool behavior)
            if not output_path.is_absolute():
                output_path = (script_base_dir / output_path).resolve()
            else:
                output_path = output_path.resolve()
        else:
            # Replace language suffix in filename (only at the end!)
            # Use lowercase language code for filename (e.g., zh-TW -> zh-tw)
            target_lang_lower = args.target.lower() if args.target else "en"
            source_lang_lower = args.source.lower() if args.source else "en"
            stem = input_path.stem
            # Try both underscore and dash patterns for backward compatibility
            suffix_underscore = f"_{source_lang_lower}"
            suffix_dash = f"-{source_lang_lower}"
            if stem.endswith(suffix_dash):
                # Replace dash-separated language code
                new_stem = stem[:-len(suffix_dash)] + f"-{target_lang_lower}"
            elif stem.endswith(suffix_underscore):
                # Replace underscore-separated language code
                new_stem = stem[:-len(suffix_underscore)] + f"-{target_lang_lower}"
            else:
                # Append new language code with dash
                new_stem = f"{stem}-{target_lang_lower}"
            
            # Use final_dirs.markdown from config for consistency with HTML output
            output_path = converter.md_output_dir / f"{new_stem}.md"
        
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
            # Use standalone converter
            from convert_to_html import convert_file_to_html
            html_config = config.get("output", {}).get("html", {})
            template_path = html_config.get("template", "templates/markmap.html")
            
            # Get HTML output directory from config
            final_dirs = config.get("output", {}).get("final_dirs", {})
            html_output_dir = (script_base_dir / final_dirs.get("html", "outputs/final")).resolve()
            html_output_dir.mkdir(parents=True, exist_ok=True)
            
            html_path = html_output_dir / f"{output_path.stem}.html"
            convert_file_to_html(
                input_path=output_path,
                output_path=html_path,
                title=f"NeetCode Agent Evolved Mindmap ({args.target.upper()})",
                template_path=template_path,
            )
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

