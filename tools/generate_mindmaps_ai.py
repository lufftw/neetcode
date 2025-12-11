#!/usr/bin/env python3
"""
AI-Powered Mind Map Generator for LeetCode Practice

Automatically reads ontology data based on config and lets GPT models creatively
generate Markmap mind maps.

Usage:
    python tools/generate_mindmaps_ai.py                              # Interactive
    python tools/generate_mindmaps_ai.py --config mindmap_ai_config.toml
    python tools/generate_mindmaps_ai.py --goal interview
    python tools/generate_mindmaps_ai.py --topic sliding_window

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
from mindmaps.data import ProblemData
from mindmaps.toml_parser import parse_toml_simple

# Try to import OpenAI
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Paths
PROJECT_ROOT = TOOLS_DIR.parent
ONTOLOGY_DIR = PROJECT_ROOT / "ontology"
DOCS_PATTERNS_DIR = PROJECT_ROOT / "docs" / "patterns"
META_PATTERNS_DIR = PROJECT_ROOT / "meta" / "patterns"
DEFAULT_CONFIG = TOOLS_DIR / "mindmap_ai_config.toml"
DEFAULT_MODEL = "gpt-5.1"


def load_config(config_path: Path | None = None) -> dict[str, Any]:
    """Load configuration from TOML file."""
    if config_path is None:
        config_path = DEFAULT_CONFIG
    
    if not config_path.exists():
        print(f"⚠️  Config not found: {config_path}, using defaults")
        return get_default_config()
    
    return parse_toml_simple(config_path.read_text(encoding="utf-8"))


def get_default_config() -> dict[str, Any]:
    """Return default configuration."""
    return {
        "model": {"name": DEFAULT_MODEL, "temperature": 0.7, "max_completion_tokens": 8000},
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
        "advanced": {"include_full_code": True, "include_complexity": True, "include_leetcode_links": True, "include_solution_links": True, "language": "zh-TW"},
        "links": {
            "leetcode_base": "https://leetcode.com/problems",
            "github_repo": "https://github.com/lufftw/neetcode",
            "github_branch": "main",
            "solution_path_template": "solutions/{slug}.py",
        },
    }


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
    """Load pattern documentation from docs/patterns/."""
    docs_config = config.get("docs", {}).get("patterns", {})
    
    if not docs_config.get("enabled", True):
        return {}
    
    if not DOCS_PATTERNS_DIR.exists():
        return {}
    
    include = docs_config.get("include", [])
    exclude = docs_config.get("exclude", ["README"])
    
    docs = {}
    for md_file in DOCS_PATTERNS_DIR.glob("*.md"):
        name = md_file.stem
        
        # Filter by include/exclude
        if include and name not in include:
            continue
        if name in exclude:
            continue
        
        docs[name] = md_file.read_text(encoding="utf-8")
    
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
    """Build system prompt based on config. Prompt is always in English, but output language is configurable."""
    advanced = config.get("advanced", {})
    language = advanced.get("language", "en")
    
    # Handle list of languages - use first one for system prompt
    if isinstance(language, list):
        language = language[0] if language else "en"
    
    # Language instructions for output (prompt itself is always English)
    lang_instructions = {
        "en": "IMPORTANT: Generate the mind map content in English. All titles, labels, and descriptions should be in English.",
        "zh-TW": "IMPORTANT: Generate the mind map content in Traditional Chinese (繁體中文). All titles, labels, and descriptions should be in Traditional Chinese.",
        "zh-CN": "IMPORTANT: Generate the mind map content in Simplified Chinese (简体中文). All titles, labels, and descriptions should be in Simplified Chinese.",
    }
    
    return dedent(f"""
    You are a world-class expert who seamlessly integrates multiple professional perspectives 
    into a unified, comprehensive understanding:
    
    **As a Top Software Architect**, you design elegant, scalable system architectures and 
    understand how algorithms fit into larger software systems. You think in abstractions, 
    patterns, and maintainable code structures.
    
    **As a Distinguished Senior Algorithm Professor**, you have decades of experience teaching 
    algorithms at the highest level. You understand theoretical foundations, explain complex 
    concepts clearly, and know how students learn best. You bridge theory and practice seamlessly.
    
    **As a Senior Principal Engineer**, you've built production systems at scale. You know 
    which algorithms work in practice, which fail under load, and how to optimize real-world 
    performance. You understand trade-offs and engineering constraints.
    
    **As a Technical Architecture & Language API Provider**, you design APIs and language 
    features used by millions. You know how to expose algorithmic concepts through clean 
    interfaces and structure knowledge for maximum usability.
    
    **As a LeetCode Learner & Interview Preparer**, you understand the journey from beginner 
    to expert. You know which problems build foundational skills, which patterns appear 
    frequently in interviews, and how to structure learning paths that lead to success.
    
    **As a Competitive Programming Champion**, you've solved thousands of problems under 
    time pressure. You recognize patterns instantly, know optimization tricks, and understand 
    the mental models that separate good solutions from great ones.
    
    **As a Project Contributor & Open Source Advocate**, you understand what makes a project 
    valuable to the community. You know how to structure knowledge so it's discoverable, 
    maintainable, and helps others contribute effectively.
    
    These perspectives are not separate—they inform each other. Your architectural thinking 
    enhances your teaching. Your engineering experience grounds your theoretical knowledge. 
    Your competitive programming skills inform your interview preparation. Your API design 
    sense helps you structure knowledge for learners. You synthesize all these insights 
    into mind maps that are simultaneously theoretically sound, practically applicable, 
    pedagogically effective, and architecturally elegant.

    Your task is to creatively generate Markmap-format mind maps based on the provided LeetCode 
    knowledge graph data, drawing from this unified expertise to create mind maps that serve 
    learners, interview candidates, competitive programmers, and contributors alike.

    {lang_instructions.get(language, lang_instructions["en"])}

    ## Your Capabilities

    1. **Deep Understanding of Knowledge Graph**: Analyze relationships between API Kernels, Patterns, 
       Algorithms, and Data Structures
    2. **Creative Visualization**: Design intuitive, beautiful, and educational mind map structures
    3. **Personalized Recommendations**: Adjust content based on user goals
    4. **Importance Identification**: Automatically determine which content is most important for learners

    ## Markmap Features (Please Utilize Fully)

    - **Links**: [Problem Name](URL) - Use links for all problem references!
    - **Styling**: **bold**, *italic*, ==highlight==, ~~strikethrough~~, `code`
    - **Checkboxes**: [ ] To-do, [x] Completed
    - **Math Formulas**: $O(n \\log n)$, $O(n^2)$
    - **Code Blocks**: ```python ... ```
    - **Tables**: | A | B | ... |
    - **Fold**: <!-- markmap: fold -->
    - **Emoji**: For visual emphasis 🎯📚⚡🔥

    ## CRITICAL: Problem Links Rule

    **Every time you mention a LeetCode problem with its number, you MUST add a clickable link.**

    Link Selection Logic (check Problem Data in user prompt):
    1. Find the problem in the provided Problem Data JSON
    2. Check the `solution_file` field:
       - **If `solution_file` is NOT empty AND not null** → Link to GitHub solution
         Format: `{github_repo}/blob/{github_branch}/{solution_file}`
       - **If `solution_file` is empty, null, or missing** → Link to LeetCode problem page
         Format: `{leetcode_base}/{slug}/`
    
    IMPORTANT: 
    - Check `solution_file` field value carefully - it must be a non-empty string
    - Empty string `""` or `null` means NO solution file exists
    - Only use GitHub link when `solution_file` has an actual file path value

    Examples:
    - Problem WITH solution (solution_file = "solutions/0003_xxx.py"):
      `[LeetCode 3 - Longest Substring](https://github.com/lufftw/neetcode/blob/main/solutions/0003_xxx.py)`
    - Problem WITHOUT solution (solution_file = "" or null):
      `[LeetCode 999 - Some Problem](https://leetcode.com/problems/some-problem/)`

    **Never mention a problem number without a link!**

    ## Output Format

    Must be valid Markmap Markdown, starting with this frontmatter:

    ```
    ---
    title: [Mind Map Title]
    markmap:
      colorFreezeLevel: 2
      maxWidth: 300
    ---
    ```

    ## Design Principles

    1. **Clear Hierarchy**: 3-5 levels optimal
    2. **Highlight Key Points**: Use bold and highlight to mark key concepts
    3. **Practical Orientation**: Associate each concept with specific problems
    4. **Beautiful and Readable**: Use emoji and color layers effectively
    5. **Learning-Friendly**: Include progress tracking and difficulty markers

    ## Important Naming Conventions

    - **Always use full name**: Always write "LeetCode" in full, never use abbreviations like "LC" or "LC problem"
    - **Problem references**: Use format "LeetCode 1 - Two Sum" or "LeetCode Problem 1", never "LC 1"
    - **Consistency**: Maintain consistent naming throughout the mind map

    Output Markmap Markdown directly, without any explanations or preambles.
    """).strip()


def build_user_prompt(
    ontology_data: dict[str, Any],
    docs_patterns: dict[str, str],
    meta_patterns: dict[str, dict[str, str]],
    problems_data: list[dict[str, Any]],
    config: dict[str, Any],
) -> str:
    """Build user prompt with all context from config."""
    generation = config.get("generation", {})
    advanced = config.get("advanced", {})
    
    language = advanced.get("language", "en")
    
    sections = []
    
    # === Summary === (Always in English for prompt)
    summary_lines = ["## 📊 Data Summary\n"]
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
        sections.append("## 📚 Ontology Knowledge Graph\n")
        sections.append("```json")
        sections.append(json.dumps(ontology_data, indent=2, ensure_ascii=False))
        sections.append("```")
    
    # === Pattern Documentation ===
    if docs_patterns:
        sections.append("\n## 📖 Pattern Documentation\n")
        for name, content in docs_patterns.items():
            sections.append(f"### {name}\n")
            # Truncate if too long
            if len(content) > 8000:
                sections.append(content[:8000] + "\n...(truncated)")
            else:
                sections.append(content)
    
    # === Meta Pattern Snippets ===
    if meta_patterns:
        sections.append("\n## 🧩 Pattern Snippets\n")
        for pattern_name, snippets in meta_patterns.items():
            sections.append(f"### {pattern_name}\n")
            for filename, content in snippets.items():
                sections.append(f"#### {filename}\n")
                if len(content) > 2000:
                    sections.append(content[:2000] + "\n...(truncated)")
                else:
                    sections.append(content)
    
    # === Problems ===
    if problems_data:
        sections.append("\n## 🎯 Problem Data\n")
        sections.append("```json")
        sections.append(json.dumps(problems_data, indent=2, ensure_ascii=False))
        sections.append("```")
    
    # === Link Format Instructions ===
    links_config = config.get("links", {})
    if links_config:
        sections.append("\n## 🔗 Link Format Instructions\n")
        
        leetcode_base = links_config.get("leetcode_base", "https://leetcode.com/problems")
        github_repo = links_config.get("github_repo", "https://github.com/lufftw/neetcode")
        github_branch = links_config.get("github_branch", "main")
        solution_template = links_config.get("solution_path_template", "solutions/{slug}.py")
        
        link_instructions = [
            "## Link Generation Rules",
            "",
            "**EVERY problem mention with a number MUST have a clickable link.**",
            "",
            "### Decision Logic",
            "1. Look up the problem in the Problem Data above",
            "2. Check `solution_file` field:",
            f"   - **NOT empty** → GitHub: `{github_repo}/blob/{github_branch}/{{solution_file}}`",
            f"   - **Empty or not found** → LeetCode: `{leetcode_base}/{{slug}}/`",
            "",
            "### Link Format in Markdown",
            "```markdown",
            "[LeetCode {id} - {title}](URL)",
            "```",
            "",
            "### Examples from Problem Data",
            "",
            "**Problem 3 (HAS solution):**",
            "- `solution_file`: `solutions/0003_longest_substring_without_repeating_characters.py`",
            f"- Link: `[LeetCode 3 - Longest Substring...]({github_repo}/blob/{github_branch}/solutions/0003_longest_substring_without_repeating_characters.py)`",
            "",
            "**Problem not in data (NO solution):**",
            f"- Link: `[LeetCode 121 - Best Time to Buy...]({leetcode_base}/best-time-to-buy-and-sell-stock/)`",
            "",
            "### Slug Format",
            "- LeetCode slug: lowercase with hyphens (e.g., `two-sum`, `best-time-to-buy-and-sell-stock`)",
            "- Can extract from `url` field in problem data",
        ]
        
        sections.append("\n".join(link_instructions))
    
    # === Generation Instructions ===
    language = advanced.get("language", "en")
    
    # Handle list of languages - use first one for generation instructions
    if isinstance(language, list):
        language = language[0] if language else "en"
    
    if language == "en":
        sections.append("\n## 🎨 Generation Instructions\n")
        
        goal = generation.get("goal", "creative")
        focus_topic = generation.get("focus_topic", "")
        style = generation.get("style", "balanced")
        custom = generation.get("custom_instructions", "")
        
        goal_prompts = {
            "interview": "Generate an **interview-focused** mind map, emphasizing high-frequency problems, company preferences, and interview techniques. Mark must-solve problems.",
            "systematic": "Generate a **systematic learning roadmap**, sorted by difficulty and dependencies, including progress tracking checkboxes.",
            "quick_review": "Generate a **concise review** mind map with only the core patterns and key problems, suitable for quick pre-interview browsing.",
            "pattern_mastery": "Generate an **in-depth pattern analysis** mind map showing relationships between patterns, variants, and code templates.",
            "weakness_focus": "Analyze problem data to identify less-covered areas and generate a **targeted practice** mind map.",
            "creative": "Based on the overall knowledge graph, **creatively** generate a mind map you believe is most helpful for LeetCode practice. It can be a decision tree, learning path, or any innovative structure.",
        }
        
        sections.append(goal_prompts.get(goal, f"Goal: {goal}"))
        
        if focus_topic:
            sections.append(f"\n**Focus Topic**: `{focus_topic}` - Please expand the mind map around this core.")
        
        style_prompts = {
            "creative": "**Style**: Creativity first, use non-traditional structures and visual elements that catch the eye.",
            "academic": "**Style**: Academic rigor, focus on logical hierarchy and complexity analysis.",
            "practical": "**Style**: Practical orientation, use code templates and concrete examples.",
            "minimal": "**Style**: Minimalist style, keep only the most essential content.",
            "balanced": "**Style**: Balance beauty and practicality, suitable for most learners.",
        }
        sections.append(f"\n{style_prompts.get(style, '')}")
        
        if custom:
            sections.append(f"\n**Additional Instructions**: {custom}")
        
        # Advanced options
        if not advanced.get("include_leetcode_links", True):
            sections.append("\nNote: Do not include LeetCode links.")
        if not advanced.get("include_complexity", True):
            sections.append("\nNote: Complexity analysis is not needed.")
    
    return "\n".join(sections)


# Cache for API key (avoid asking multiple times)
_cached_api_key: str | None = None


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
    model_config = config.get("model", {})
    model = model_config.get("name", DEFAULT_MODEL)
    temperature = float(model_config.get("temperature", 0.7))
    max_completion_tokens = int(model_config.get("max_completion_tokens", 8000))
    api_base = model_config.get("api_base", "")
    
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
        # GPT-5.1 and newer models use max_completion_tokens
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
    except Exception as e:
        error_msg = str(e)
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
    
    model_config = config.get("model", {})
    model = model_config.get("name", DEFAULT_MODEL)
    temperature = float(model_config.get("temperature", 0.7))
    max_completion_tokens = int(model_config.get("max_completion_tokens", 8000))
    api_base = model_config.get("api_base", "")
    
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
            print(f"\n🤖 Optimizing existing prompt with AI...")
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
            print(f"\n🤖 Generating prompt with AI...")
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
        print("\n📝 Regenerating prompt from config and data...")
        print("   Step 1: Building prompt from config...")
        base_system_prompt = build_system_prompt(config)
        base_user_prompt = build_user_prompt(
            ontology_data, docs_patterns, meta_patterns, problems_data, config
        )
        
        print("   Step 2: Optimizing with AI...")
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
    
    model_name = config.get("model", {}).get("name", DEFAULT_MODEL)
    print(f"\n🤖 Generating with {model_name}...")
    
    if not HAS_OPENAI:
        print("\n⚠️  OpenAI library not installed.")
        print("   Copy the prompt above to GPT-5.1 manually.")
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
                
                html_content = generate_html_mindmap(title, content, use_autoloader=False)
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
    
    # Show config if requested
    if args.list_config:
        print(json.dumps(config, indent=2, ensure_ascii=False))
        return 0
    
    generate_mindmap_ai(config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
