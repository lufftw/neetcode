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
        
        # Versioning
        versioning = output_config.get("versioning", {})
        self.versioning_enabled = versioning.get("enabled", False)
        self.version_dir = (base_dir / versioning.get("directory", "outputs/versions")).resolve()
        
        # Ensure directories exist
        self.md_output_dir.mkdir(parents=True, exist_ok=True)
        self.html_output_dir.mkdir(parents=True, exist_ok=True)
        if self.versioning_enabled:
            self.version_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_template(self, template_path: str) -> Template:
        """Load Jinja2 template from file."""
        base_dir = Path(__file__).parent.parent.parent
        full_path = base_dir / template_path
        
        if full_path.exists():
            template_content = full_path.read_text(encoding="utf-8")
            return Template(template_content)
        
        # Fallback to default template
        return Template(self._default_template())
    
    def _get_next_version(self) -> str:
        """Get next version number (v1, v2, ...)."""
        if not self.version_dir.exists():
            return "v1"
        
        existing = sorted(
            [d for d in self.version_dir.iterdir() if d.is_dir() and d.name.startswith("v")],
            key=lambda x: int(x.name[1:]) if x.name[1:].isdigit() else 0
        )
        
        if not existing:
            return "v1"
        
        last_num = int(existing[-1].name[1:])
        return f"v{last_num + 1}"
    
    def _default_template(self) -> str:
        """Return a minimal default template matching the main template format."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - NeetCode Mind Maps</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body { height: 100%; }
        .markmap { width: 100%; height: 100%; }
        .markmap > svg { width: 100%; height: 100%; }
        #topbar {
            position: fixed; top: 0; left: 0; right: 0; z-index: 100;
            background: #fff; border-bottom: 1px solid #e5e7eb;
            padding: 8px 16px; display: flex; gap: 8px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size: 13px;
        }
        #topbar button {
            padding: 4px 12px; border: 1px solid #d1d5db;
            border-radius: 4px; background: #fff; cursor: pointer;
        }
        #topbar button:hover { background: #f3f4f6; }
        .markmap { margin-top: 40px; height: calc(100% - 40px); }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
    <script src="https://cdn.jsdelivr.net/npm/markmap-view"></script>
    <script src="https://cdn.jsdelivr.net/npm/markmap-lib"></script>
    <script src="https://cdn.jsdelivr.net/npm/markmap-toolbar"></script>
    <script>
        function fitView() {
            var svg = document.querySelector('.markmap > svg');
            if (svg && svg.mm) svg.mm.fit();
        }
        function expandAll() {
            var svg = document.querySelector('.markmap > svg');
            if (svg && svg.mm) {
                var root = svg.mm.state.data;
                (function expand(n) {
                    n.payload = Object.assign({}, n.payload, { fold: 0 });
                    if (n.children) n.children.forEach(expand);
                })(root);
                svg.mm.setData(root); svg.mm.fit();
            }
        }
        function collapseAll() {
            var svg = document.querySelector('.markmap > svg');
            if (svg && svg.mm) {
                var root = svg.mm.state.data;
                root.children && root.children.forEach(function collapse(n) {
                    if (n.children && n.children.length) {
                        n.payload = Object.assign({}, n.payload, { fold: 1 });
                        n.children.forEach(collapse);
                    }
                });
                svg.mm.setData(root); svg.mm.fit();
            }
        }
        document.addEventListener('DOMContentLoaded', function() {
            const { Transformer, Markmap } = window.markmap;
            const transformer = new Transformer();
            const markdown = `{{ markdown_content | safe }}`;
            const { root } = transformer.transform(markdown);
            const svg = d3.select('.markmap').append('svg');
            const mm = Markmap.create(svg.node(), { color: (node) => node.payload?.color || '#f59e0b' }, root);
            svg.node().mm = mm;
            if (window.markmap && window.markmap.Toolbar) {
                const toolbar = new window.markmap.Toolbar();
                toolbar.attach(mm);
                setTimeout(function() {
                    document.querySelectorAll('.mm-toolbar').forEach(function(toolbar) {
                        toolbar.querySelectorAll('.mm-toolbar-item').forEach(function(item) {
                            if ((item.title || '').toLowerCase().includes('dark')) item.remove();
                        });
                        var brand = toolbar.querySelector('.mm-toolbar-brand');
                        if (brand) {
                            brand.innerHTML = '🟡 NeetCode';
                            brand.href = '#'; brand.onclick = function(e) { e.preventDefault(); };
                            brand.style.fontSize = '12px'; brand.style.color = '#666';
                        }
                    });
                }, 200);
            }
        });
    </script>
</head>
<body>
    <div id="topbar">
        <button onclick="fitView()">Fit View</button>
        <button onclick="expandAll()">Expand All</button>
        <button onclick="collapseAll()">Collapse All</button>
    </div>
    <div class="markmap"></div>
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
        Save all final outputs based on configuration.
        
        Args:
            results: Dictionary with keys like "general_en", "specialist_zh-TW"
                    mapping to markdown content
            naming_config: Optional naming configuration override
            
        Returns:
            Dictionary mapping output type to {md: path, html: path}
        """
        naming = naming_config or self.config.get("output", {}).get("naming", {})
        prefix = naming.get("prefix", "neetcode")
        template = naming.get("template", "{prefix}_ontology_agent_evolved_{lang}")
        
        saved_files = {}
        
        # Get version directory if versioning is enabled
        version_subdir = None
        if self.versioning_enabled:
            version_name = self._get_next_version()
            version_subdir = self.version_dir / version_name
            version_subdir.mkdir(parents=True, exist_ok=True)
            print(f"  📁 Version: {version_name}")
        
        for output_key, content in results.items():
            # Parse output key (e.g., "general_en" or "specialist_zh-TW")
            # Use rsplit to handle language codes that might contain underscores
            parts = output_key.rsplit("_", 1)
            if len(parts) == 2:
                output_type, lang = parts
            else:
                output_type = parts[0]
                lang = "en"
            
            # Generate filename from template
            filename = template.format(prefix=prefix, lang=lang)
            
            # Generate title
            title = f"NeetCode Agent Evolved Mindmap ({lang.upper()})"
            
            # Save to final directories
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
            
            # Also save to version directory
            if version_subdir:
                version_md = version_subdir / f"{filename}.md"
                version_html = version_subdir / f"{filename}.html"
                version_md.write_text(content, encoding="utf-8")
                html_content = self.convert(content, title, {"type": output_type, "language": lang})
                version_html.write_text(html_content, encoding="utf-8")
                print(f"  📦 Versioned: {version_subdir.name}/{filename}.*")
        
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

