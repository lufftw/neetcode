"""
Configuration loading and defaults for AI Mind Map Generator.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

# Paths
# From tools/mindmaps/ai_mindmap/config.py:
#   parent -> tools/mindmaps/ai_mindmap
#   parent.parent -> tools/mindmaps
#   parent.parent.parent -> tools
#   parent.parent.parent.parent -> project root
TOOLS_DIR = Path(__file__).parent.parent.parent  # tools/mindmaps/ai_mindmap -> tools
MINDMAPS_DIR = Path(__file__).parent.parent  # tools/mindmaps/ai_mindmap -> tools/mindmaps
PROJECT_ROOT = TOOLS_DIR.parent  # tools -> project root

# Default model - use a chat model available via /v1/chat/completions
DEFAULT_MODEL = "gpt-4.1"
DEFAULT_CONFIG_PATH = MINDMAPS_DIR / "generate_mindmaps_ai.toml"


def load_config(config_path: Path | None = None) -> dict[str, Any]:
    """Load configuration from TOML file."""
    from mindmaps.toml_parser import parse_toml_simple
    
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH
    
    if not config_path.exists():
        print(f"⚠️  Config not found: {config_path}, using defaults")
        return get_default_config()
    
    return parse_toml_simple(config_path.read_text(encoding="utf-8"))


def get_model_config(config: dict[str, Any], model_type: str = "mindmap") -> dict[str, Any]:
    """
    Get model configuration for a specific purpose.
    
    Args:
        config: The full configuration dictionary
        model_type: Either "prompt" for prompt optimization or "mindmap" for generation
    
    Returns:
        Dict with model name, temperature, max_completion_tokens, and api_base
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

