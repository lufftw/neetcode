"""
Prompt building and loading for AI Mind Map Generator.
"""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent
from typing import Any

# Try to import yaml
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Paths
TOOLS_DIR = Path(__file__).parent.parent
PROMPTS_DIR = TOOLS_DIR / "prompts"

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
    prompt_path = PROMPTS_DIR / "system-prompt.md"
    
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
    
    When mentioning LeetCode problems, use this simplified format:
    - `LeetCode {number}` or `LeetCode {number} - {title}`
    - Use full "LeetCode" not "LC"
    - DO NOT include URLs or links - post-processing will add them automatically
    - DO NOT use markdown link syntax like `[LeetCode X](url)`
    
    Example:
    - ✅ Correct: `LeetCode 11` or `LeetCode 11 - Container With Most Water`
    - ❌ Wrong: `[LeetCode 11](url)` or `LC 11` or `LeetCode 11 - Container With Most Water · [Solution](url)`
    
    Post-processing will automatically convert all `LeetCode N` references to complete links
    with titles and solution URLs. You only need to output the plain text format.
    
    Output Markmap Markdown directly, without any explanations.
    """).strip()


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
        problems_note = sections_config.get(
            "problems_note",
            "**Important:** Use simplified format `LeetCode {leetcode_id}` or `LeetCode {leetcode_id} - {title}` "
            "when referencing problems. Use full \"LeetCode\" not \"LC\". "
            "DO NOT include URLs or markdown links - post-processing will add them automatically.\n"
        )
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

