"""
HTML generation from Markdown for AI Mind Map Generator.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

# Paths
TOOLS_DIR = Path(__file__).parent.parent
PROJECT_ROOT = TOOLS_DIR.parent


def load_meta_description(lang: str, base_filename: str, config: dict[str, Any]) -> str | None:
    """Load meta description from configured file path or auto-detect.
    
    Args:
        lang: Language code (e.g., "en", "zh-TW")
        base_filename: Base filename without extension (e.g., "neetcode-ontology-ai")
        config: Configuration dict
        
    Returns:
        Meta description string, or None if not found
    """
    output_config = config.get("output", {})
    meta_descriptions = output_config.get("meta_descriptions", {})
    
    # Try configured path first
    if isinstance(meta_descriptions, dict) and lang in meta_descriptions:
        desc_path_str = meta_descriptions[lang]
        desc_path = Path(desc_path_str)
        if not desc_path.is_absolute():
            desc_path = PROJECT_ROOT / desc_path
        
        if desc_path.exists():
            try:
                return desc_path.read_text(encoding="utf-8").strip()
            except Exception as e:
                print(f"   ⚠️  Failed to read meta description from {desc_path}: {e}")
    
    # Auto-detect: try tools/mindmaps/meta/{base_filename}-{lang}.txt (kebab-case)
    from mindmaps.config import META_DESCRIPTIONS_DIR
    lang_lower = lang.lower().replace("_", "-")
    auto_path = META_DESCRIPTIONS_DIR / f"{base_filename}-{lang_lower}.txt"
    if auto_path.exists():
        try:
            return auto_path.read_text(encoding="utf-8").strip()
        except Exception as e:
            print(f"   ⚠️  Failed to read auto-detected meta description from {auto_path}: {e}")
    
    # Fallback: try without language suffix
    auto_path_no_lang = META_DESCRIPTIONS_DIR / f"{base_filename}.txt"
    if auto_path_no_lang.exists():
        try:
            return auto_path_no_lang.read_text(encoding="utf-8").strip()
        except Exception:
            pass
    
    return None


def generate_html_from_markdown(config: dict[str, Any]) -> int:
    """Generate HTML files from existing Markdown files without regenerating Markdown.
    
    This function reads existing Markdown mind map files and generates HTML versions
    with proper meta descriptions. Useful when you only want to update HTML without
    regenerating the entire mind map.
    
    Args:
        config: Configuration dict
        
    Returns:
        0 on success, 1 on error
    """
    import json as json_module
    
    output_config = config.get("output", {})
    output_dir = Path(output_config.get("directory", "docs/mindmaps"))
    html_dir = Path(output_config.get("html_directory", "docs/pages/mindmaps"))
    
    # Get base filename
    base_filename = output_config.get("filename", "neetcode-ontology-ai.md")
    if not base_filename.endswith(".md"):
        base_filename = f"{base_filename}.md"
    base_name = base_filename.replace(".md", "")
    
    # Get languages from config
    advanced = config.get("advanced", {})
    language_setting = advanced.get("language", "en")
    
    # Handle both string and list formats
    if isinstance(language_setting, list):
        languages = language_setting
    elif isinstance(language_setting, str):
        if language_setting.startswith("[") and language_setting.endswith("]"):
            try:
                languages = json_module.loads(language_setting)
            except Exception:
                languages = [language_setting]
        else:
            languages = [language_setting]
    else:
        languages = ["en"]
    
    print(f"\n📄 Generating HTML from existing Markdown files...")
    print(f"   Base filename: {base_filename}")
    print(f"   Languages: {languages}")
    print(f"   HTML output: {html_dir}")
    
    html_dir.mkdir(parents=True, exist_ok=True)
    
    from mindmaps.html import generate_html_mindmap
    
    success_count = 0
    error_count = 0
    
    for lang in languages:
        # Determine Markdown filename (kebab-case)
        if len(languages) > 1:
            # Convert language code to lowercase and use hyphen separator
            lang_lower = lang.lower().replace("_", "-")
            md_filename = f"{base_name}-{lang_lower}.md"
        else:
            md_filename = base_filename
        
        md_file = output_dir / md_filename
        
        if not md_file.exists():
            print(f"   ⚠️  Markdown file not found: {md_file}")
            print(f"      Skipping {lang}...")
            error_count += 1
            continue
        
        print(f"\n🌐 Processing {lang}...")
        print(f"   Reading: {md_file}")
        
        try:
            # Read Markdown content
            content = md_file.read_text(encoding="utf-8")
            
            # Extract title from frontmatter or use default
            title = f"LeetCode Ontology Mind Map ({lang})"
            if content.startswith("---"):
                for line in content.split("\n"):
                    if line.startswith("title:"):
                        title = line.replace("title:", "").strip().strip('"').strip("'")
                        break
            
            # Load meta description for this language
            meta_description = load_meta_description(lang, base_name, config)
            if meta_description:
                print(f"   📝 Using meta description from file ({len(meta_description)} chars)")
            else:
                print(f"   ℹ️  No meta description file found for {lang}, using default")
            
            # Generate HTML
            html_content = generate_html_mindmap(title, content, use_autoloader=False, description=meta_description)
            
            # Determine HTML filename (kebab-case)
            if len(languages) > 1:
                # Convert language code to lowercase and use hyphen separator
                lang_lower = lang.lower().replace("_", "-")
                html_filename = f"{base_name}-{lang_lower}.html"
            else:
                html_filename = base_filename.replace(".md", ".html")
            
            html_file = html_dir / html_filename
            html_file.write_text(html_content, encoding="utf-8")
            print(f"   ✅ Generated: {html_file}")
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ Error processing {lang}: {e}")
            error_count += 1
            continue
    
    print(f"\n{'='*60}")
    if success_count > 0:
        print(f"✅ Successfully generated {success_count} HTML file(s)")
    if error_count > 0:
        print(f"❌ Failed to generate {error_count} HTML file(s)")
    print(f"{'='*60}")
    
    return 0 if error_count == 0 else 1

