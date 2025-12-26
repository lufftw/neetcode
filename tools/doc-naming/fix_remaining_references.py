#!/usr/bin/env python3
"""
Fix remaining old filename references after kebab-case migration.

This script performs comprehensive replacement of old filenames in all file types,
handling various reference formats that the main renaming script might have missed.
"""

import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Set


def load_mapping() -> Dict[str, str]:
    """Load the rename mapping from JSON file."""
    mapping_file = Path("rename_mapping.json")
    if not mapping_file.exists():
        print(f"ERROR: {mapping_file} not found. Run rename_docs_to_kebab_case.py first.")
        return {}
    
    with open(mapping_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_all_files_to_check() -> List[str]:
    """Get all files that might contain references."""
    extensions = ['.md', '.yml', '.yaml', '.py', '.txt', '.json', '.toml']
    files_to_check = []
    
    for ext in extensions:
        try:
            result = subprocess.run(
                ['git', 'ls-files', f'*{ext}'],
                capture_output=True,
                text=True,
                check=True
            )
            files_to_check.extend(result.stdout.strip().split('\n'))
        except subprocess.CalledProcessError:
            continue
    
    return [f for f in files_to_check if f.strip()]


def fix_references(mapping: Dict[str, str]) -> int:
    """Fix all remaining references to old filenames."""
    print("Loading rename mapping...")
    
    # Build comprehensive replacement mappings
    # Map old filename -> new filename
    filename_mapping = {}
    # Map old full path -> new full path (normalized to forward slashes)
    path_mapping = {}
    # Map old relative paths -> new relative paths
    rel_path_mapping = {}
    
    for old_path, new_path in mapping.items():
        old_path_norm = old_path.replace('\\', '/')
        new_path_norm = new_path.replace('\\', '/')
        
        old_name = Path(old_path_norm).name
        new_name = Path(new_path_norm).name
        
        filename_mapping[old_name] = new_name
        path_mapping[old_path_norm] = new_path_norm
        
        # Build relative path variants
        old_dir = str(Path(old_path_norm).parent).replace('\\', '/')
        new_dir = str(Path(new_path_norm).parent).replace('\\', '/')
        
        if old_dir != '.':
            old_rel = f"{old_dir}/{old_name}"
            new_rel = f"{new_dir}/{new_name}"
            rel_path_mapping[old_rel] = new_rel
            # Also map with backslashes for Windows compatibility
            rel_path_mapping[old_rel.replace('/', '\\')] = new_rel.replace('/', '\\')
    
    print(f"Found {len(filename_mapping)} files to fix references for")
    print(f"\nChecking files for old references...")
    
    files_to_check = get_all_files_to_check()
    updated_count = 0
    updated_files: Set[str] = set()
    
    for filepath in files_to_check:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            file_updated = False
            
            # Strategy 1: Replace full paths (exact match)
            for old_path, new_path in path_mapping.items():
                if old_path in content:
                    content = content.replace(old_path, new_path)
                    file_updated = True
            
            # Strategy 2: Replace relative paths (directory + filename)
            for old_rel, new_rel in rel_path_mapping.items():
                if old_rel in content:
                    content = content.replace(old_rel, new_rel)
                    file_updated = True
            
            # Strategy 3: Replace standalone filenames (most common case)
            # This handles:
            # - YAML: "  - Title: OLD_NAME.md"
            # - Markdown links: "[text](OLD_NAME.md)"
            # - Plain text: "See OLD_NAME.md"
            for old_name, new_name in filename_mapping.items():
                # Use word boundaries to avoid partial matches
                # But be careful with special characters in filenames
                escaped_old = re.escape(old_name)
                
                # Pattern 1: In YAML format (after colon, possibly with spaces)
                # Match: "  - Title: OLD_NAME.md" or "key: OLD_NAME.md"
                yaml_pattern = re.compile(
                    rf'(\s+[-\w\s]+:\s+){escaped_old}(\s|$)',
                    re.MULTILINE
                )
                if yaml_pattern.search(content):
                    content = yaml_pattern.sub(rf'\1{new_name}\2', content)
                    file_updated = True
                
                # Pattern 2: In Markdown links
                # Match: "[text](OLD_NAME.md)" or "[text](path/OLD_NAME.md)"
                link_pattern = re.compile(
                    rf'(\[.*?\]\([^)]*?){escaped_old}(#.*?)?(\))',
                    re.MULTILINE
                )
                if link_pattern.search(content):
                    content = link_pattern.sub(rf'\1{new_name}\2\3', content)
                    file_updated = True
                
                # Pattern 3: In quoted strings (Python, JSON, etc.)
                # Match: '"OLD_NAME.md"' or "'OLD_NAME.md'"
                quoted_pattern = re.compile(
                    rf'(["\'])([^"\']*?){escaped_old}(["\'])',
                    re.MULTILINE
                )
                if quoted_pattern.search(content):
                    content = quoted_pattern.sub(rf'\1\2{new_name}\3', content)
                    file_updated = True
                
                # Pattern 4: Standalone in text (with word boundaries)
                # Match: "See OLD_NAME.md" or "OLD_NAME.md is..."
                # Use word boundary but allow for common separators
                standalone_pattern = re.compile(
                    rf'([\s\(\[\'"]){escaped_old}([\s\)\]\'".,;:!?])',
                    re.MULTILINE
                )
                if standalone_pattern.search(content):
                    content = standalone_pattern.sub(rf'\1{new_name}\2', content)
                    file_updated = True
            
            if file_updated and content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_count += 1
                updated_files.add(filepath)
                print(f"  Updated: {filepath}")
        
        except Exception as e:
            print(f"  WARNING: Could not process {filepath}: {e}")
    
    print(f"\n✓ Updated {updated_count} files")
    if updated_files:
        print(f"\nUpdated files:")
        for f in sorted(updated_files):
            print(f"  - {f}")
    
    return updated_count


def main():
    """Main entry point."""
    print("=" * 60)
    print("Fix Remaining Filename References")
    print("=" * 60)
    
    mapping = load_mapping()
    if not mapping:
        return 1
    
    updated = fix_references(mapping)
    
    print("\n" + "=" * 60)
    print(f"✓ Fix complete. Updated {updated} files.")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review the changes: git diff")
    print("2. Verify no old references remain:")
    print("   git grep -l 'ACT_LOCAL_GITHUB_ACTIONS.md' || echo 'No old references'")
    print("3. Build documentation: mkdocs build --strict")
    
    return 0


if __name__ == '__main__':
    exit(main())

