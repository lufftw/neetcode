"""
Prompt file management for AI Mind Map Generator.

Handles saving, loading, and optimizing prompts.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import Any

# Try to import OpenAI
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    OpenAI = None  # type: ignore

from .config import get_model_config
from .openai_client import get_api_key, is_codex_model, is_chat_model


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

