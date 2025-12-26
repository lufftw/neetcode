#!/usr/bin/env python3
"""
Script to rename all .md files (except README variants) to kebab-case.
Creates a mapping and performs the renames with git mv.
Also updates all references to renamed files.
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

def to_kebab_case(filename: str) -> str:
    """Convert filename to kebab-case."""
    # Remove .md extension
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    
    # Replace underscores and spaces with hyphens
    name = re.sub(r'[_\s]+', '-', name)
    
    # Convert CamelCase to kebab-case
    # Insert hyphen before uppercase letters (but not at start)
    name = re.sub(r'(?<!^)(?<!-)([A-Z])', r'-\1', name)
    
    # Convert to lowercase
    name = name.lower()
    
    # Remove multiple consecutive hyphens
    name = re.sub(r'-+', '-', name)
    
    # Remove leading/trailing hyphens
    name = name.strip('-')
    
    # Reattach extension
    return f"{name}.{ext}" if ext else name

def get_all_md_files() -> list[str]:
    """Get all .md files tracked by git, excluding README variants."""
    result = subprocess.run(
        ['git', 'ls-files', '*.md'],
        capture_output=True,
        text=True,
        check=True
    )
    
    files = result.stdout.strip().split('\n')
    # Filter out README variants
    files = [f for f in files if f and not any(
        f.endswith(rm) for rm in ['README.md', 'README_zh-TW.md']
    )]
    
    return files

def create_rename_mapping() -> Dict[str, str]:
    """Create mapping of old filename -> new kebab-case filename."""
    files = get_all_md_files()
    mapping = {}
    
    for filepath in files:
        path = Path(filepath)
        old_name = path.name
        new_name = to_kebab_case(old_name)
        
        # Only add to mapping if name actually changes
        if old_name != new_name:
            new_path = path.parent / new_name
            mapping[filepath] = str(new_path)
    
    return mapping

def main():
    """Main execution."""
    dry_run = '--dry-run' in sys.argv
    
    print("🔍 Step 1: Creating rename mapping...")
    mapping = create_rename_mapping()
    
    if not mapping:
        print("✅ No files need renaming (all already in kebab-case)")
        return
    
    print(f"\n📋 Found {len(mapping)} files to rename:\n")
    for old, new in sorted(mapping.items()):
        print(f"  {old}")
        print(f"  → {new}\n")
    
    # Save mapping to file for reference
    with open('rename_mapping.txt', 'w', encoding='utf-8') as f:
        for old, new in sorted(mapping.items()):
            f.write(f"{old}\t{new}\n")
    print(f"💾 Mapping saved to rename_mapping.txt\n")
    
    if dry_run:
        print("🔍 DRY RUN MODE - No files will be renamed")
        print("   Run without --dry-run to perform actual renames")
        return
    
    # Ask for confirmation (in automated mode, we'll proceed)
    print("🚀 Proceeding with renames using git mv...\n")
    
    # Perform renames
    for old_path, new_path in sorted(mapping.items()):
        try:
            subprocess.run(
                ['git', 'mv', old_path, new_path],
                check=True,
                capture_output=True
            )
            print(f"✅ Renamed: {old_path} → {new_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error renaming {old_path}: {e.stderr.decode()}")
            sys.exit(1)
    
    print(f"\n✅ Successfully renamed {len(mapping)} files!")
    
    # Step 2: Update references
    print("\n🔍 Step 2: Searching for references to old filenames...")
    update_references(mapping)
    
    print("\n✅ Migration complete!")
    print("\n📝 Verification steps:")
    print("   1. Run: git status (to see all changes)")
    print("   2. Run: mkdocs build (to verify documentation build)")
    print("   3. Search for old filenames: git grep <old-filename>")

def update_references(mapping: Dict[str, str]):
    """Update all references to renamed files."""
    # Create reverse mapping: old filename -> new filename (just the basename)
    filename_mapping = {}
    for old_path, new_path in mapping.items():
        old_name = Path(old_path).name
        new_name = Path(new_path).name
        filename_mapping[old_name] = new_name
        # Also map the full relative path
        filename_mapping[old_path] = new_path
    
    # Find all files that might reference the old names
    # Search in: .md, .yml, .yaml, .py, .txt, .json files
    search_extensions = ['.md', '.yml', '.yaml', '.py', '.txt', '.json']
    
    files_to_check = []
    for ext in search_extensions:
        result = subprocess.run(
            ['git', 'ls-files', f'*{ext}'],
            capture_output=True,
            text=True,
            check=True
        )
        files_to_check.extend(result.stdout.strip().split('\n'))
    
    files_to_check = [f for f in files_to_check if f]
    
    updated_count = 0
    for filepath in files_to_check:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            # Replace all occurrences of old filenames
            for old_name, new_name in filename_mapping.items():
                # Replace as full path
                content = content.replace(old_name, new_name)
                # Also replace just the filename in various contexts
                # Markdown links: [text](path/to/file.md)
                content = re.sub(
                    rf'(\[.*?\]\(.*?/){re.escape(old_name)}(\))',
                    rf'\1{new_name}\2',
                    content
                )
                # Direct references in text
                content = re.sub(
                    rf'(["\'])(.*?/)?{re.escape(old_name)}\1',
                    rf'\1\2{new_name}\1',
                    content
                )
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_count += 1
                print(f"  ✅ Updated references in: {filepath}")
        except Exception as e:
            print(f"  ⚠️  Warning: Could not process {filepath}: {e}")
    
    print(f"\n  📝 Updated references in {updated_count} files")

if __name__ == '__main__':
    main()

