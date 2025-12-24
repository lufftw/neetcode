#!/usr/bin/env python3
"""
AI-Powered Mind Map Generator for LeetCode Practice

Automatically reads ontology data based on config and lets GPT models creatively
generate Markmap mind maps.

Usage:
    python tools/generate_mindmaps_ai.py                              # Interactive
    python tools/generate_mindmaps_ai.py --config generate_mindmaps_ai.toml
    python tools/generate_mindmaps_ai.py --goal interview
    python tools/generate_mindmaps_ai.py --topic sliding_window
    python tools/generate_mindmaps_ai.py --html-only                  # Generate HTML from existing Markdown files

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
import os
import sys
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import Any

# Add tools directory to path
TOOLS_DIR = Path(__file__).parent
sys.path.insert(0, str(TOOLS_DIR))

from mindmaps import load_ontology, load_problems, DEFAULT_OUTPUT_DIR
from mindmaps.helpers import fix_table_links
from mindmaps.data import ProblemData
from mindmaps.toml_parser import parse_toml_simple
from mindmaps.post_processing import post_process_content

# Try to import OpenAI
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Try to import yaml
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Paths
PROJECT_ROOT = TOOLS_DIR.parent
ONTOLOGY_DIR = PROJECT_ROOT / "ontology"
DOCS_PATTERNS_DIR = PROJECT_ROOT / "docs" / "patterns"
PROMPTS_DIR = TOOLS_DIR / "prompts"
META_PATTERNS_DIR = PROJECT_ROOT / "meta" / "patterns"
DEFAULT_CONFIG = TOOLS_DIR / "generate_mindmaps_ai.toml"
# Use a chat model that is available via /v1/chat/completions by default.
# Older Codex-style completion models (e.g., gpt-5.1-codex) are no longer
# served by the public API and will raise "model not supported" errors.
DEFAULT_MODEL = "gpt-4.1"


def load_config(config_path: Path | None = None) -> dict[str, Any]:
    """Load configuration from TOML file."""
    if config_path is None:
        config_path = DEFAULT_CONFIG
    
    if not config_path.exists():
        print(f"⚠️  Config not found: {config_path}, using defaults")
        return get_default_config()
    
    return parse_toml_simple(config_path.read_text(encoding="utf-8"))


def get_model_config(config: dict[str, Any], model_type: str = "mindmap") -> dict[str, Any]:
    """
    Get model configuration for a specific type (prompt or mindmap).
    
    Args:
        config: Full configuration dict
        model_type: "prompt" or "mindmap"
        
    Returns:
        Dict with model configuration (name, temperature, max_completion_tokens, api_base)
    """
    model_config = config.get("model", {})
    
    # Support new separate model configs
    if model_type == "prompt":
        model_name = model_config.get("prompt_model") or model_config.get("name", DEFAULT_MODEL)
        temperature = float(model_config.get("prompt_temperature", model_config.get("temperature", 0.7)))
        max_tokens = int(model_config.get("prompt_max_completion_tokens", model_config.get("max_completion_tokens", 8000)))
    else:  # mindmap
        model_name = model_config.get("mindmap_model") or model_config.get("name", DEFAULT_MODEL)
        temperature = float(model_config.get("mindmap_temperature", model_config.get("temperature", 0.7)))
        max_tokens = int(model_config.get("mindmap_max_completion_tokens", model_config.get("max_completion_tokens", 8000)))
    
    api_base = model_config.get("api_base", "")
    
    return {
        "name": model_name,
        "temperature": temperature,
        "max_completion_tokens": max_tokens,
        "api_base": api_base,
    }


def get_default_config() -> dict[str, Any]:
    """Return default configuration."""
    return {
        "model": {
            "name": DEFAULT_MODEL, 
            "temperature": 0.7, 
            "max_completion_tokens": 8000,
            "prompt_model": "gpt-4o",
            "prompt_temperature": 0.7,
            "prompt_max_completion_tokens": 8000,
            "mindmap_model": DEFAULT_MODEL,
            "mindmap_temperature": 0.7,
            "mindmap_max_completion_tokens": 8000,
        },
        "output": {"directory": "docs/mindmaps", "prefix": "ai_generated"},
        "ontology": {
            "api_kernels": True, "patterns": True, "algorithms": True,
            "data_structures": True, "families": True, "topics": True,
            "difficulties": True, "companies": True, "roadmaps": True,
        },
        "docs": {"patterns": {"enabled": True, "include": [], "exclude": ["README"]}},
        "meta": {"patterns": {
            "enabled": True, "include": [],
            "include_headers": True, "include_comparisons": True,
            "include_decisions": True, "include_templates": True, "include_problems": True,
        }},
        "problems": {"enabled": True, "limit": 50, "difficulties": [], "topics": [], "api_kernels": [], "roadmaps": [], "specific_ids": []},
        "generation": {"goal": "creative", "focus_topic": "", "style": "balanced", "custom_instructions": ""},
        "advanced": {"include_full_code": True, "include_complexity": True, "language": "zh-TW"},
        # Note: links config no longer used in prompts - post-processing handles all links automatically
    }


# =============================================================================
# Prompt Loading Functions
# =============================================================================

# Cache for loaded prompts
_cached_prompts: dict[str, Any] = {}


def load_prompts_config() -> dict[str, Any]:
    """Load prompts configuration from YAML file."""
    global _cached_prompts
    
    if _cached_prompts:
        return _cached_prompts
    
    config_path = PROMPTS_DIR / "prompts_config.yaml"
    
    if not config_path.exists():
        print(f"⚠️  Prompts config not found: {config_path}")
        return _get_default_prompts_config()
    
    if HAS_YAML:
        with open(config_path, encoding="utf-8") as f:
            _cached_prompts = yaml.safe_load(f)
    else:
        # Fallback: simple YAML parsing for our specific format
        _cached_prompts = _parse_simple_yaml(config_path)
    
    return _cached_prompts


def _get_default_prompts_config() -> dict[str, Any]:
    """Return default prompts configuration (fallback)."""
    return {
        "language_instructions": {
            "en": "IMPORTANT: Generate the mind map content in English. All titles, labels, and descriptions should be in English.",
            "zh-TW": "IMPORTANT: Generate the mind map content in Traditional Chinese (繁體中文). All titles, labels, and descriptions should be in Traditional Chinese.",
            "zh-CN": "IMPORTANT: Generate the mind map content in Simplified Chinese (简体中文). All titles, labels, and descriptions should be in Simplified Chinese.",
        },
        "goal_prompts": {
            "interview": "Generate an **interview-focused** mind map, emphasizing high-frequency problems, company preferences, and interview techniques. Mark must-solve problems.",
            "systematic": "Generate a **systematic learning roadmap**, sorted by difficulty and dependencies, including progress tracking checkboxes.",
            "quick_review": "Generate a **concise review** mind map with only the core patterns and key problems, suitable for quick pre-interview browsing.",
            "pattern_mastery": "Generate an **in-depth pattern analysis** mind map showing relationships between patterns, variants, and code templates.",
            "weakness_focus": "Analyze problem data to identify less-covered areas and generate a **targeted practice** mind map.",
            "creative": "Based on the overall knowledge graph, **creatively** generate a mind map you believe is most helpful for LeetCode practice. It can be a decision tree, learning path, or any innovative structure.",
        },
        "style_prompts": {
            "creative": "**Style**: Creativity first, use non-traditional structures and visual elements that catch the eye.",
            "academic": "**Style**: Academic rigor, focus on logical hierarchy and complexity analysis.",
            "practical": "**Style**: Practical orientation, use code templates and concrete examples.",
            "minimal": "**Style**: Minimalist style, keep only the most essential content.",
            "balanced": "**Style**: Balance beauty and practicality, suitable for most learners.",
        },
        "user_prompt_sections": {
            "summary_header": "## 📊 Data Summary\n",
            "ontology_header": "## 📚 Ontology Knowledge Graph\n",
            "pattern_docs_header": "\n## 📖 Pattern Documentation\n",
            "pattern_snippets_header": "\n## 🧩 Pattern Snippets\n",
            "problems_header": "\n## 🎯 Problem Data\n",
            "problems_note": "Note: Use `LeetCode {leetcode_id}` format to reference problems. Links and titles will be added automatically by post-processing.\n",
            "generation_header": "\n## 🎨 Generation Instructions\n",
            "focus_topic_template": "\n**Focus Topic**: `{topic}` - Please expand the mind map around this core.",
            "custom_instructions_template": "\n**Additional Instructions**: {instructions}",
            "no_complexity_note": "\nNote: Complexity analysis is not needed.",
        },
    }


def _parse_simple_yaml(path: Path) -> dict[str, Any]:
    """Simple YAML parser for our specific format (fallback when PyYAML not available)."""
    result: dict[str, Any] = {}
    current_section: str | None = None
    current_dict: dict[str, str] = {}
    
    with open(path, encoding="utf-8") as f:
        for line in f:
            # Skip comments and empty lines
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            
            # Check for top-level section (no leading spaces, ends with :)
            if not line.startswith(" ") and line.rstrip().endswith(":"):
                # Save previous section
                if current_section and current_dict:
                    result[current_section] = current_dict
                    current_dict = {}
                
                current_section = stripped.rstrip(":")
                continue
            
            # Check for key-value pair (2 spaces, key: "value" or key: value)
            if line.startswith("  ") and ":" in line and not line.startswith("    "):
                parts = line.strip().split(":", 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip().strip('"').strip("'")
                    if current_section:
                        current_dict[key] = value
    
    # Save last section
    if current_section and current_dict:
        result[current_section] = current_dict
    
    return result


def load_system_prompt_template() -> str:
    """Load system prompt template from file."""
    prompt_path = PROMPTS_DIR / "system_prompt.md"
    
    if not prompt_path.exists():
        print(f"⚠️  System prompt not found: {prompt_path}, using built-in default")
        return _get_default_system_prompt()
    
    return prompt_path.read_text(encoding="utf-8")


def _get_default_system_prompt() -> str:
    """Return default system prompt (fallback)."""
    return dedent("""
    You are a world-class expert in algorithms and LeetCode problem solving.
    
    Your task is to generate Markmap-format mind maps based on the provided data.
    
    {{LANGUAGE_INSTRUCTION}}
    
    ## CRITICAL: Problem Reference Format
    
    When mentioning LeetCode problems, use this simple format: `LeetCode {number}`
    
    DO NOT include URLs or links - post-processing will add them automatically.
    
    Output Markmap Markdown directly, without any explanations.
    """).strip()


def load_ontology_data(config: dict[str, Any]) -> dict[str, Any]:
    """Load ontology data based on config."""
    ontology_config = config.get("ontology", {})
    ontology = load_ontology()
    
    data = {}
    field_map = {
        "api_kernels": ontology.api_kernels,
        "patterns": ontology.patterns,
        "algorithms": ontology.algorithms,
        "data_structures": ontology.data_structures,
        "families": ontology.families,
        "topics": ontology.topics,
        "difficulties": ontology.difficulties,
        "companies": ontology.companies,
        "roadmaps": ontology.roadmaps,
    }
    
    for field, values in field_map.items():
        if ontology_config.get(field, True):
            data[field] = values
    
    return data


def load_docs_patterns(config: dict[str, Any]) -> dict[str, str]:
    """Load pattern documentation from docs/patterns/ (supports both flat and nested structures)."""
    docs_config = config.get("docs", {}).get("patterns", {})
    
    if not docs_config.get("enabled", True):
        return {}
    
    if not DOCS_PATTERNS_DIR.exists():
        return {}
    
    include = docs_config.get("include", [])
    exclude = docs_config.get("exclude", ["README"])
    
    docs = {}
    
    # Support both flat structure (*.md in root) and nested structure (*/intuition.md, */templates.md)
    # First, check root level .md files
    for md_file in DOCS_PATTERNS_DIR.glob("*.md"):
        name = md_file.stem
        
        # Filter by include/exclude
        if include and name not in include:
            continue
        if name in exclude:
            continue
        
        docs[name] = md_file.read_text(encoding="utf-8")
    
    # Then, check subdirectories for nested structure (e.g., sliding_window/intuition.md)
    for subdir in DOCS_PATTERNS_DIR.iterdir():
        if not subdir.is_dir():
            continue
        
        # Pattern name is the subdirectory name
        pattern_name = subdir.name
        
        # Filter by include/exclude (check if pattern name matches)
        if include and pattern_name not in include:
            continue
        if pattern_name in exclude:
            continue
        
        # Load all .md files in this subdirectory
        for md_file in subdir.glob("*.md"):
            # Use pattern_name/filename as key (e.g., "sliding_window/intuition")
            file_stem = md_file.stem
            key = f"{pattern_name}/{file_stem}"
            docs[key] = md_file.read_text(encoding="utf-8")
    
    return docs


def load_meta_patterns(config: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Load pattern snippets from meta/patterns/."""
    meta_config = config.get("meta", {}).get("patterns", {})
    
    if not meta_config.get("enabled", True):
        return {}
    
    if not META_PATTERNS_DIR.exists():
        return {}
    
    include_dirs = meta_config.get("include", [])
    include_headers = meta_config.get("include_headers", True)
    include_comparisons = meta_config.get("include_comparisons", True)
    include_decisions = meta_config.get("include_decisions", True)
    include_templates = meta_config.get("include_templates", True)
    include_problems = meta_config.get("include_problems", True)
    
    patterns = {}
    for pattern_dir in META_PATTERNS_DIR.iterdir():
        if not pattern_dir.is_dir():
            continue
        
        name = pattern_dir.name
        if include_dirs and name not in include_dirs:
            continue
        
        snippets = {}
        for md_file in pattern_dir.glob("*.md"):
            filename = md_file.name
            
            # Filter by type
            if filename.startswith("_header") and not include_headers:
                continue
            if filename.startswith("_comparison") and not include_comparisons:
                continue
            if filename.startswith("_decision") and not include_decisions:
                continue
            if filename.startswith("_templates") and not include_templates:
                continue
            if not filename.startswith("_") and not include_problems:
                continue
            
            snippets[filename] = md_file.read_text(encoding="utf-8")
        
        if snippets:
            patterns[name] = snippets
    
    return patterns


def load_problems_data(config: dict[str, Any]) -> list[dict[str, Any]]:
    """Load problem metadata based on config filters."""
    problems_config = config.get("problems", {})
    
    if not problems_config.get("enabled", True):
        return []
    
    problems = load_problems()
    
    # Apply filters
    difficulties = problems_config.get("difficulties", [])
    topics = problems_config.get("topics", [])
    api_kernels = problems_config.get("api_kernels", [])
    roadmaps = problems_config.get("roadmaps", [])
    specific_ids = problems_config.get("specific_ids", [])
    limit = problems_config.get("limit", 50)
    
    filtered = []
    for p in problems.values():
        # Specific IDs override other filters
        if specific_ids:
            if p.id not in specific_ids:
                continue
        else:
            # Apply filters
            if difficulties and p.difficulty.lower() not in [d.lower() for d in difficulties]:
                continue
            if topics and not any(t in p.topics for t in topics):
                continue
            if api_kernels and not any(k in p.api_kernels for k in api_kernels):
                continue
            if roadmaps and not any(r in p.roadmaps for r in roadmaps):
                continue
        
        filtered.append({
            "id": p.id,
            "leetcode_id": p.leetcode_id,
            "title": p.title,
            "slug": p.slug,
            "url": p.url,
            "difficulty": p.difficulty,
            "topics": p.topics,
            "patterns": p.patterns,
            "api_kernels": p.api_kernels,
            "families": p.families,
            "data_structures": p.data_structures,
            "algorithms": p.algorithms,
            "related_problems": p.related_problems,
            "companies": p.companies,
            "roadmaps": p.roadmaps,
            "solution_file": p.solution_file,
        })
    
    # Sort by leetcode_id and limit
    filtered.sort(key=lambda x: x.get("leetcode_id", 0))
    if limit > 0:
        filtered = filtered[:limit]
    
    return filtered


def build_system_prompt(config: dict[str, Any]) -> str:
    """Build system prompt based on config. Loads from external file with variable substitution."""
    advanced = config.get("advanced", {})
    language = advanced.get("language", "en")
    
    # Handle list of languages - use first one for system prompt
    if isinstance(language, list):
        language = language[0] if language else "en"
    
    # Load prompts config and system prompt template
    prompts_config = load_prompts_config()
    template = load_system_prompt_template()
    
    # Get language instruction
    lang_instructions = prompts_config.get("language_instructions", {})
    lang_instruction = lang_instructions.get(language, lang_instructions.get("en", ""))
    
    # Substitute variables in template
    prompt = template.replace("{{LANGUAGE_INSTRUCTION}}", lang_instruction)
    
    return prompt.strip()


def build_user_prompt(
    ontology_data: dict[str, Any],
    docs_patterns: dict[str, str],
    meta_patterns: dict[str, dict[str, str]],
    problems_data: list[dict[str, Any]],
    config: dict[str, Any],
) -> str:
    """Build user prompt with all context from config. Uses external prompts config."""
    generation = config.get("generation", {})
    advanced = config.get("advanced", {})
    
    language = advanced.get("language", "en")
    
    # Load prompts configuration
    prompts_config = load_prompts_config()
    sections_config = prompts_config.get("user_prompt_sections", {})
    goal_prompts = prompts_config.get("goal_prompts", {})
    style_prompts = prompts_config.get("style_prompts", {})
    
    sections = []
    
    # === Summary === (Always in English for prompt)
    summary_header = sections_config.get("summary_header", "## 📊 Data Summary\n")
    summary_lines = [summary_header]
    if ontology_data:
        for key, values in ontology_data.items():
            summary_lines.append(f"- **{key}**: {len(values)} items")
    if docs_patterns:
        summary_lines.append(f"- **Pattern Docs**: {len(docs_patterns)} files")
    if meta_patterns:
        total_snippets = sum(len(s) for s in meta_patterns.values())
        summary_lines.append(f"- **Pattern Snippets**: {len(meta_patterns)} directories, {total_snippets} snippets")
    if problems_data:
        summary_lines.append(f"- **Problems**: {len(problems_data)} problems")
    sections.append("\n".join(summary_lines))
    
    # === Ontology Data ===
    if ontology_data:
        ontology_header = sections_config.get("ontology_header", "## 📚 Ontology Knowledge Graph\n")
        sections.append(ontology_header)
        sections.append("```json")
        sections.append(json.dumps(ontology_data, indent=2, ensure_ascii=False))
        sections.append("```")
    
    # === Pattern Documentation ===
    if docs_patterns:
        pattern_docs_header = sections_config.get("pattern_docs_header", "\n## 📖 Pattern Documentation\n")
        sections.append(pattern_docs_header)
        for name, content in docs_patterns.items():
            sections.append(f"### {name}\n")
            # Truncate if too long
            if len(content) > 8000:
                sections.append(content[:8000] + "\n...(truncated)")
            else:
                sections.append(content)
    
    # === Meta Pattern Snippets ===
    if meta_patterns:
        pattern_snippets_header = sections_config.get("pattern_snippets_header", "\n## 🧩 Pattern Snippets\n")
        sections.append(pattern_snippets_header)
        for pattern_name, snippets in meta_patterns.items():
            sections.append(f"### {pattern_name}\n")
            for filename, content in snippets.items():
                sections.append(f"#### {filename}\n")
                if len(content) > 2000:
                    sections.append(content[:2000] + "\n...(truncated)")
                else:
                    sections.append(content)
    
    # === Problems ===
    # Only include essential fields for LLM (links will be added by post-processing)
    if problems_data:
        # Simplify problem data - remove link-related fields
        simplified_problems = []
        for p in problems_data:
            simplified_problems.append({
                "id": p.get("id"),
                "leetcode_id": p.get("leetcode_id"),
                "difficulty": p.get("difficulty"),
                "topics": p.get("topics", []),
                "patterns": p.get("patterns", []),
                "api_kernels": p.get("api_kernels", []),
                "families": p.get("families", []),
                "data_structures": p.get("data_structures", []),
                "algorithms": p.get("algorithms", []),
                "related_problems": p.get("related_problems", []),
                "companies": p.get("companies", []),
                "roadmaps": p.get("roadmaps", []),
            })
        
        problems_header = sections_config.get("problems_header", "\n## 🎯 Problem Data\n")
        problems_note = sections_config.get("problems_note", "Note: Use `LeetCode {leetcode_id}` format to reference problems. Links and titles will be added automatically by post-processing.\n")
        sections.append(problems_header)
        sections.append(problems_note)
        sections.append("```json")
        sections.append(json.dumps(simplified_problems, indent=2, ensure_ascii=False))
        sections.append("```")
    
    # === Generation Instructions ===
    language = advanced.get("language", "en")
    
    # Handle list of languages - use first one for generation instructions
    if isinstance(language, list):
        language = language[0] if language else "en"
    
    if language == "en":
        generation_header = sections_config.get("generation_header", "\n## 🎨 Generation Instructions\n")
        sections.append(generation_header)
        
        goal = generation.get("goal", "creative")
        focus_topic = generation.get("focus_topic", "")
        style = generation.get("style", "balanced")
        custom = generation.get("custom_instructions", "")
        
        # Use goal prompts from config
        sections.append(goal_prompts.get(goal, f"Goal: {goal}"))
        
        if focus_topic:
            focus_template = sections_config.get("focus_topic_template", "\n**Focus Topic**: `{topic}` - Please expand the mind map around this core.")
            sections.append(focus_template.format(topic=focus_topic))
        
        # Use style prompts from config
        style_prompt = style_prompts.get(style, "")
        if style_prompt:
            sections.append(f"\n{style_prompt}")
        
        if custom:
            custom_template = sections_config.get("custom_instructions_template", "\n**Additional Instructions**: {instructions}")
            sections.append(custom_template.format(instructions=custom))
        
        # Advanced options
        if not advanced.get("include_complexity", True):
            no_complexity = sections_config.get("no_complexity_note", "\nNote: Complexity analysis is not needed.")
            sections.append(no_complexity)
    
    return "\n".join(sections)


# Cache for API key (avoid asking multiple times)
_cached_api_key: str | None = None


def is_codex_model(model_name: str) -> bool:
    """Return True when using a Codex-style model that now requires Responses API."""
    return "codex" in model_name.lower()


def is_chat_model(model_name: str) -> bool:
    """
    Determine if a model is a chat model or completion model.
    
    Chat models use /v1/chat/completions endpoint.
    Completion models use /v1/completions endpoint.
    
    Args:
        model_name: Model name (e.g., "gpt-4o", "gpt-5.1-codex", "o1")
        
    Returns:
        True if chat model, False if completion model
    """
    model_lower = model_name.lower()
    
    # Completion models (use /v1/completions) - check these first (more specific)
    completion_model_patterns = [
        "text-",            # text-davinci-003, text-curie-001, etc.
        "davinci",          # davinci-003, etc.
        "curie",            # curie-001, etc.
        "babbage",          # babbage-001, etc.
        "ada",              # ada-001, etc.
    ]
    
    for pattern in completion_model_patterns:
        if pattern in model_lower:
            return False
    
    # Chat models (use /v1/chat/completions)
    # GPT-5.x series (excluding codex variants) are chat models
    chat_model_patterns = [
        "gpt-4",           # gpt-4, gpt-4o, gpt-4-turbo, gpt-4o-mini
        "gpt-3.5",         # gpt-3.5-turbo
        "gpt-5",           # gpt-5.2, gpt-5.1 (but NOT gpt-5.1-codex - handled separately)
        "o1",              # o1, o1-mini, o3-mini
        "o3",              # o3-mini
        "claude",          # Claude models
    ]
    
    for pattern in chat_model_patterns:
        if pattern in model_lower:
            return True
    
    # Default: assume chat model for unknown models (most modern models are chat)
    return True


def get_api_key() -> str | None:
    """Get API key from environment or interactive input (cached)."""
    global _cached_api_key
    
    # Return cached key if available
    if _cached_api_key:
        return _cached_api_key
    
    # 1. From environment variable
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if api_key:
        print("🔑 Using environment variable OPENAI_API_KEY")
        _cached_api_key = api_key
        return api_key
    
    # 2. Interactive input
    print("\n🔑 Please enter OpenAI API Key")
    print("   (Or set environment variable: $env:OPENAI_API_KEY = 'sk-...')")
    
    api_key = input("\nAPI Key: ").strip()
    if api_key:
        _cached_api_key = api_key
    return api_key if api_key else None


def generate_with_openai(
    system_prompt: str,
    user_prompt: str,
    config: dict[str, Any],
) -> str:
    """Call OpenAI API to generate mind map."""
    # Use mindmap model configuration
    model_config = get_model_config(config, "mindmap")
    model = model_config["name"]
    temperature = model_config["temperature"]
    max_completion_tokens = model_config["max_completion_tokens"]
    api_base = model_config["api_base"]
    
    # Get API key
    api_key = get_api_key()
    if not api_key:
        raise ValueError("No API key provided")
    
    # Create client with optional base URL
    client_kwargs = {"api_key": api_key}
    if api_base:
        client_kwargs["base_url"] = api_base
    
    client = OpenAI(**client_kwargs)
    
    try:
        is_codex = is_codex_model(model)
        use_chat_api = is_chat_model(model) and not is_codex
        
        if is_codex:
            # Codex models are now served via the Responses API
            response = client.responses.create(
                model=model,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                # Some Codex models reject temperature; rely on defaults.
                max_output_tokens=max_completion_tokens,
            )
            return response.output_text
        elif use_chat_api:
            # Chat models use /v1/chat/completions
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_completion_tokens=max_completion_tokens,
            )
            return response.choices[0].message.content
        else:
            # Completion models use /v1/completions
            # Combine system and user prompts
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            # Completion API uses max_tokens instead of max_completion_tokens
            # Use max_tokens if available, otherwise use max_completion_tokens
            max_tokens = model_config.get("max_tokens", max_completion_tokens)
            
            response = client.completions.create(
                model=model,
                prompt=full_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].text
    except Exception as e:
        error_msg = str(e)
        # Provide a clearer hint when an unsupported completion model is used
        if "model is not supported" in error_msg.lower():
            raise ValueError(
                f"Model '{model}' is not supported on the current endpoint. "
                "Codex-style models (e.g., gpt-5.1-codex) now require the Responses API. "
                "Use Responses API for Codex models or a chat model such as gpt-4.1, gpt-4o, or o1 via /v1/chat/completions."
            ) from e
        if "Connection" in error_msg or "getaddrinfo" in error_msg:
            print("\n❌ Network connection error!")
            print("   Possible causes:")
            print("   1. No internet connection")
            print("   2. Firewall blocking OpenAI API")
            print("   3. Proxy settings needed")
            print("\n💡 Solution:")
            print("   - Check your internet connection")
            print("   - Configure proxy in config: api_base = 'your-proxy-url'")
            print("   - Or use the saved prompt manually:")
            prompt_config = config.get("prompt", {})
            prompt_dir = Path(prompt_config.get("directory", "tools/prompts/generated"))
            prompt_filename = prompt_config.get("filename", "mindmap_prompt")
            prompt_file = prompt_dir / f"{prompt_filename}.md"
            if prompt_file.exists():
                print(f"   Prompt saved at: {prompt_file}")
        raise


def find_existing_prompt(prompt_dir: Path, filename: str) -> Path | None:
    """Find existing prompt file (single file, no timestamp)."""
    if not prompt_dir.exists():
        return None
    
    prompt_file = prompt_dir / f"{filename}.md"
    if prompt_file.exists():
        return prompt_file
    
    return None


def save_prompt(system_prompt: str, user_prompt: str, config: dict[str, Any]) -> Path | None:
    """Save prompt to file (overwrites existing, no timestamp)."""
    prompt_config = config.get("prompt", {})
    
    if not prompt_config.get("save", True):
        return None
    
    prompt_dir = Path(prompt_config.get("directory", "tools/prompts/generated"))
    prompt_dir.mkdir(parents=True, exist_ok=True)
    
    filename = prompt_config.get("filename", "mindmap_prompt")
    prompt_file = prompt_dir / f"{filename}.md"
    
    prompt_file.write_text(
        f"# System Prompt\n\n{system_prompt}\n\n---\n\n# User Prompt\n\n{user_prompt}",
        encoding="utf-8"
    )
    
    return prompt_file


def optimize_prompt_with_ai(
    existing_system_prompt: str,
    existing_user_prompt: str,
    config: dict[str, Any],
) -> tuple[str, str]:
    """Let AI optimize the existing prompt.
    
    Args:
        existing_system_prompt: Current system prompt
        existing_user_prompt: Current user prompt
        config: Configuration dict
        
    Returns:
        Tuple of (optimized_system_prompt, optimized_user_prompt)
    """
    if not HAS_OPENAI:
        print("⚠️  OpenAI library not installed. Cannot optimize prompt.")
        return existing_system_prompt, existing_user_prompt
    
    # Use prompt model configuration
    model_config = get_model_config(config, "prompt")
    model = model_config["name"]
    temperature = model_config["temperature"]
    max_completion_tokens = model_config["max_completion_tokens"]
    api_base = model_config["api_base"]
    
    # Get API key
    api_key = get_api_key()
    if not api_key:
        print("⚠️  No API key provided. Cannot optimize prompt.")
        return existing_system_prompt, existing_user_prompt
    
    # Create client
    client_kwargs = {"api_key": api_key}
    if api_base:
        client_kwargs["base_url"] = api_base
    
    client = OpenAI(**client_kwargs)
    
    # Build optimization prompt
    optimization_system_prompt = dedent("""
    You are an expert prompt engineer specializing in optimizing prompts for AI models.
    Your task is to improve prompts to be more effective, clear, and structured while
    maintaining their original intent and functionality.
    
    When optimizing prompts:
    1. Enhance clarity and structure
    2. Improve instructions and examples
    3. Maintain all critical requirements and constraints
    4. Keep the same format and output requirements
    5. Make the prompt more effective for the target task
    """).strip()
    
    # Extract instruction sections from user prompt (before data sections)
    user_prompt_sections = existing_user_prompt.split("## 📊 Data Summary")
    user_instructions = user_prompt_sections[0] if user_prompt_sections else existing_user_prompt[:2000]
    
    optimization_user_prompt = dedent(f"""
    Please optimize the following prompt for generating LeetCode mind maps.
    
    The prompt consists of two parts:
    1. System Prompt: Defines the AI's role and capabilities
    2. User Prompt: Contains instructions and data for generating mind maps
    
    IMPORTANT: The User Prompt contains large JSON data sections that should NOT be modified.
    Only optimize the instruction sections (before "## 📊 Data Summary").
    
    Please optimize both parts to be more effective while maintaining:
    - All critical requirements (link rules, format requirements, etc.)
    - The same structure and organization
    - All data sections (JSON blocks) unchanged
    
    Return the optimized prompt in the same format:
    - Start with "# System Prompt" followed by the optimized system prompt
    - Then "---" separator  
    - Then "# User Prompt" followed by ONLY the optimized instruction sections
      (do NOT include the data sections - they will be appended separately)
    
    Current System Prompt:
    {existing_system_prompt}
    
    ---
    
    Current User Prompt Instructions (to optimize):
    {user_instructions}
    
    (Note: The actual data sections will be preserved and appended after optimization)
    """).strip()
    
    try:
        print("   🤖 Calling AI to optimize prompt...")
        
        # Determine if model is chat or completion model
        is_codex = is_codex_model(model)
        use_chat_api = is_chat_model(model) and not is_codex
        
        if is_codex:
            response = client.responses.create(
                model=model,
                input=[
                    {"role": "system", "content": optimization_system_prompt},
                    {"role": "user", "content": optimization_user_prompt},
                ],
                # Some Codex models reject temperature; rely on defaults.
                max_output_tokens=max_completion_tokens,
            )
            optimized_content = response.output_text
        elif use_chat_api:
            # Chat models use /v1/chat/completions
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": optimization_system_prompt},
                    {"role": "user", "content": optimization_user_prompt},
                ],
                temperature=temperature,
                max_completion_tokens=max_completion_tokens,
            )
            optimized_content = response.choices[0].message.content
        else:
            # Completion models use /v1/completions
            full_prompt = f"{optimization_system_prompt}\n\n{optimization_user_prompt}"
            max_tokens = model_config.get("max_tokens", max_completion_tokens)
            
            response = client.completions.create(
                model=model,
                prompt=full_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            optimized_content = response.choices[0].text
        
        # Parse optimized prompt
        if "---" in optimized_content:
            parts = optimized_content.split("---", 1)
            optimized_system = parts[0].replace("# System Prompt", "").strip()
            optimized_user_instructions = parts[1].replace("# User Prompt", "").strip()
            
            # Reconstruct user prompt: optimized instructions + original data sections
            if len(user_prompt_sections) > 1:
                optimized_user = optimized_user_instructions + "\n\n## 📊 Data Summary" + "## 📊 Data Summary".join(user_prompt_sections[1:])
            else:
                optimized_user = optimized_user_instructions
            
            print("   ✅ Prompt optimized successfully!")
            return optimized_system, optimized_user
        else:
            print("⚠️  Could not parse optimized prompt, using original.")
            return existing_system_prompt, existing_user_prompt
            
    except Exception as e:
        print(f"⚠️  Error optimizing prompt: {e}")
        print("   Using original prompt instead.")
        return existing_system_prompt, existing_user_prompt


def ask_use_existing_prompt(existing_prompt_file: Path | None) -> str:
    """Ask user what to do with prompt.
    
    Returns:
        "load": Load and use existing prompt as-is (only if file exists)
        "optimize": Optimize existing prompt with AI
        "regenerate": Regenerate prompt from config and data
        "regenerate_and_optimize": Regenerate from config, then optimize with AI
    """
    if existing_prompt_file:
        mtime = datetime.fromtimestamp(existing_prompt_file.stat().st_mtime)
        print(f"\n📋 Found existing prompt: {existing_prompt_file.name}")
        print(f"   Last modified: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nOptions:")
        print("  [l] Load existing prompt (use as-is)")
        print("  [o] Optimize existing prompt by AI (will overwrite)")
        print("  [r] Regenerate prompt from config (will overwrite)")
        print("  [a] Regenerate from config + Optimize by AI (will overwrite)")
    else:
        print("\n📋 No existing prompt found.")
        print("\nOptions:")
        print("  [o] Generate prompt with AI (recommended)")
        print("  [r] Generate prompt from config (standard)")
    
    choice = input("\nChoice [default: r]: ").strip().lower()
    
    if existing_prompt_file and choice == "l":
        return "load"
    elif choice == "a" and existing_prompt_file:
        return "regenerate_and_optimize"
    elif choice == "o":
        return "optimize"
    else:
        return "regenerate"


def load_meta_description(lang: str, base_filename: str, config: dict[str, Any]) -> str | None:
    """Load meta description from configured file path or auto-detect.
    
    Args:
        lang: Language code (e.g., "en", "zh-TW")
        base_filename: Base filename without extension (e.g., "neetcode_ontology_ai")
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
    
    # Auto-detect: try tools/mindmaps/meta/{base_filename}_{lang}.txt
    from mindmaps.config import META_DESCRIPTIONS_DIR
    auto_path = META_DESCRIPTIONS_DIR / f"{base_filename}_{lang}.txt"
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
    output_config = config.get("output", {})
    output_dir = Path(output_config.get("directory", "docs/mindmaps"))
    html_dir = Path(output_config.get("html_directory", "docs/pages/mindmaps"))
    
    # Get base filename
    base_filename = output_config.get("filename", "neetcode_ontology_ai.md")
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
            import json
            try:
                languages = json.loads(language_setting)
            except:
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
        # Determine Markdown filename
        if len(languages) > 1:
            md_filename = f"{base_name}_{lang}.md"
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
            
            # Determine HTML filename
            if len(languages) > 1:
                html_filename = f"{base_name}_{lang}.html"
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
    prompt_filename = prompt_config.get("filename", "mindmap_prompt")
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
            # Save regenerated prompt (overwrites)
            save_prompt(system_prompt, user_prompt, config)
    elif prompt_action == "optimize":
        # Optimize existing prompt with AI
        if existing_prompt_file:
            prompt_model_config = get_model_config(config, "prompt")
            print(f"\n🤖 Optimizing existing prompt with AI (using {prompt_model_config['name']})...")
            prompt_content = existing_prompt_file.read_text(encoding="utf-8")
            
            # Parse existing prompt
            parts = prompt_content.split("\n---\n")
            if len(parts) >= 2:
                existing_system_prompt = parts[0].replace("# System Prompt", "").strip()
                existing_user_prompt = parts[1].replace("# User Prompt", "").strip()
                
                # Let AI optimize the prompt
                system_prompt, user_prompt = optimize_prompt_with_ai(
                    existing_system_prompt, existing_user_prompt, config
                )
                # Save optimized prompt (overwrites existing)
                prompt_file = save_prompt(system_prompt, user_prompt, config)
                if prompt_file:
                    print(f"📄 Optimized prompt saved: {prompt_file}")
            else:
                print("⚠️  Could not parse existing prompt, regenerating with AI instead...")
                # Generate base prompt first, then optimize
                base_system_prompt = build_system_prompt(config)
                base_user_prompt = build_user_prompt(
                    ontology_data, docs_patterns, meta_patterns, problems_data, config
                )
                # Optimize the base prompt
                system_prompt, user_prompt = optimize_prompt_with_ai(
                    base_system_prompt, base_user_prompt, config
                )
                prompt_file = save_prompt(system_prompt, user_prompt, config)
                if prompt_file:
                    print(f"📄 AI-generated prompt saved: {prompt_file}")
        else:
            # First time: Generate base prompt, then optimize with AI
            prompt_model_config = get_model_config(config, "prompt")
            print(f"\n🤖 Generating prompt with AI (using {prompt_model_config['name']})...")
            print("   Step 1: Building base prompt from config...")
            base_system_prompt = build_system_prompt(config)
            base_user_prompt = build_user_prompt(
                ontology_data, docs_patterns, meta_patterns, problems_data, config
            )
            
            print("   Step 2: Optimizing with AI...")
            # Let AI optimize the base prompt
            system_prompt, user_prompt = optimize_prompt_with_ai(
                base_system_prompt, base_user_prompt, config
            )
            # Save AI-optimized prompt
            prompt_file = save_prompt(system_prompt, user_prompt, config)
            if prompt_file:
                print(f"📄 AI-generated prompt saved: {prompt_file}")
    elif prompt_action == "regenerate_and_optimize":
        # Regenerate from config, then optimize with AI
        prompt_model_config = get_model_config(config, "prompt")
        print("\n📝 Regenerating prompt from config and data...")
        print("   Step 1: Building prompt from config...")
        base_system_prompt = build_system_prompt(config)
        base_user_prompt = build_user_prompt(
            ontology_data, docs_patterns, meta_patterns, problems_data, config
        )
        
        print(f"   Step 2: Optimizing with AI (using {prompt_model_config['name']})...")
        # Let AI optimize the regenerated prompt
        system_prompt, user_prompt = optimize_prompt_with_ai(
            base_system_prompt, base_user_prompt, config
        )
        # Save AI-optimized prompt (overwrites existing)
        prompt_file = save_prompt(system_prompt, user_prompt, config)
        if prompt_file:
            print(f"📄 Regenerated and optimized prompt saved: {prompt_file}")
    else:  # regenerate
        # Regenerate prompts from config and data
        print("\n📝 Regenerating prompt from config and data...")
        system_prompt = build_system_prompt(config)
        user_prompt = build_user_prompt(
            ontology_data, docs_patterns, meta_patterns, problems_data, config
        )
        # Save regenerated prompt (overwrites existing)
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
    print(f"   🗺️  Mind map generation: {mindmap_model_config['name']}")
    
    if not HAS_OPENAI:
        print("\n⚠️  OpenAI library not installed.")
        print("   Copy the prompt above to GPT-5.1-codex manually.")
        return ""
    
    # Get languages (support both string and list)
    advanced = config.get("advanced", {})
    language_setting = advanced.get("language", "en")
    
    # Debug: print language setting
    print(f"\n📋 Language setting: {language_setting} (type: {type(language_setting).__name__})")
    
    # Handle both string and list formats
    if isinstance(language_setting, list):
        languages = language_setting
    elif isinstance(language_setting, str):
        # Try to parse as JSON array if it looks like one
        if language_setting.startswith("[") and language_setting.endswith("]"):
            import json
            try:
                languages = json.loads(language_setting)
            except:
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
        
        # Show which model is being used for this generation
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
            
            # Generate content
            content = generate_with_openai(lang_system_prompt, lang_user_prompt, lang_config)
            
            # Fix link formats in tables to ensure they're clickable
            content = fix_table_links(content)
            
            # Apply post-processing to standardize links and add titles from cache
            # This ensures consistent link format: [LeetCode 11 - Container With Most Water](url) | [Solution](url)
            problems = load_problems()
            content = post_process_content(content, problems)
            print(f"   ✅ Post-processing applied (links standardized with titles)")
            
            all_contents[lang] = content
            
            # Save with language suffix
            if len(languages) > 1:
                lang_filename = f"{base_name}_{lang}.md"
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


def interactive_mode() -> dict[str, Any]:
    """Interactive mode for generating mind maps."""
    print("\n" + "="*60)
    print("🧠 AI Mind Map Generator for LeetCode")
    print("="*60)
    
    # Load default config
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
        help="Learning goal (overrides config): interview, systematic, quick_review, pattern_mastery, weakness_focus, creative"
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
        help="Generate HTML files from existing Markdown files without regenerating Markdown. "
             "Useful when you only want to update HTML output or meta descriptions."
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
        # If --model is specified, set both prompt and mindmap models to the same value
        # User can still override individually in config file
        config.setdefault("model", {})["name"] = args.model
        config.setdefault("model", {})["prompt_model"] = args.model
        config.setdefault("model", {})["mindmap_model"] = args.model
    
    # Show config if requested
    if args.list_config:
        print(json.dumps(config, indent=2, ensure_ascii=False))
        return 0
    
    # HTML-only mode: generate HTML from existing Markdown files
    if args.html_only:
        return generate_html_from_markdown(config)
    
    generate_mindmap_ai(config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
