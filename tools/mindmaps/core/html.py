# tools/mindmaps/html.py
"""HTML generation for mind maps."""

from __future__ import annotations
from pathlib import Path

from .templates import (
    HTML_TEMPLATE_MANUAL,
    HTML_TEMPLATE_AUTOLOADER,
    STYLE_CSS,
)


def markdown_to_html_content(markdown_content: str) -> str:
    """Extract markdown content without YAML frontmatter."""
    lines = markdown_content.split("\n")
    if lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                lines = lines[i + 1:]
                break
    return "\n".join(lines)


def generate_html_mindmap(
    title: str,
    markdown_content: str,
    use_autoloader: bool = False,
    description: str | None = None,
) -> str:
    """Generate HTML file with embedded markmap."""
    content = markdown_to_html_content(markdown_content)
    content_escaped = content.replace('`', '\\`').replace('$', '\\$')
    
    # Generate default description if not provided
    if description is None:
        description = f"Interactive mind map visualization of {title} from NeetCode Practice Framework. Explore algorithm patterns, problem relationships, and learning paths."
    
    # Escape description for HTML (escape quotes)
    description_escaped = description.replace('"', '&quot;')
    
    if use_autoloader:
        return HTML_TEMPLATE_AUTOLOADER.format(
            title=title,
            description=description_escaped,
            markdown_content=content
        )
    return HTML_TEMPLATE_MANUAL.format(
        title=title,
        description=description_escaped,
        markdown_content=content_escaped
    )


def setup_pages_directory(pages_dir: Path) -> None:
    """Create the GitHub Pages directory structure."""
    (pages_dir / "mindmaps").mkdir(parents=True, exist_ok=True)
    (pages_dir / "assets").mkdir(parents=True, exist_ok=True)
    
    style_path = pages_dir / "assets" / "style.css"
    style_path.write_text(STYLE_CSS, encoding="utf-8")
    print(f"  Written: {style_path}")

