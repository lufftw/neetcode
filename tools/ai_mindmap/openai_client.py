"""
OpenAI API client for AI Mind Map Generator.

Handles API key management and model calls.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

# Try to import OpenAI
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    OpenAI = None  # type: ignore

from .config import get_model_config

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
    if not HAS_OPENAI:
        raise ImportError("OpenAI package not installed. Run: pip install openai")
    
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
            prompt_filename = prompt_config.get("filename", "mindmap-prompt")
            prompt_file = prompt_dir / f"{prompt_filename}.md"
            if prompt_file.exists():
                print(f"   Prompt saved at: {prompt_file}")
        raise

