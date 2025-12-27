#!/usr/bin/env python3
# =============================================================================
# Standalone Markdown to HTML Converter
# =============================================================================
# Convert Markmap Markdown files to interactive HTML files.
#
# Usage:
#   python convert_to_html.py input.md                    # Convert to input.html
#   python convert_to_html.py input.md -o output.html     # Specify output file
#   python convert_to_html.py input.md -t "My Title"      # Custom title
#   python convert_to_html.py input.md --template custom.html  # Custom template
#
# This tool is independent of the main AI Markmap Agent pipeline.
# =============================================================================

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Template

# Try to import TOML parser (simple fallback if not available)
try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # Fallback for older Python
    except ImportError:
        tomllib = None


class StandaloneHTMLConverter:
    """
    Standalone converter that doesn't depend on the main package structure.
    """
    
    def __init__(self, template_path: str | Path | None = None):
        """
        Initialize the converter.
        
        Args:
            template_path: Path to HTML template (optional, defaults to templates/markmap.html)
        """
        self.base_dir = Path(__file__).parent
        
        # Load template
        if template_path:
            template_path = Path(template_path)
            if not template_path.is_absolute():
                template_path = self.base_dir / template_path
        else:
            template_path = self.base_dir / "templates" / "markmap.html"
        
        if not template_path.exists():
            raise FileNotFoundError(
                f"Template file not found: {template_path}\n"
                "Please ensure templates/markmap.html exists or specify a custom template path."
            )
        
        self.template = Template(template_path.read_text(encoding="utf-8"))
    
    def convert(
        self,
        markdown_content: str,
        title: str | None = None,
        description: str | None = None,
    ) -> str:
        """
        Convert Markdown to HTML.
        
        Args:
            markdown_content: Markdown content for the Markmap
            title: Optional title for the HTML page
            description: Optional meta description for SEO
            
        Returns:
            HTML string
        """
        # Escape special characters for JavaScript template literal
        # Order matters: escape backslash first, then backtick, then ${ to prevent template expression interpretation
        escaped_content = (
            markdown_content
            .replace("\\", "\\\\")  # Escape backslashes first
            .replace("`", "\\`")     # Escape backticks
            .replace("${", "\\${")   # Escape ${ to prevent template expression interpretation
        )
        
        # Escape description for HTML (escape quotes)
        description_escaped = None
        if description:
            description_escaped = description.replace('"', '&quot;').replace("'", "&#39;")
        
        # Prepare template variables
        template_vars = {
            "title": title or "AI Generated Markmap",
            "markdown_content": escaped_content,
            "description": description_escaped,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        return self.template.render(**template_vars)


def load_config(config_path: Path | None = None) -> dict[str, Any]:
    """Load configuration from TOML file.
    
    Args:
        config_path: Path to config file (default: convert_to_html.toml in script directory)
        
    Returns:
        Configuration dict
    """
    if config_path is None:
        config_path = Path(__file__).parent / "convert_to_html.toml"
    
    if not config_path.exists():
        return {}
    
    if tomllib is None:
        print("⚠️  Warning: TOML parser not available. Install 'tomli' for Python < 3.11: pip install tomli")
        return {}
    
    try:
        with open(config_path, "rb") as f:
            return tomllib.load(f)
    except Exception as e:
        print(f"⚠️  Warning: Failed to load config: {e}")
        return {}


def load_meta_description(
    meta_description_file: str,
    config: dict[str, Any],
    project_root: Path | None = None,
) -> str | None:
    """Load meta description file from meta_descriptions_dir.
    
    Args:
        meta_description_file: Meta description filename (e.g., "neetcode_ontology_agent_evolved_en.txt")
        config: Configuration dict (for meta_descriptions_dir setting)
        project_root: Project root path (default: assumes script is in tools/ai-markmap-agent/)
        
    Returns:
        Meta description string, or None if not found
    """
    if project_root is None:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent.parent
    
    # Build path: meta_descriptions_dir / filename
    meta_dir_str = config.get("meta_descriptions_dir", "tools/mindmaps/meta")
    meta_dir = project_root / meta_dir_str if not Path(meta_dir_str).is_absolute() else Path(meta_dir_str)
    
    desc_path = meta_dir / meta_description_file
    if desc_path.exists():
        try:
            return desc_path.read_text(encoding="utf-8").strip()
        except Exception as e:
            print(f"   ⚠️  Failed to read meta description: {e}")
    else:
        print(f"   ⚠️  Meta description file not found: {desc_path}")
    
    return None


def convert_file_to_html(
    input_path: str | Path,
    output_path: str | Path | None = None,
    title: str | None = None,
    template_path: str | Path | None = None,
    description: str | None = None,
    config: dict[str, Any] | None = None,
) -> Path:
    """
    Convert a Markdown file to HTML (programmatic interface).
    
    Args:
        input_path: Path to input Markdown file (can be relative or absolute)
        output_path: Path to output HTML file (default: same as input with .html)
        title: Optional HTML page title
        template_path: Optional custom template path
        description: Optional meta description (if None and config provided, will auto-load)
        config: Optional configuration dict (used for auto-loading meta description)
        
    Returns:
        Path to the generated HTML file
        
    This function can be imported and used programmatically.
    """
    # Resolve input path (handles both absolute and relative paths)
    input_path = Path(input_path)
    if not input_path.is_absolute():
        # If relative, resolve relative to current working directory
        # (This is correct for programmatic calls where paths are already resolved)
        input_path = input_path.resolve()
    else:
        input_path = input_path.resolve()
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if output_path is None:
        output_path = input_path.with_suffix(".html")
    else:
        output_path = Path(output_path)
        if not output_path.is_absolute():
            output_path = output_path.resolve()
        else:
            output_path = output_path.resolve()
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if title is None:
        title = f"{input_path.stem.replace('_', ' ').title()} - NeetCode Mind Maps"
    
    # Load meta description if not provided and config is available
    if description is None and config:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent.parent
        description = load_meta_description(input_path.name, config, project_root)
    
    markdown_content = input_path.read_text(encoding="utf-8")
    
    # Remove markdown code fence if present (LLM sometimes wraps output)
    markdown_content = markdown_content.strip()
    if markdown_content.startswith("```markdown"):
        markdown_content = markdown_content[len("```markdown"):].strip()
    if markdown_content.startswith("```md"):
        markdown_content = markdown_content[len("```md"):].strip()
    if markdown_content.startswith("```"):
        markdown_content = markdown_content[3:].strip()
    if markdown_content.endswith("```"):
        markdown_content = markdown_content[:-3].strip()
    
    converter = StandaloneHTMLConverter(template_path=template_path)
    html_content = converter.convert(markdown_content, title=title, description=description)
    output_path.write_text(html_content, encoding="utf-8")
    
    return output_path


def main() -> int:
    """
    Main entry point for standalone HTML converter.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = argparse.ArgumentParser(
        description="Convert Markmap Markdown files to interactive HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert markdown to HTML (same name, .html extension)
  python convert_to_html.py input.md
  
  # Specify output file
  python convert_to_html.py input.md -o output.html
  
  # Custom title
  python convert_to_html.py input.md -t "My Mind Map"
  
  # Use custom template
  python convert_to_html.py input.md --template templates/custom.html
        """
    )
    
    parser.add_argument(
        "input",
        type=str,
        nargs="?",
        default=None,
        help="Input Markdown file path (optional if using --preset)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output HTML file path (default: same as input with .html extension)"
    )
    parser.add_argument(
        "-t", "--title",
        type=str,
        default=None,
        help="HTML page title (default: derived from input filename)"
    )
    parser.add_argument(
        "--template",
        type=str,
        default=None,
        help="Path to custom HTML template (overrides default)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to configuration file (default: convert_to_html.toml in script directory)"
    )
    parser.add_argument(
        "--preset",
        type=str,
        default=None,
        help="Use a preset from config file (e.g., 'neetcode_ontology_agent_evolved_en')"
    )
    parser.add_argument(
        "--description",
        type=str,
        default=None,
        help="Meta description for HTML (overrides auto-detection from config)"
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List available presets from config file and exit"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all presets from config file"
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config_path = None
        if args.config:
            config_path = Path(args.config)
            if not config_path.is_absolute():
                config_path = (Path(__file__).parent / config_path).resolve()
        
        config = load_config(config_path)
        
        # List presets if requested
        if args.list_presets:
            presets = config.get("presets", {})
            if presets:
                print("Available presets:")
                for preset_name in presets.keys():
                    preset = presets[preset_name]
                    input_file = preset.get("input", "N/A")
                    output_file = preset.get("output", "N/A")
                    title = preset.get("title", "N/A")
                    print(f"  {preset_name}:")
                    print(f"    Input:  {input_file}")
                    print(f"    Output: {output_file}")
                    print(f"    Title:  {title}")
            else:
                print("No presets found in configuration file.")
            return 0
        
        # Process all presets if requested
        if args.all:
            presets = config.get("presets", {})
            if not presets:
                print("❌ Error: No presets found in configuration file.")
                return 1
            
            script_base_dir = Path(__file__).parent
            project_root = script_base_dir.parent.parent
            
            print(f"\n🔄 Processing all {len(presets)} preset(s)...\n")
            
            success_count = 0
            error_count = 0
            
            for preset_name, preset in presets.items():
                print(f"{'='*60}")
                print(f"📋 Processing preset: {preset_name}")
                print(f"{'='*60}")
                
                try:
                    # Resolve paths
                    input_path = Path(preset["input"])
                    if not input_path.is_absolute():
                        input_path = (project_root / input_path).resolve()
                    
                    if not input_path.exists():
                        print(f"   ⚠️  Input file not found: {input_path}")
                        print(f"   ⏭️  Skipping...\n")
                        error_count += 1
                        continue
                    
                    output_path = Path(preset["output"])
                    if not output_path.is_absolute():
                        output_path = (project_root / output_path).resolve()
                    
                    title = preset.get("title", None)
                    
                    # Load meta description
                    description = args.description  # CLI arg overrides
                    if description is None:
                        meta_file = preset.get("meta_description_file")
                        if meta_file:
                            description = load_meta_description(meta_file, config, project_root)
                    
                    # Get template path
                    template_path = None
                    if config.get("template_path"):
                        template_path = Path(config["template_path"])
                        if not template_path.is_absolute():
                            template_path = (script_base_dir / template_path).resolve()
                    
                    print(f"   Input:  {input_path}")
                    print(f"   Output: {output_path}")
                    print(f"   Title:  {title}")
                    if description:
                        print(f"   Meta description: {len(description)} chars")
                    
                    # Convert
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    markdown_content = input_path.read_text(encoding="utf-8")
                    
                    # Remove markdown code fence if present
                    markdown_content = markdown_content.strip()
                    if markdown_content.startswith("```markdown"):
                        markdown_content = markdown_content[len("```markdown"):].strip()
                    if markdown_content.startswith("```md"):
                        markdown_content = markdown_content[len("```md"):].strip()
                    if markdown_content.startswith("```"):
                        markdown_content = markdown_content[3:].strip()
                    if markdown_content.endswith("```"):
                        markdown_content = markdown_content[:-3].strip()
                    
                    converter = StandaloneHTMLConverter(template_path=template_path)
                    html_content = converter.convert(markdown_content, title=title, description=description)
                    output_path.write_text(html_content, encoding="utf-8")
                    
                    print(f"   ✅ Generated: {output_path}\n")
                    success_count += 1
                    
                except Exception as e:
                    print(f"   ❌ Error: {e}\n")
                    error_count += 1
                    continue
            
            # Summary
            print(f"{'='*60}")
            if success_count > 0:
                print(f"✅ Successfully processed {success_count} preset(s)")
            if error_count > 0:
                print(f"❌ Failed to process {error_count} preset(s)")
            print(f"{'='*60}")
            
            return 0 if error_count == 0 else 1
        
        # Handle preset mode
        if args.preset:
            presets = config.get("presets", {})
            if args.preset not in presets:
                print(f"❌ Error: Preset '{args.preset}' not found in configuration.")
                print("   Use --list-presets to see available presets.")
                return 1
            
            preset = presets[args.preset]
            
            # Get script base directory for resolving relative paths
            script_base_dir = Path(__file__).parent
            project_root = script_base_dir.parent.parent
            
            # Resolve preset paths relative to project root
            input_path = Path(preset["input"])
            if not input_path.is_absolute():
                input_path = (project_root / input_path).resolve()
            
            output_path = Path(preset["output"])
            if not output_path.is_absolute():
                output_path = (project_root / output_path).resolve()
            
            title = preset.get("title", None)
            
            # Load meta description: CLI arg > preset file > None
            description = args.description
            if description is None:
                meta_file = preset.get("meta_description_file")
                if meta_file:
                    description = load_meta_description(meta_file, config, project_root)
            
            # Get template path from config or use default
            template_path = None
            if config.get("template_path"):
                template_path = Path(config["template_path"])
                if not template_path.is_absolute():
                    template_path = (script_base_dir / template_path).resolve()
            
            # Convert using preset
            print(f"📋 Using preset: {args.preset}")
            print(f"   Input:  {input_path}")
            print(f"   Output: {output_path}")
            print(f"   Title:  {title}")
            if description:
                print(f"   Meta description: {len(description)} chars")
            else:
                print(f"   Meta description: None (no file found)")
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            markdown_content = input_path.read_text(encoding="utf-8")
            
            # Remove markdown code fence if present
            markdown_content = markdown_content.strip()
            if markdown_content.startswith("```markdown"):
                markdown_content = markdown_content[len("```markdown"):].strip()
            if markdown_content.startswith("```md"):
                markdown_content = markdown_content[len("```md"):].strip()
            if markdown_content.startswith("```"):
                markdown_content = markdown_content[3:].strip()
            if markdown_content.endswith("```"):
                markdown_content = markdown_content[:-3].strip()
            
            converter = StandaloneHTMLConverter(template_path=template_path)
            html_content = converter.convert(markdown_content, title=title, description=description)
            output_path.write_text(html_content, encoding="utf-8")
            
            print(f"\n✅ Success!")
            print(f"   Output: {output_path}")
            return 0
        
        # Check if input is required (not using preset)
        if not args.preset and not args.input:
            print("❌ Error: Input file required when not using --preset")
            print("   Usage: python convert_to_html.py input.md [options]")
            print("   Or use: python convert_to_html.py --preset <preset_name>")
            return 1
        
        # Get script base directory for resolving relative paths (CLI tool behavior)
        script_base_dir = Path(__file__).parent
        
        # Resolve input path (only if not using preset)
        input_path = None
        if args.input:
            input_path = Path(args.input)
            if not input_path.is_absolute():
                input_path = (script_base_dir / input_path).resolve()
            else:
                input_path = input_path.resolve()
            
            if not input_path.exists():
                print(f"❌ Error: Input file not found: {input_path}")
                print(f"   Resolved from: {args.input}")
                print(f"   Script directory: {script_base_dir}")
                return 1
            
            if not input_path.is_file():
                print(f"❌ Error: Input path is not a file: {input_path}")
                return 1
        
        # Determine output path
        if args.output:
            output_path = Path(args.output)
            # Resolve relative paths relative to script directory (CLI tool behavior)
            if not output_path.is_absolute():
                output_path = (script_base_dir / output_path).resolve()
            else:
                output_path = output_path.resolve()
        else:
            output_path = input_path.with_suffix(".html")
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Determine title
        if args.title:
            title = args.title
        elif input_path:
            # Derive title from filename
            title = f"{input_path.stem.replace('_', ' ').title()} - NeetCode Mind Maps"
        else:
            title = "AI Generated Markmap - NeetCode Mind Maps"
        
        # Read markdown content
        if input_path:
            print(f"📖 Reading: {input_path}")
            markdown_content = input_path.read_text(encoding="utf-8")
            print(f"   ✓ Loaded {len(markdown_content)} characters")
            
            # Load meta description
            description = args.description
            if description is None and config:
                project_root = script_base_dir.parent.parent
                description = load_meta_description(input_path.name, config, project_root)
        else:
            print("❌ Error: No input file specified")
            return 1
            if description:
                print(f"   📝 Loaded meta description ({len(description)} chars)")
        
        # Get template path
        template_path = args.template
        if template_path is None and config.get("template_path"):
            template_path = config["template_path"]
            if not Path(template_path).is_absolute():
                template_path = script_base_dir / template_path
        
        # Create converter
        print(f"🔧 Initializing converter...")
        converter = StandaloneHTMLConverter(template_path=template_path)
        
        # Convert to HTML
        print(f"🔄 Converting to HTML...")
        html_content = converter.convert(markdown_content, title=title, description=description)
        
        # Save HTML
        print(f"💾 Saving: {output_path}")
        output_path.write_text(html_content, encoding="utf-8")
        
        # Report success
        print(f"\n✅ Success!")
        print(f"   Input:  {input_path}")
        print(f"   Output: {output_path}")
        print(f"   Title:  {title}")
        print(f"   Size:   {len(html_content)} characters")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: File not found: {e}")
        return 1
    except PermissionError as e:
        print(f"\n❌ Error: Permission denied: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
