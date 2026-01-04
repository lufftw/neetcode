# =============================================================================
# HTML Converter - Wrapper for Standalone Tool
# =============================================================================
# This module provides a compatibility layer that calls the standalone
# convert_to_html.py tool. The standalone tool is the single source of truth
# for HTML conversion functionality.
# =============================================================================

from __future__ import annotations

from pathlib import Path
from typing import Any


# Keep a minimal MarkMapHTMLConverter class for versioning support
# (used by load_baseline_markmap and handle_versioning_mode)
class MarkMapHTMLConverter:
    """
    Minimal wrapper for versioning support.
    
    The actual HTML conversion is handled by the standalone convert_to_html.py tool.
    This class only provides versioning-related methods.
    """
    
    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize with config (only for versioning support)."""
        from ..config_loader import ConfigLoader
        self.config = config or ConfigLoader.get_config()
        output_config = self.config.get("output", {})
        versioning = output_config.get("versioning", {})
        base_dir = Path(__file__).parent.parent.parent
        self.version_dir = (base_dir / versioning.get("directory", "outputs/versions")).resolve()
        self.versioning_enabled = versioning.get("enabled", False)
        self.versioning_mode = versioning.get("mode", "continue")
        self.prompt_on_reset = versioning.get("prompt_on_reset", True)
    
    def _get_existing_versions(self) -> list[Path]:
        """Get list of existing version directories, sorted by version number."""
        if not self.version_dir.exists():
            return []
        
        return sorted(
            [d for d in self.version_dir.iterdir() if d.is_dir() and d.name.startswith("v") and d.name[1:].isdigit()],
            key=lambda x: int(x.name[1:])
        )
    
    def _get_latest_version_path(self, lang: str = "en") -> Path | None:
        """
        Get path to the latest version's markdown file for continue mode.
        
        Args:
            lang: Language code (e.g., "en", "zh-TW")
            
        Returns:
            Path to latest version file, or None if no versions exist
        """
        existing = self._get_existing_versions()
        if not existing:
            return None
        
        latest_dir = existing[-1]
        naming = self.config.get("output", {}).get("naming", {})
        prefix = naming.get("prefix", "neetcode")
        template = naming.get("template", "{prefix}-ontology-agent-evolved-{lang}")
        lang_for_filename = lang.lower() if lang else "en"
        filename = template.format(prefix=prefix, lang=lang_for_filename) + ".md"
        
        latest_file = latest_dir / filename
        if latest_file.exists():
            return latest_file
        
        return None
    
    def handle_reset_mode(self) -> bool:
        """
        Handle reset mode: prompt user for confirmation.
        
        Returns:
            True if reset confirmed (or no versions exist), False if user cancelled
        """
        existing = self._get_existing_versions()
        
        if not existing:
            print("  No existing versions found. Will start fresh with v1.")
            return True
        
        version_names = [d.name for d in existing]
        
        print("\n" + "=" * 60)
        print("🔄 Reset Mode")
        print("=" * 60)
        print(f"\n  Found {len(existing)} existing version(s): {', '.join(version_names)}")
        print("\n  Old versions will be replaced with v1 after pipeline completes.")
        print("  (If pipeline fails, old versions are preserved)")
        
        if self.prompt_on_reset:
            print("\n  Continue with reset? [Y/N]: ", end="")
            try:
                response = input().strip().upper()
            except (EOFError, KeyboardInterrupt):
                print("\n  Cancelled.")
                return False
            
            if response != "Y":
                print("\n  Reset cancelled. Exiting without changes.")
                return False
        
        print(f"\n  ✓ Reset confirmed. Will output as v1 when complete.")
        return True


def save_all_markmaps(
    results: dict[str, str],
    config: dict[str, Any] | None = None,
) -> dict[str, dict[str, Path]]:
    """
    Save all final Markmap outputs using the standalone convert_to_html.py tool.
    
    This function calls the standalone tool programmatically, maintaining
    decoupling while allowing integration.
    
    Args:
        results: Dictionary of output_key -> markdown_content
        config: Optional configuration
        
    Returns:
        Dictionary of saved file paths
    """
    # Import the standalone converter
    base_dir = Path(__file__).parent.parent.parent
    standalone_path = base_dir / "convert_to_html.py"
    
    if not standalone_path.exists():
        raise FileNotFoundError(
            f"Standalone converter not found: {standalone_path}\n"
            "Please ensure convert_to_html.py exists in the ai-markmap-agent directory."
        )
    
    # Import the standalone converter module
    import importlib.util
    spec = importlib.util.spec_from_file_location("convert_to_html", standalone_path)
    convert_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(convert_module)
    convert_file_to_html = convert_module.convert_file_to_html
    
    # Get output directories from config
    from ..config_loader import ConfigLoader
    config = config or ConfigLoader.get_config()
    output_config = config.get("output", {})
    final_dirs = output_config.get("final_dirs", {})
    # Use project root as base_dir (consistent with graph.py)
    base_dir = Path(__file__).parent.parent.parent.parent
    md_output_dir = (base_dir / final_dirs.get("markdown", "outputs/final")).resolve()
    html_output_dir = (base_dir / final_dirs.get("html", "outputs/final")).resolve()
    
    md_output_dir.mkdir(parents=True, exist_ok=True)
    html_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get naming configuration
    naming = output_config.get("naming", {})
    prefix = naming.get("prefix", "neetcode")
    template = naming.get("template", "{prefix}-ontology-agent-evolved-{lang}")
    
    # Get template path from config
    html_config = output_config.get("html", {})
    template_path = html_config.get("template", "templates/markmap.html")
    
    saved_files = {}
    
    # Process each output
    for output_key, content in results.items():
        # Parse output key (e.g., "general_en" or "specialist_zh-TW")
        parts = output_key.rsplit("_", 1)
        if len(parts) == 2:
            output_type, lang = parts
        else:
            output_type = parts[0]
            lang = "en"
        
        # Generate filename (use lowercase language code for filename)
        lang_for_filename = lang.lower() if lang else "en"
        filename = template.format(prefix=prefix, lang=lang_for_filename)
        
        # Generate title (keep original language code format for display)
        title = f"NeetCode Agent Evolved Mindmap ({lang.upper()})"
        
        # Save markdown first
        md_path = md_output_dir / f"{filename}.md"
        md_path.write_text(content, encoding="utf-8")
        
        # Convert to HTML using standalone tool
        html_path = html_output_dir / f"{filename}.html"
        convert_file_to_html(
            input_path=md_path,
            output_path=html_path,
            title=title,
            template_path=template_path,
        )
        
        saved_files[output_key] = {
            "md": md_path,
            "html": html_path,
        }
        
        print(f"  ✓ Saved: {filename}.md, {filename}.html")
        
        # Handle versioning if enabled
        versioning = output_config.get("versioning", {})
        if versioning.get("enabled", False):
            version_dir = (base_dir / versioning.get("directory", "outputs/versions")).resolve()
            
            # Determine version name
            if versioning.get("mode", "continue") == "reset":
                # Clean up old versions first
                converter = MarkMapHTMLConverter(config)
                existing = converter._get_existing_versions()
                for version_dir_old in existing:
                    import shutil
                    shutil.rmtree(version_dir_old)
                    print(f"  🗑️ Deleted old: {version_dir_old.name}")
                version_name = "v1"
            else:
                # Get next version
                converter = MarkMapHTMLConverter(config)
                existing = converter._get_existing_versions()
                if not existing:
                    version_name = "v1"
                else:
                    last_num = int(existing[-1].name[1:])
                    version_name = f"v{last_num + 1}"
            
            version_subdir = version_dir / version_name
            version_subdir.mkdir(parents=True, exist_ok=True)
            
            # Save to version directory
            version_md = version_subdir / f"{filename}.md"
            version_html = version_subdir / f"{filename}.html"
            version_md.write_text(content, encoding="utf-8")
            convert_file_to_html(
                input_path=version_md,
                output_path=version_html,
                title=title,
                template_path=template_path,
            )
            print(f"  📦 Versioned: {version_subdir.name}/{filename}.*")
    
    return saved_files


def convert_to_html(
    markdown_content: str,
    title: str | None = None,
    config: dict[str, Any] | None = None,
) -> str:
    """
    Convert Markdown to HTML using the standalone tool.
    
    Convenience function.
    
    Args:
        markdown_content: Markdown content
        title: Optional title
        config: Optional configuration
        
    Returns:
        HTML string
    """
    import tempfile
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp:
        tmp.write(markdown_content)
        tmp_path = Path(tmp.name)
    
    try:
        # Import standalone converter
        base_dir = Path(__file__).parent.parent.parent
        standalone_path = base_dir / "convert_to_html.py"
        
        if not standalone_path.exists():
            raise FileNotFoundError(f"Standalone converter not found: {standalone_path}")
        
        import importlib.util
        spec = importlib.util.spec_from_file_location("convert_to_html", standalone_path)
        convert_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(convert_module)
        StandaloneHTMLConverter = convert_module.StandaloneHTMLConverter
        
        # Get template path from config
        from ..config_loader import ConfigLoader
        config = config or ConfigLoader.get_config()
        html_config = config.get("output", {}).get("html", {})
        template_path = html_config.get("template", "templates/markmap.html")
        
        # Convert
        converter = StandaloneHTMLConverter(template_path=template_path)
        html_content = converter.convert(markdown_content, title=title)
        
        return html_content
    finally:
        # Clean up temp file
        if tmp_path.exists():
            tmp_path.unlink()
