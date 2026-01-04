#!/usr/bin/env python3
"""
AI-Powered Mind Map Generator for LeetCode Practice

Automatically reads ontology data based on config and lets GPT models creatively
generate Markmap mind maps.

Usage:
    python tools/mindmaps/generate_mindmaps_ai.py                              # Interactive
    python tools/mindmaps/generate_mindmaps_ai.py --config generate_mindmaps_ai.toml
    python tools/mindmaps/generate_mindmaps_ai.py --goal interview
    python tools/mindmaps/generate_mindmaps_ai.py --topic sliding_window
    python tools/mindmaps/generate_mindmaps_ai.py --html-only                  # Generate HTML from existing Markdown files

Prompt Options:
    When an existing prompt is found, you can choose:
    - [l] Load existing prompt (use as-is)
    - [o] Optimize by AI (will overwrite)
    - [r] Regenerate prompt from config (will overwrite)
    
    On first run (no existing prompt):
    - [o] Generate prompt with AI (recommended)
    - [r] Generate prompt from config (standard)

Environment:
    OPENAI_API_KEY: Your OpenAI API key (required for API mode)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Add tools/ to Python path so mindmaps module can be imported
SCRIPT_DIR = Path(__file__).parent
TOOLS_DIR = SCRIPT_DIR.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

# Import from modular packages
from ai_mindmap import (
    # Config
    load_config,
    get_model_config,
    get_default_config,
    DEFAULT_MODEL,
    # Prompts
    build_system_prompt,
    build_user_prompt,
    # Data loading
    load_ontology_data,
    load_docs_patterns,
    load_meta_patterns,
    load_problems_data,
    # OpenAI client
    generate_with_openai,
    # Prompt management
    find_existing_prompt,
    save_prompt,
    optimize_prompt_with_ai,
    ask_use_existing_prompt,
    # HTML generation
    load_meta_description,
    generate_html_from_markdown,
)

# Import from mindmaps package
from mindmaps import load_problems
from mindmaps.link_post_processor import add_links_to_mindmap

# Try to import OpenAI for checking availability
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Paths
PROJECT_ROOT = TOOLS_DIR.parent
DEFAULT_CONFIG = SCRIPT_DIR / "generate_mindmaps_ai.toml"


def generate_mindmap_ai(config: dict[str, Any]) -> str:
    """Main function to generate AI-powered mind map."""
    
    print("🔄 Loading data based on config...")
    
    # Load all data based on config
    ontology_data = load_ontology_data(config)
    print(f"   📚 Ontology: {sum(len(v) for v in ontology_data.values())} items")
    
    docs_patterns = load_docs_patterns(config)
    print(f"   📖 Pattern Docs: {len(docs_patterns)} files")
    
    meta_patterns = load_meta_patterns(config)
    print(f"   🧩 Pattern Snippets: {sum(len(s) for s in meta_patterns.values())} snippets")
    
    problems_data = load_problems_data(config)
    print(f"   🎯 Problems: {len(problems_data)} problems")
    
    # Check for existing prompt
    prompt_config = config.get("prompt", {})
    prompt_dir = Path(prompt_config.get("directory", "tools/prompts/generated"))
    prompt_filename = prompt_config.get("filename", "mindmap-prompt")
    existing_prompt_file = find_existing_prompt(prompt_dir, prompt_filename)
    
    # Ask user what to do with existing prompt
    prompt_action = ask_use_existing_prompt(existing_prompt_file)
    
    if prompt_action == "load" and existing_prompt_file:
        print(f"\n📄 Loading existing prompt: {existing_prompt_file.name}")
        prompt_content = existing_prompt_file.read_text(encoding="utf-8")
        
        # Parse prompt file
        parts = prompt_content.split("\n---\n")
        if len(parts) >= 2:
            system_prompt = parts[0].replace("# System Prompt", "").strip()
            user_prompt = parts[1].replace("# User Prompt", "").strip()
        else:
            print("⚠️  Could not parse existing prompt, regenerating...")
            system_prompt = build_system_prompt(config)
            user_prompt = build_user_prompt(
                ontology_data, docs_patterns, meta_patterns, problems_data, config
            )
            save_prompt(system_prompt, user_prompt, config)
    elif prompt_action == "optimize":
        _handle_prompt_optimize(config, existing_prompt_file, ontology_data, docs_patterns, meta_patterns, problems_data)
        # Get the prompts after optimization
        prompt_file = Path(prompt_config.get("directory", "tools/prompts/generated")) / f"{prompt_filename}.md"
        if prompt_file.exists():
            prompt_content = prompt_file.read_text(encoding="utf-8")
            parts = prompt_content.split("\n---\n")
            system_prompt = parts[0].replace("# System Prompt", "").strip() if len(parts) >= 2 else build_system_prompt(config)
            user_prompt = parts[1].replace("# User Prompt", "").strip() if len(parts) >= 2 else build_user_prompt(ontology_data, docs_patterns, meta_patterns, problems_data, config)
        else:
            system_prompt = build_system_prompt(config)
            user_prompt = build_user_prompt(ontology_data, docs_patterns, meta_patterns, problems_data, config)
    elif prompt_action == "regenerate_and_optimize":
        _handle_regenerate_and_optimize(config, ontology_data, docs_patterns, meta_patterns, problems_data)
        # Get the prompts after optimization
        prompt_file = Path(prompt_config.get("directory", "tools/prompts/generated")) / f"{prompt_filename}.md"
        if prompt_file.exists():
            prompt_content = prompt_file.read_text(encoding="utf-8")
            parts = prompt_content.split("\n---\n")
            system_prompt = parts[0].replace("# System Prompt", "").strip() if len(parts) >= 2 else build_system_prompt(config)
            user_prompt = parts[1].replace("# User Prompt", "").strip() if len(parts) >= 2 else build_user_prompt(ontology_data, docs_patterns, meta_patterns, problems_data, config)
        else:
            system_prompt = build_system_prompt(config)
            user_prompt = build_user_prompt(ontology_data, docs_patterns, meta_patterns, problems_data, config)
    else:  # regenerate
        print("\n📝 Regenerating prompt from config and data...")
        system_prompt = build_system_prompt(config)
        user_prompt = build_user_prompt(
            ontology_data, docs_patterns, meta_patterns, problems_data, config
        )
        prompt_file = save_prompt(system_prompt, user_prompt, config)
        if prompt_file:
            print(f"📄 Regenerated prompt saved: {prompt_file}")
    
    # Get output config
    output_config = config.get("output", {})
    output_dir = Path(output_config.get("directory", "docs/mindmaps"))
    
    # Show which models are being used
    prompt_model_config = get_model_config(config, "prompt")
    mindmap_model_config = get_model_config(config, "mindmap")
    
    print(f"\n🤖 Model Configuration:")
    print(f"   📝 Prompt optimization: {prompt_model_config['name']}")
    print(f"      Max tokens: {prompt_model_config.get('max_completion_tokens', 'N/A')}")
    print(f"   🗺️  Mind map generation: {mindmap_model_config['name']}")
    print(f"      Max tokens: {mindmap_model_config.get('max_completion_tokens', 'N/A')}")
    
    if not HAS_OPENAI:
        print("\n⚠️  OpenAI library not installed.")
        print("   Copy the prompt above to GPT manually.")
        return ""
    
    # Get languages (support both string and list)
    advanced = config.get("advanced", {})
    language_setting = advanced.get("language", "en")
    
    print(f"\n📋 Language setting: {language_setting} (type: {type(language_setting).__name__})")
    
    # Handle both string and list formats
    if isinstance(language_setting, list):
        languages = language_setting
    elif isinstance(language_setting, str):
        if language_setting.startswith("[") and language_setting.endswith("]"):
            try:
                languages = json.loads(language_setting)
            except Exception:
                languages = [language_setting]
        else:
            languages = [language_setting]
    else:
        languages = ["en"]
    
    print(f"📋 Languages to generate: {languages}")
    
    # Base filename
    base_filename = output_config.get("filename", "ai_generated.md")
    if not base_filename.endswith(".md"):
        base_filename = f"{base_filename}.md"
    base_name = base_filename.replace(".md", "")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    all_contents = {}
    
    # Generate for each language
    for lang in languages:
        print(f"\n🌐 Generating {lang} version...")
        
        current_mindmap_model = get_model_config(config, "mindmap")
        print(f"   🤖 Using model: {current_mindmap_model['name']}")
        
        try:
            # Create language-specific config
            lang_config = config.copy()
            lang_config["advanced"] = advanced.copy()
            lang_config["advanced"]["language"] = lang
            
            # Build prompts with language-specific config
            lang_system_prompt = build_system_prompt(lang_config)
            lang_user_prompt = build_user_prompt(
                ontology_data, docs_patterns, meta_patterns, problems_data, lang_config
            )
            
            # Generate content (without links to save tokens)
            content = generate_with_openai(lang_system_prompt, lang_user_prompt, lang_config)
            
            # Add links after generation (post-processing to save tokens)
            problems = load_problems()
            content = add_links_to_mindmap(content, problems)
            print(f"   ✅ Links added via post-processing (saved tokens during generation)")
            
            all_contents[lang] = content
            
            # Save with language suffix (kebab-case)
            if len(languages) > 1:
                # Convert language code to lowercase and use hyphen separator
                lang_lower = lang.lower().replace("_", "-")
                lang_filename = f"{base_name}-{lang_lower}.md"
            else:
                lang_filename = base_filename
            
            output_file = output_dir / lang_filename
            output_file.write_text(content, encoding="utf-8")
            print(f"✅ Markdown ({lang}): {output_file}")
            
            # Generate HTML if enabled
            generate_html = output_config.get("generate_html", False)
            if generate_html in (True, "true", "True", "yes", "1"):
                from mindmaps.html import generate_html_mindmap
                
                html_dir = Path(output_config.get("html_directory", "docs/pages/mindmaps"))
                html_dir.mkdir(parents=True, exist_ok=True)
                
                # Extract title from content or use default
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
                
                html_content = generate_html_mindmap(title, content, use_autoloader=False, description=meta_description)
                html_filename = lang_filename.replace(".md", ".html")
                html_file = html_dir / html_filename
                html_file.write_text(html_content, encoding="utf-8")
                print(f"✅ HTML ({lang}): {html_file}")
        except Exception as e:
            print(f"❌ Failed to generate {lang} version: {e}")
            print(f"   Skipping {lang}, continuing with other languages...")
            continue
    
    # Return first content for backward compatibility
    return all_contents.get(languages[0], "")


def _handle_prompt_optimize(config, existing_prompt_file, ontology_data, docs_patterns, meta_patterns, problems_data):
    """Handle prompt optimization."""
    if existing_prompt_file:
        prompt_model_config = get_model_config(config, "prompt")
        print(f"\n🤖 Optimizing existing prompt with AI (using {prompt_model_config['name']})...")
        prompt_content = existing_prompt_file.read_text(encoding="utf-8")
        
        parts = prompt_content.split("\n---\n")
        if len(parts) >= 2:
            existing_system_prompt = parts[0].replace("# System Prompt", "").strip()
            existing_user_prompt = parts[1].replace("# User Prompt", "").strip()
            
            system_prompt, user_prompt = optimize_prompt_with_ai(
                existing_system_prompt, existing_user_prompt, config
            )
            prompt_file = save_prompt(system_prompt, user_prompt, config)
            if prompt_file:
                print(f"📄 Optimized prompt saved: {prompt_file}")
        else:
            print("⚠️  Could not parse existing prompt, regenerating with AI instead...")
            base_system_prompt = build_system_prompt(config)
            base_user_prompt = build_user_prompt(
                ontology_data, docs_patterns, meta_patterns, problems_data, config
            )
            system_prompt, user_prompt = optimize_prompt_with_ai(
                base_system_prompt, base_user_prompt, config
            )
            prompt_file = save_prompt(system_prompt, user_prompt, config)
            if prompt_file:
                print(f"📄 AI-generated prompt saved: {prompt_file}")
    else:
        prompt_model_config = get_model_config(config, "prompt")
        print(f"\n🤖 Generating prompt with AI (using {prompt_model_config['name']})...")
        print("   Step 1: Building base prompt from config...")
        base_system_prompt = build_system_prompt(config)
        base_user_prompt = build_user_prompt(
            ontology_data, docs_patterns, meta_patterns, problems_data, config
        )
        
        print("   Step 2: Optimizing with AI...")
        system_prompt, user_prompt = optimize_prompt_with_ai(
            base_system_prompt, base_user_prompt, config
        )
        prompt_file = save_prompt(system_prompt, user_prompt, config)
        if prompt_file:
            print(f"📄 AI-generated prompt saved: {prompt_file}")


def _handle_regenerate_and_optimize(config, ontology_data, docs_patterns, meta_patterns, problems_data):
    """Handle regenerate and optimize prompt."""
    prompt_model_config = get_model_config(config, "prompt")
    print("\n📝 Regenerating prompt from config and data...")
    print("   Step 1: Building prompt from config...")
    base_system_prompt = build_system_prompt(config)
    base_user_prompt = build_user_prompt(
        ontology_data, docs_patterns, meta_patterns, problems_data, config
    )
    
    print(f"   Step 2: Optimizing with AI (using {prompt_model_config['name']})...")
    system_prompt, user_prompt = optimize_prompt_with_ai(
        base_system_prompt, base_user_prompt, config
    )
    prompt_file = save_prompt(system_prompt, user_prompt, config)
    if prompt_file:
        print(f"📄 Regenerated and optimized prompt saved: {prompt_file}")


def interactive_mode() -> dict[str, Any]:
    """Interactive mode for generating mind maps."""
    print("\n" + "="*60)
    print("🧠 AI Mind Map Generator for LeetCode")
    print("="*60)
    
    config = load_config()
    
    print("\nSelect generation goal:")
    print("1. 🎯 Interview Prep - High-frequency problems and company preferences")
    print("2. 📚 Systematic Learning - Learning path sorted by difficulty")
    print("3. ⚡ Quick Review - Concise core content")
    print("4. 🔬 Pattern Mastery - In-depth pattern analysis")
    print("5. 🎨 Creative - Let AI generate creatively")
    print("6. 📌 Specific Topic - Focus on a specific topic")
    print("7. ⚙️  Use config file settings")
    
    choice = input("\nChoice (1-7) [default: 5]: ").strip() or "5"
    
    goals = {
        "1": "interview",
        "2": "systematic", 
        "3": "quick_review",
        "4": "pattern_mastery",
        "5": "creative",
        "6": None,
        "7": None,
    }
    
    if choice == "6":
        print("\nAvailable topics: sliding_window, binary_search, bfs, dfs, dp, backtracking, two_pointers, ...")
        topic = input("Enter topic: ").strip()
        config["generation"]["focus_topic"] = topic
        config["generation"]["goal"] = "creative"
    elif choice == "7":
        config_path = input(f"Config file path [{DEFAULT_CONFIG}]: ").strip()
        if config_path:
            config = load_config(Path(config_path))
    else:
        config["generation"]["goal"] = goals.get(choice, "creative")
    
    return config


def main() -> int:
    parser = argparse.ArgumentParser(
        description="AI-powered mind map generator for LeetCode"
    )
    parser.add_argument(
        "--config", "-c",
        type=Path,
        default=None,
        help=f"Config file path (default: {DEFAULT_CONFIG})"
    )
    parser.add_argument(
        "--goal", "-g",
        choices=["interview", "systematic", "quick_review", "pattern_mastery", "weakness_focus", "creative"],
        help="Learning goal (overrides config)"
    )
    parser.add_argument(
        "--topic", "-t",
        help="Focus on specific topic (overrides config)"
    )
    parser.add_argument(
        "--style", "-s",
        choices=["creative", "academic", "practical", "minimal", "balanced"],
        help="Mind map style (overrides config)"
    )
    parser.add_argument(
        "--model", "-m",
        help="OpenAI model (overrides config)"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Interactive mode"
    )
    parser.add_argument(
        "--list-config",
        action="store_true",
        help="Show current config and exit"
    )
    parser.add_argument(
        "--html-only",
        action="store_true",
        help="Generate HTML files from existing Markdown files without regenerating Markdown"
    )
    
    args = parser.parse_args()
    
    # Load config
    if args.interactive or (not args.config and not args.goal and not args.topic):
        config = interactive_mode()
    else:
        config = load_config(args.config)
    
    # Override with CLI args
    if args.goal:
        config.setdefault("generation", {})["goal"] = args.goal
    if args.topic:
        config.setdefault("generation", {})["focus_topic"] = args.topic
    if args.style:
        config.setdefault("generation", {})["style"] = args.style
    if args.model:
        config.setdefault("model", {})["name"] = args.model
        config.setdefault("model", {})["prompt_model"] = args.model
        config.setdefault("model", {})["mindmap_model"] = args.model
    
    # Show config if requested
    if args.list_config:
        print(json.dumps(config, indent=2, ensure_ascii=False))
        return 0
    
    # HTML-only mode
    if args.html_only:
        return generate_html_from_markdown(config)
    
    generate_mindmap_ai(config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
