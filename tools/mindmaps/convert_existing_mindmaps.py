#!/usr/bin/env python3
"""
Convert existing Markmap files to replace tables with tree structure.

This script processes existing mind map files and converts any Markdown tables
outside of code blocks into Markmap tree structures.
"""

import sys
from pathlib import Path

# Add tools directory to path
TOOLS_DIR = Path(__file__).parent
sys.path.insert(0, str(TOOLS_DIR))

from mindmaps.helpers import convert_tables_in_markmap


def convert_file(file_path: Path, backup: bool = True) -> bool:
    """
    Convert tables in a Markmap file.
    
    Args:
        file_path: Path to the Markmap file
        backup: Whether to create a backup file
        
    Returns:
        True if conversion was successful, False otherwise
    """
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return False
    
    # Read original content
    original_content = file_path.read_text(encoding="utf-8")
    
    # Convert tables
    converted_content = convert_tables_in_markmap(original_content)
    
    # Check if content changed
    if original_content == converted_content:
        print(f"ℹ️  No tables found in: {file_path.name}")
        return True
    
    # Create backup if requested
    if backup:
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")
        backup_path.write_text(original_content, encoding="utf-8")
        print(f"💾 Backup created: {backup_path.name}")
    
    # Write converted content
    file_path.write_text(converted_content, encoding="utf-8")
    print(f"✅ Converted: {file_path.name}")
    return True


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Convert Markdown tables in Markmap files to tree structure"
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Markmap files to convert (default: all .md files in docs/mindmaps/)"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't create backup files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be converted without making changes"
    )
    
    args = parser.parse_args()
    
    # Determine files to process
    if args.files:
        files = [Path(f) for f in args.files]
    else:
        # Default: all .md files in docs/mindmaps/
        docs_dir = Path(__file__).parent.parent / "docs" / "mindmaps"
        if docs_dir.exists():
            files = list(docs_dir.glob("*.md"))
        else:
            print(f"❌ Directory not found: {docs_dir}")
            return 1
    
    if not files:
        print("ℹ️  No files to process")
        return 0
    
    print(f"📋 Processing {len(files)} file(s)...\n")
    
    converted_count = 0
    for file_path in files:
        if args.dry_run:
            # Just check if conversion would change anything
            original_content = file_path.read_text(encoding="utf-8")
            converted_content = convert_tables_in_markmap(original_content)
            if original_content != converted_content:
                print(f"🔍 Would convert: {file_path.name}")
                converted_count += 1
            else:
                print(f"ℹ️  No changes needed: {file_path.name}")
        else:
            if convert_file(file_path, backup=not args.no_backup):
                converted_count += 1
            print()
    
    if args.dry_run:
        print(f"\n📊 Summary: {converted_count} file(s) would be converted")
    else:
        print(f"\n📊 Summary: {converted_count} file(s) converted")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

