#!/usr/bin/env python3
"""
Text to Mind Map Generator

Converts ANY text input into structured mind maps using LLM.
Supports multiple output formats: Markdown, Mermaid, Markmap HTML.

Usage:
    python tools/text_to_mindmap.py --input "Your text here"
    python tools/text_to_mindmap.py --file input.txt
    python tools/text_to_mindmap.py --file input.txt --format mermaid
    python tools/text_to_mindmap.py --file input.txt --format html --output mindmap.html

Supported LLM Backends:
    - OpenAI (GPT-4, GPT-3.5)
    - Anthropic (Claude)
    - Ollama (Local)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Literal

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "docs" / "mindmaps" / "generated"

# Output format types
OutputFormat = Literal["markdown", "mermaid", "html", "json"]

# ---------------------------------------------------------------------------
# LLM Prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are an expert at analyzing text and creating structured mind maps.
Your task is to:
1. Identify the main topic/theme
2. Extract key concepts and their relationships
3. Organize into a hierarchical structure (max 4 levels deep)
4. Output in the requested format

Rules:
- Keep node labels concise (max 5 words)
- Maximum 30 nodes total
- Group related concepts together
- Identify the most important relationships
"""

MARKDOWN_PROMPT = """Convert this text into a Markdown mind map structure using headings:

TEXT:
{text}

Output ONLY the Markdown, using:
- # for main topic
- ## for major branches
- ### for sub-branches
- #### for details
- Use bullet points for leaf nodes if needed

Example output:
# Main Topic
## Branch 1
### Sub-branch 1.1
- Detail A
- Detail B
### Sub-branch 1.2
## Branch 2
"""

MERMAID_PROMPT = """Convert this text into a Mermaid mindmap diagram:

TEXT:
{text}

Output ONLY the Mermaid code block, like:
```mermaid
mindmap
  root((Main Topic))
    Branch 1
      Sub-branch 1.1
      Sub-branch 1.2
    Branch 2
      Sub-branch 2.1
```

Keep it readable with max 30 nodes.
"""

JSON_PROMPT = """Convert this text into a JSON mind map structure:

TEXT:
{text}

Output ONLY valid JSON with this structure:
{{
  "root": "Main Topic",
  "children": [
    {{
      "name": "Branch 1",
      "children": [
        {{"name": "Sub-branch 1.1"}},
        {{"name": "Sub-branch 1.2"}}
      ]
    }},
    {{
      "name": "Branch 2",
      "children": []
    }}
  ]
}}
"""

# ---------------------------------------------------------------------------
# LLM Backends
# ---------------------------------------------------------------------------

def call_openai(prompt: str, model: str = "gpt-4") -> str:
    """Call OpenAI API."""
    try:
        from openai import OpenAI
        client = OpenAI()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except ImportError:
        raise RuntimeError("openai package not installed. Run: pip install openai")
    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {e}")


def call_anthropic(prompt: str, model: str = "claude-3-sonnet-20240229") -> str:
    """Call Anthropic API."""
    try:
        import anthropic
        client = anthropic.Anthropic()
        response = client.messages.create(
            model=model,
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        return response.content[0].text
    except ImportError:
        raise RuntimeError("anthropic package not installed. Run: pip install anthropic")
    except Exception as e:
        raise RuntimeError(f"Anthropic API error: {e}")


def call_ollama(prompt: str, model: str = "llama3") -> str:
    """Call local Ollama API."""
    try:
        import requests
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": f"{SYSTEM_PROMPT}\n\n{prompt}",
                "stream": False,
            },
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["response"]
    except ImportError:
        raise RuntimeError("requests package not installed. Run: pip install requests")
    except Exception as e:
        raise RuntimeError(f"Ollama API error: {e}")


def call_llm(prompt: str, backend: str = "openai", model: str | None = None) -> str:
    """Call the specified LLM backend."""
    backends = {
        "openai": (call_openai, "gpt-4"),
        "anthropic": (call_anthropic, "claude-3-sonnet-20240229"),
        "ollama": (call_ollama, "llama3"),
    }
    
    if backend not in backends:
        raise ValueError(f"Unknown backend: {backend}. Choose from: {list(backends.keys())}")
    
    func, default_model = backends[backend]
    return func(prompt, model or default_model)


# ---------------------------------------------------------------------------
# Text to Mind Map Conversion
# ---------------------------------------------------------------------------

def text_to_markdown(text: str, backend: str = "openai") -> str:
    """Convert text to Markdown mind map structure."""
    prompt = MARKDOWN_PROMPT.format(text=text)
    return call_llm(prompt, backend)


def text_to_mermaid(text: str, backend: str = "openai") -> str:
    """Convert text to Mermaid mindmap syntax."""
    prompt = MERMAID_PROMPT.format(text=text)
    result = call_llm(prompt, backend)
    
    # Clean up: ensure it's wrapped in mermaid code block
    if "```mermaid" not in result:
        result = f"```mermaid\n{result}\n```"
    
    return result


def text_to_json(text: str, backend: str = "openai") -> dict:
    """Convert text to JSON mind map structure."""
    prompt = JSON_PROMPT.format(text=text)
    result = call_llm(prompt, backend)
    
    # Extract JSON from response
    if "```json" in result:
        result = result.split("```json")[1].split("```")[0]
    elif "```" in result:
        result = result.split("```")[1].split("```")[0]
    
    return json.loads(result.strip())


def json_to_markmap_html(json_data: dict, title: str = "Mind Map") -> str:
    """Convert JSON mind map to interactive Markmap HTML."""
    
    def json_to_markdown(node: dict, level: int = 1) -> str:
        """Recursively convert JSON to Markdown."""
        prefix = "#" * level
        name = node.get("name", node.get("root", ""))
        lines = [f"{prefix} {name}"]
        
        for child in node.get("children", []):
            lines.append(json_to_markdown(child, level + 1))
        
        return "\n".join(lines)
    
    markdown_content = json_to_markdown({"name": json_data.get("root", "Mind Map"), "children": json_data.get("children", [])})
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ margin: 0; padding: 0; }}
        #mindmap {{ width: 100vw; height: 100vh; }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
    <script src="https://cdn.jsdelivr.net/npm/markmap-view"></script>
    <script src="https://cdn.jsdelivr.net/npm/markmap-lib"></script>
</head>
<body>
    <svg id="mindmap"></svg>
    <script>
        const {{ Transformer, Markmap, loadCSS, loadJS }} = window.markmap;
        const transformer = new Transformer();
        
        const markdown = `{markdown_content}`;
        
        const {{ root }} = transformer.transform(markdown);
        
        Markmap.create('#mindmap', null, root);
    </script>
</body>
</html>"""
    
    return html


def text_to_html(text: str, backend: str = "openai", title: str = "Mind Map") -> str:
    """Convert text directly to interactive Markmap HTML."""
    json_data = text_to_json(text, backend)
    return json_to_markmap_html(json_data, title)


# ---------------------------------------------------------------------------
# Main Conversion Function
# ---------------------------------------------------------------------------

def convert_text_to_mindmap(
    text: str,
    output_format: OutputFormat = "mermaid",
    backend: str = "openai",
    title: str = "Mind Map",
) -> str:
    """
    Convert any text to a mind map in the specified format.
    
    Args:
        text: Input text to convert
        output_format: Output format (markdown, mermaid, html, json)
        backend: LLM backend (openai, anthropic, ollama)
        title: Title for HTML output
        
    Returns:
        Mind map in the specified format
    """
    converters = {
        "markdown": lambda t: text_to_markdown(t, backend),
        "mermaid": lambda t: text_to_mermaid(t, backend),
        "json": lambda t: json.dumps(text_to_json(t, backend), indent=2),
        "html": lambda t: text_to_html(t, backend, title),
    }
    
    if output_format not in converters:
        raise ValueError(f"Unknown format: {output_format}")
    
    return converters[output_format](text)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert any text to mind map using LLM.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input", "-i",
        help="Input text directly",
    )
    parser.add_argument(
        "--file", "-f",
        type=Path,
        help="Input file path",
    )
    parser.add_argument(
        "--format", "-t",
        choices=["markdown", "mermaid", "json", "html"],
        default="mermaid",
        help="Output format (default: mermaid)",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--backend", "-b",
        choices=["openai", "anthropic", "ollama"],
        default="openai",
        help="LLM backend (default: openai)",
    )
    parser.add_argument(
        "--title",
        default="Mind Map",
        help="Title for HTML output",
    )
    
    args = parser.parse_args()
    
    # Get input text
    if args.input:
        text = args.input
    elif args.file:
        if not args.file.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            return 1
        text = args.file.read_text(encoding="utf-8")
    else:
        print("Error: Provide --input or --file", file=sys.stderr)
        return 1
    
    # Convert
    print(f"Converting text using {args.backend}...", file=sys.stderr)
    try:
        result = convert_text_to_mindmap(
            text=text,
            output_format=args.format,
            backend=args.backend,
            title=args.title,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    # Output
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
        print(f"Written: {args.output}", file=sys.stderr)
    else:
        print(result)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())


