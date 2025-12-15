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
    ) -> str:
        """
        Convert Markdown to HTML.
        
        Args:
            markdown_content: Markdown content for the Markmap
            title: Optional title for the HTML page
            
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
        
        # Prepare template variables
        template_vars = {
            "title": title or "AI Generated Markmap",
            "markdown_content": escaped_content,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        return self.template.render(**template_vars)


def convert_file_to_html(
    input_path: str | Path,
    output_path: str | Path | None = None,
    title: str | None = None,
    template_path: str | Path | None = None,
) -> Path:
    """
    Convert a Markdown file to HTML (programmatic interface).
    
    Args:
        input_path: Path to input Markdown file (can be relative or absolute)
        output_path: Path to output HTML file (default: same as input with .html)
        title: Optional HTML page title
        template_path: Optional custom template path
        
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
    
    markdown_content = input_path.read_text(encoding="utf-8")
    converter = StandaloneHTMLConverter(template_path=template_path)
    html_content = converter.convert(markdown_content, title=title)
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
        help="Input Markdown file path"
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
    
    args = parser.parse_args()
    
    try:
        # Get script base directory for resolving relative paths (CLI tool behavior)
        script_base_dir = Path(__file__).parent
        
        # Resolve input path
        # Relative paths are resolved relative to script directory, not current working directory
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
        else:
            # Derive title from filename
            title = f"{input_path.stem.replace('_', ' ').title()} - NeetCode Mind Maps"
        
        # Read markdown content
        print(f"📖 Reading: {input_path}")
        markdown_content = input_path.read_text(encoding="utf-8")
        print(f"   ✓ Loaded {len(markdown_content)} characters")
        
        # Create converter
        print(f"🔧 Initializing converter...")
        converter = StandaloneHTMLConverter(template_path=args.template)
        
        # Convert to HTML
        print(f"🔄 Converting to HTML...")
        html_content = converter.convert(markdown_content, title=title)
        
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
