#!/usr/bin/env python3
"""
HTML Meta Description Generator for Mind Maps

Generates SEO-friendly meta descriptions from Markdown files using OpenAI GPT-4o.
Follows the Meta Description Generation Spec for optimal SERP display.

Usage:
    python tools/html_meta_description_generator.py                    # Generate all configured files
    python tools/html_meta_description_generator.py --file path.md    # Generate specific file
    python tools/html_meta_description_generator.py --list            # List configured files
"""

from __future__ import annotations

import argparse
import getpass
import re
import sys
from pathlib import Path
from typing import Any

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

# Handle both module import and direct script execution
_script_dir = Path(__file__).resolve().parent
if str(_script_dir.parent) not in sys.path:
    sys.path.insert(0, str(_script_dir.parent))

from tools.mindmaps.config import PROJECT_ROOT, META_DESCRIPTIONS_DIR
from tools.mindmaps.toml_parser import parse_toml_simple


CONFIG_FILE = Path(__file__).resolve().parent / "html_meta_description_generator.toml"
PROMPT_FILE = Path(__file__).resolve().parent / "html-meta-description-generator.md"
PROMPT_FILE_ZH_TW = Path(__file__).resolve().parent / "html-meta-description-generator-zh-tw.md"

# Default configuration
DEFAULT_CONFIG = {
    "minLen": 80,
    "maxLen": 160,
    "preferFrontmatterDescription": True,
    "keepInlineCodeContent": True,
    "keepImageAlt": True,
    "languageMode": "auto",
    "outputDir": str(META_DESCRIPTIONS_DIR),
    "model": "gpt-4o",
}


def _extract_md_section(content: str, heading: str) -> str | None:
    """
    Extract a markdown section body by heading (e.g., "System Prompt" or "System Prompt (zh-TW)").

    Returns the section text without the heading line, or None if not found.
    """
    pattern = rf'## {re.escape(heading)}\s*\n(.*?)(?=\n## |$)'
    m = re.search(pattern, content, re.DOTALL)
    return m.group(1).strip() if m else None


def load_prompts() -> dict[str, tuple[str, str]]:
    """
    Load prompts from markdown file.

    Supports:
    - `html_meta_description_generator.md`:
      - "## System Prompt" + "## User Prompt Template" (default)
    - `html_meta_description_generator_zh-TW.md` (optional):
      - "## System Prompt" + "## User Prompt Template" (Traditional Chinese / Taiwan)
    """
    if not PROMPT_FILE.exists():
        raise FileNotFoundError(f"Prompt file not found: {PROMPT_FILE}")
    
    content = PROMPT_FILE.read_text(encoding="utf-8")
    
    system_prompt = _extract_md_section(content, "System Prompt")
    user_prompt_template = _extract_md_section(content, "User Prompt Template")
    if not system_prompt:
        raise ValueError("System prompt not found in prompt file (## System Prompt)")
    if not user_prompt_template:
        raise ValueError("User prompt template not found in prompt file (## User Prompt Template)")

    prompts: dict[str, tuple[str, str]] = {"default": (system_prompt, user_prompt_template)}

    if PROMPT_FILE_ZH_TW.exists():
        zh_content = PROMPT_FILE_ZH_TW.read_text(encoding="utf-8")
        zh_system = _extract_md_section(zh_content, "System Prompt")
        zh_user = _extract_md_section(zh_content, "User Prompt Template")
        if zh_system and zh_user:
            prompts["zh-TW"] = (zh_system, zh_user)

    return prompts


def load_config() -> dict[str, Any]:
    """Load configuration from TOML file."""
    config = DEFAULT_CONFIG.copy()
    
    if CONFIG_FILE.exists():
        try:
            parsed = parse_toml_simple(CONFIG_FILE.read_text(encoding="utf-8"))
            # Global settings
            if "global" in parsed:
                config.update(parsed["global"])
            # File-specific settings (will be merged per file)
            config["files"] = parsed.get("files", {})
        except Exception as e:
            print(f"Warning: Failed to load config: {e}")
    
    return config


def extract_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Extract frontmatter from markdown content."""
    frontmatter = {}
    body = content
    
    if content.startswith("---"):
        lines = content.split("\n")
        end_idx = None
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                end_idx = i
                break
        
        if end_idx:
            frontmatter_lines = lines[1:end_idx]
            body = "\n".join(lines[end_idx + 1:])
            
            # Simple YAML-like parsing
            for line in frontmatter_lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    frontmatter[key] = value
    
    return frontmatter, body


def clean_markdown_text(text: str, config: dict[str, Any]) -> str:
    """Clean markdown text for description extraction."""
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'~~~[\s\S]*?~~~', '', text)
    
    # Remove inline code (keep content if configured)
    if config.get("keepInlineCodeContent", True):
        text = re.sub(r'`([^`]+)`', r'\1', text)
    else:
        text = re.sub(r'`[^`]+`', '', text)
    
    # Remove images (keep alt text if configured)
    if config.get("keepImageAlt", True):
        text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', text)
    else:
        text = re.sub(r'!\[[^\]]*\]\([^\)]+\)', '', text)
    
    # Remove links (keep text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove blockquote markers
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    
    # Remove table syntax (simple)
    text = re.sub(r'\|', ' ', text)
    text = re.sub(r'^[\s\-\|:]+$', '', text, flags=re.MULTILINE)
    
    # Remove headings
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


def detect_language(text: str) -> str:
    """Detect language based on CJK character ratio."""
    if not text:
        return "en"
    
    cjk_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff\u3000-\u303f]')
    cjk_count = len(cjk_pattern.findall(text))
    total_chars = len(text)
    
    if total_chars == 0:
        return "en"
    
    cjk_ratio = cjk_count / total_chars
    return "zh-TW" if cjk_ratio > 0.3 else "en"


def validate_description(desc: str, config: dict[str, Any]) -> bool:
    """Validate description according to spec rules."""
    if not desc or len(desc.strip()) < config.get("minLen", 80):
        return False
    
    # Check for markdown artifacts
    if re.search(r'```|\[.*\]\(|#+\s|`[^`]', desc):
        return False
    
    # Check for navigation/boilerplate
    boilerplate_patterns = [
        r'table\s+of\s+contents',
        r'read\s+more',
        r'上一篇|下一篇',
        r'tags?\s*:',
        r'categories?\s*:',
    ]
    desc_lower = desc.lower()
    for pattern in boilerplate_patterns:
        if re.search(pattern, desc_lower):
            return False
    
    # Check for URLs
    url_count = len(re.findall(r'https?://[^\s]+', desc))
    if url_count > 1:
        return False
    
    # Check for code-like content
    code_indicators = ['{', '}', '=>', 'import ', 'function ', 'def ', 'class ']
    code_density = sum(1 for indicator in code_indicators if indicator in desc)
    if code_density > 2 and len(desc) < 200:
        return False
    
    # Check for keyword stuffing
    words = desc.lower().split()
    if len(words) > 0:
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        max_repeat = max(word_counts.values()) if word_counts else 0
        if max_repeat >= 3 and len(words) < 30:
            return False
    
    return True


def truncate_description(desc: str, max_len: int) -> str:
    """Truncate description at sentence or word boundary."""
    if len(desc) <= max_len:
        return desc
    
    # Try sentence boundary
    sentence_endings = r'[.!?。！？]'
    matches = list(re.finditer(sentence_endings, desc[:max_len]))
    if matches:
        last_match = matches[-1]
        return desc[:last_match.end()].strip()
    
    # Try word boundary
    last_space = desc.rfind(' ', 0, max_len)
    if last_space > max_len * 0.7:  # Only if we keep at least 70% of content
        return desc[:last_space].strip()
    
    # Hard cut
    return desc[:max_len].strip()


def extract_candidate_description(md_content: str, config: dict[str, Any]) -> str | None:
    """Extract candidate description from markdown."""
    frontmatter, body = extract_frontmatter(md_content)
    
    # Priority 1: Frontmatter description
    if config.get("preferFrontmatterDescription", True):
        for key in ["description", "summary", "excerpt"]:
            if key in frontmatter:
                desc = frontmatter[key].strip()
                if validate_description(desc, config):
                    return desc
    
    # Priority 2: First good paragraph
    cleaned_body = clean_markdown_text(body, config)
    paragraphs = [p.strip() for p in cleaned_body.split("\n\n") if p.strip()]
    
    for para in paragraphs:
        if len(para) >= config.get("minLen", 80):
            if validate_description(para, config):
                return truncate_description(para, config.get("maxLen", 160))
    
    # Priority 3: Merge paragraphs
    merged = ""
    for para in paragraphs:
        if merged:
            merged += " "
        merged += para
        if len(merged) >= config.get("minLen", 80):
            merged = truncate_description(merged, config.get("maxLen", 160))
            if validate_description(merged, config):
                return merged
    
    # Priority 4: Heading + first sentence
    title = frontmatter.get("title", "")
    if paragraphs:
        first_sentence = paragraphs[0].split('.')[0] if '.' in paragraphs[0] else paragraphs[0]
        if title:
            desc = f"{title}. {first_sentence}"
        else:
            desc = first_sentence
        desc = truncate_description(desc, config.get("maxLen", 160))
        if validate_description(desc, config):
            return desc
    
    return None


def generate_with_openai(md_content: str, config: dict[str, Any], api_key: str, title: str = "") -> str:
    """Generate description using OpenAI GPT-4o."""
    client = OpenAI(api_key=api_key)
    
    # Detect language
    language_mode = config.get("languageMode", "auto")
    if language_mode == "auto":
        detected_lang = detect_language(md_content)
    else:
        detected_lang = language_mode
    
    # Extract candidate for context
    candidate = extract_candidate_description(md_content, config)
    
    # Load prompts from external markdown file
    prompts = load_prompts()
    system_prompt, user_prompt_template = prompts.get(detected_lang, prompts["default"])
    
    # Build user prompt from template
    candidate_info = f"Existing candidate: {candidate}" if candidate else ""
    user_prompt = user_prompt_template.format(
        title=title or "Untitled",
        content_preview=md_content[:2000],
        candidate_info=candidate_info,
        language=detected_lang,
    )
    
    # Get model from config
    model = config.get("model", "gpt-4o")
    
    try:
        # Use max_completion_tokens (newer API standard)
        # For older models that don't support it, we'll catch the error and retry with max_tokens
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_completion_tokens=200,
            )
        except Exception as e:
            # Fallback to max_tokens for older models
            if "max_completion_tokens" in str(e) or "unsupported_parameter" in str(e).lower():
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=200,
                )
            else:
                raise
        
        description = response.choices[0].message.content.strip()
        
        # Clean and validate
        description = clean_markdown_text(description, config)
        description = truncate_description(description, config.get("maxLen", 160))
        
        # Ensure minimum length
        if len(description) < config.get("minLen", 80):
            # Add fallback sentence
            if detected_lang == "zh-TW":
                description += f" 關於「{title or '此主題'}」的詳細說明與範例。"
            else:
                description += f" Learn more about {title or 'this topic'} with examples and explanations."
            description = truncate_description(description, config.get("maxLen", 160))
        
        return description
        
    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {e}")


def escape_html_attr(text: str) -> str:
    """Escape text for HTML attribute."""
    text = text.replace("&", "&amp;")
    text = text.replace('"', "&quot;")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def generate_description(md_file: Path, config: dict[str, Any], api_key: str, file_config: dict[str, Any] | None = None) -> str:
    """Generate description for a markdown file."""
    # Merge file-specific config
    merged_config = config.copy()
    if file_config:
        # Ensure file_config is a dictionary
        if isinstance(file_config, dict):
            merged_config.update(file_config)
        else:
            # If it's not a dict (e.g., empty list from TOML parsing), treat as empty config
            pass
    
    content = md_file.read_text(encoding="utf-8")
    frontmatter, _ = extract_frontmatter(content)
    title = frontmatter.get("title", md_file.stem.replace("_", " ").title())
    
    # Try extraction first
    candidate = extract_candidate_description(content, merged_config)
    
    # Always use OpenAI for final generation (better quality)
    try:
        description = generate_with_openai(content, merged_config, api_key, title)
    except Exception as e:
        print(f"Warning: OpenAI generation failed: {e}")
        if candidate:
            description = candidate
        else:
            # Fallback
            if detect_language(content) == "zh-TW":
                description = f"關於「{title}」的筆記與說明。"
            else:
                description = f"Notes and explanations about {title}."
    
    # Final validation and truncation
    description = truncate_description(description, merged_config.get("maxLen", 160))
    if len(description) < merged_config.get("minLen", 80):
        # Pad if too short
        if detect_language(description) == "zh-TW":
            description += " 包含詳細說明與實用範例。"
        else:
            description += " Includes detailed explanations and practical examples."
        description = truncate_description(description, merged_config.get("maxLen", 160))
    
    return escape_html_attr(description)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate meta descriptions from Markdown files")
    parser.add_argument("--file", "-f", type=Path, help="Generate for specific file")
    parser.add_argument("--list", "-l", action="store_true", help="List configured files")
    parser.add_argument("--output", "-o", type=Path, help="Output directory (overrides config)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files without asking")
    
    args = parser.parse_args()
    
    config = load_config()
    output_dir_str = args.output if args.output else config.get("outputDir", str(META_DESCRIPTIONS_DIR))
    output_dir = Path(output_dir_str)
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.list:
        print("Configured files:")
        files = config.get("files", {})
        for file_path, file_config in files.items():
            print(f"  {file_path}")
        return 0
    
    # Get files to process
    files_to_process: list[tuple[Path, dict[str, Any] | None]] = []
    
    if args.file:
        # Single file
        if not args.file.exists():
            print(f"Error: File not found: {args.file}")
            return 1
        files_to_process.append((args.file, None))
    else:
        # All configured files
        files = config.get("files", {})
        if not files:
            print("No files configured. Add files to html_meta_description_generator.toml")
            return 1
        
        for file_path_str, file_config in files.items():
            # Remove any surrounding quotes from path string
            file_path_str = file_path_str.strip().strip('"').strip("'")
            file_path = Path(file_path_str)
            if not file_path.is_absolute():
                file_path = PROJECT_ROOT / file_path
            if file_path.exists():
                files_to_process.append((file_path, file_config))
            else:
                print(f"Warning: File not found: {file_path}")
    
    # Prompt for API key if we need to generate descriptions
    if files_to_process:
        print("OpenAI API Key required for generating descriptions.")
        api_key = getpass.getpass("Enter your OpenAI API Key: ")
        if not api_key or not api_key.strip():
            print("Error: API key cannot be empty")
            return 1
        api_key = api_key.strip()
    
    # Process files
    for md_file, file_config in files_to_process:
        print(f"\nProcessing: {md_file}")
        
        # Determine output filename
        output_filename = md_file.stem + ".txt"
        output_file = output_dir / output_filename
        
        # Check if exists
        if output_file.exists() and not args.force:
            response = input(f"  {output_file} exists. Overwrite? [y/N]: ")
            if response.lower() != 'y':
                print(f"  Skipped: {output_file}")
                continue
        
        try:
            description = generate_description(md_file, config, api_key, file_config)
            output_file.write_text(description, encoding="utf-8")
            print(f"  ✅ Generated: {output_file} ({len(description)} chars)")
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return 1
    
    if files_to_process:
        print(f"\n[OK] Generated {len(files_to_process)} description(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

