"""
AI Mind Map Generator Module

This package provides functionality for AI-powered mind map generation
for LeetCode practice.

Modules:
- config: Configuration loading and defaults
- prompts: Prompt building and loading
- data_loader: Data loading (ontology, patterns, problems)
- openai_client: OpenAI API interactions
- prompt_manager: Prompt file management and optimization
- html_generator: HTML generation from markdown
"""

from .config import (
    load_config,
    get_model_config,
    get_default_config,
    DEFAULT_MODEL,
)
from .prompts import (
    load_prompts_config,
    load_system_prompt_template,
    build_system_prompt,
    build_user_prompt,
)
from .data_loader import (
    load_ontology_data,
    load_docs_patterns,
    load_meta_patterns,
    load_problems_data,
)
from .openai_client import (
    is_codex_model,
    is_chat_model,
    get_api_key,
    generate_with_openai,
)
from .prompt_manager import (
    find_existing_prompt,
    save_prompt,
    optimize_prompt_with_ai,
    ask_use_existing_prompt,
)
from .html_generator import (
    load_meta_description,
    generate_html_from_markdown,
)

__all__ = [
    # config
    "load_config",
    "get_model_config",
    "get_default_config",
    "DEFAULT_MODEL",
    # prompts
    "load_prompts_config",
    "load_system_prompt_template",
    "build_system_prompt",
    "build_user_prompt",
    # data_loader
    "load_ontology_data",
    "load_docs_patterns",
    "load_meta_patterns",
    "load_problems_data",
    # openai_client
    "is_codex_model",
    "is_chat_model",
    "get_api_key",
    "generate_with_openai",
    # prompt_manager
    "find_existing_prompt",
    "save_prompt",
    "optimize_prompt_with_ai",
    "ask_use_existing_prompt",
    # html_generator
    "load_meta_description",
    "generate_html_from_markdown",
]

