# =============================================================================
# HTML Converter
# =============================================================================
# Converts Markdown Markmaps to interactive HTML using Markmap library.
# =============================================================================

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Template

from ..config_loader import ConfigLoader


class MarkMapHTMLConverter:
    """
    Converts Markdown content to interactive HTML Markmaps.
    
    Uses Jinja2 templates and the Markmap JavaScript library
    to generate standalone HTML files.
    """
    
    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialize the HTML converter.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or ConfigLoader.get_config()
        output_config = self.config.get("output", {})
        html_config = output_config.get("html", {})
        
        # Load template
        template_path = html_config.get("template", "templates/markmap.html")
        self.template = self._load_template(template_path)
        
        # HTML options
        self.include_styles = html_config.get("include_styles", True)
        self.include_scripts = html_config.get("include_scripts", True)
        self.default_title = html_config.get("title", "AI Generated Markmap")
        
        # Output directories
        final_dirs = output_config.get("final_dirs", {})
        base_dir = Path(__file__).parent.parent.parent
        
        self.md_output_dir = (base_dir / final_dirs.get("markdown", "outputs/final")).resolve()
        self.html_output_dir = (base_dir / final_dirs.get("html", "outputs/final")).resolve()
        
        # Ensure directories exist
        self.md_output_dir.mkdir(parents=True, exist_ok=True)
        self.html_output_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_template(self, template_path: str) -> Template:
        """Load Jinja2 template from file."""
        base_dir = Path(__file__).parent.parent.parent
        full_path = base_dir / template_path
        
        if full_path.exists():
            template_content = full_path.read_text(encoding="utf-8")
            return Template(template_content)
        
        # Fallback to default template
        return Template(self._default_template())
    
    def _default_template(self) -> str:
        """Return a minimal default template."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        html, body { height: 100%; margin: 0; }
        #markmap { width: 100%; height: 100vh; }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
    <script src="https://cdn.jsdelivr.net/npm/markmap-lib@0.16.0/dist/browser/index.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/markmap-view@0.16.0/dist/browser/index.js"></script>
</head>
<body>
    <svg id="markmap"></svg>
    <script>
        const markdownContent = `{{ markdown_content | safe }}`;
        const { Markmap, Transformer } = markmap;
        const transformer = new Transformer();
        const { root } = transformer.transform(markdownContent);
        Markmap.create('#markmap', { autoFit: true }, root);
    </script>
</body>
</html>"""
    
    def convert(
        self,
        markdown_content: str,
        title: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """
        Convert Markdown to HTML.
        
        Args:
            markdown_content: Markdown content for the Markmap
            title: Optional title for the HTML page
            metadata: Additional metadata to include
            
        Returns:
            HTML string
        """
        # Escape backticks and backslashes in markdown for JS template literal
        escaped_content = markdown_content.replace("\\", "\\\\").replace("`", "\\`")
        
        # Prepare template variables
        template_vars = {
            "title": title or self.default_title,
            "markdown_content": escaped_content,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "AI Markmap Agent",
            **(metadata or {}),
        }
        
        return self.template.render(**template_vars)
    
    def save(
        self,
        markdown_content: str,
        output_name: str,
        title: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> tuple[Path, Path]:
        """
        Save both Markdown and HTML files.
        
        Args:
            markdown_content: Markdown content
            output_name: Base name for output files (without extension)
            title: Optional title
            metadata: Additional metadata
            
        Returns:
            Tuple of (md_path, html_path)
        """
        # Save Markdown
        md_path = self.md_output_dir / f"{output_name}.md"
        md_path.write_text(markdown_content, encoding="utf-8")
        
        # Convert and save HTML
        html_content = self.convert(markdown_content, title, metadata)
        html_path = self.html_output_dir / f"{output_name}.html"
        html_path.write_text(html_content, encoding="utf-8")
        
        return md_path, html_path
    
    def save_all_outputs(
        self,
        results: dict[str, str],
        naming_config: dict[str, Any] | None = None,
    ) -> dict[str, dict[str, Path]]:
        """
        Save all 4 final outputs based on configuration.
        
        Args:
            results: Dictionary with keys like "general_en", "specialist_zh-TW"
                    mapping to markdown content
            naming_config: Optional naming configuration override
            
        Returns:
            Dictionary mapping output type to {md: path, html: path}
        """
        naming = naming_config or self.config.get("output", {}).get("naming", {})
        prefix = naming.get("prefix", "neetcode")
        
        saved_files = {}
        
        for output_key, content in results.items():
            # Parse output key (e.g., "general_en" or "specialist_zh-TW")
            parts = output_key.split("_", 1)
            if len(parts) == 2:
                output_type, lang = parts
            else:
                output_type = parts[0]
                lang = "en"
            
            # Generate filename
            filename = f"{prefix}_{output_type}_ai_{lang}"
            
            # Generate title
            type_label = "通才版" if output_type == "general" else "專才版"
            if lang == "en":
                type_label = "General" if output_type == "general" else "Specialist"
            title = f"NeetCode {type_label} Mindmap"
            
            # Save files
            md_path, html_path = self.save(
                markdown_content=content,
                output_name=filename,
                title=title,
                metadata={"type": output_type, "language": lang},
            )
            
            saved_files[output_key] = {
                "md": md_path,
                "html": html_path,
            }
            
            print(f"  ✓ Saved: {filename}.md, {filename}.html")
        
        return saved_files


def convert_to_html(
    markdown_content: str,
    title: str | None = None,
    config: dict[str, Any] | None = None,
) -> str:
    """
    Convert Markdown to HTML.
    
    Convenience function.
    
    Args:
        markdown_content: Markdown content
        title: Optional title
        config: Optional configuration
        
    Returns:
        HTML string
    """
    converter = MarkMapHTMLConverter(config)
    return converter.convert(markdown_content, title)


def save_all_markmaps(
    results: dict[str, str],
    config: dict[str, Any] | None = None,
) -> dict[str, dict[str, Path]]:
    """
    Save all final Markmap outputs.
    
    Convenience function.
    
    Args:
        results: Dictionary of output_key -> markdown_content
        config: Optional configuration
        
    Returns:
        Dictionary of saved file paths
    """
    converter = MarkMapHTMLConverter(config)
    return converter.save_all_outputs(results)

