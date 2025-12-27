#!/usr/bin/env python3
"""
Rename HTML files in docs/pages/mindmaps to kebab-case.

Converts filenames from snake_case to kebab-case and updates all references.
"""

import re
import subprocess
from pathlib import Path
from typing import Dict, List


def to_kebab_case(filename: str) -> str:
    """Convert filename to kebab-case."""
    if filename.endswith('.html'):
        name = filename[:-5]
        ext = '.html'
    else:
        name = filename
        ext = ''
    
    # Replace underscores with hyphens
    name = name.replace('_', '-')
    # Convert to lowercase
    name = name.lower()
    # Remove any double hyphens
    name = re.sub(r'-+', '-', name)
    # Remove leading/trailing hyphens
    name = name.strip('-')
    
    return f"{name}{ext}" if ext else name


def get_html_files() -> List[Path]:
    """Get all HTML files in docs/pages/mindmaps."""
    mindmaps_dir = Path("docs/pages/mindmaps")
    if not mindmaps_dir.exists():
        print(f"ERROR: {mindmaps_dir} does not exist")
        return []
    
    html_files = list(mindmaps_dir.glob("*.html"))
    # Exclude index.html
    html_files = [f for f in html_files if f.name != "index.html"]
    return sorted(html_files)


def create_rename_mapping() -> Dict[str, str]:
    """Create mapping of old names to new kebab-case names."""
    html_files = get_html_files()
    mapping = {}
    
    for file_path in html_files:
        old_name = file_path.name
        new_name = to_kebab_case(old_name)
        
        if old_name != new_name:
            old_path = str(file_path)
            new_path = str(file_path.parent / new_name)
            mapping[old_path] = new_path
            print(f"  {old_name:50s} → {new_name}")
    
    return mapping


def rename_files(mapping: Dict[str, str]) -> int:
    """Rename files using git mv."""
    print(f"\nRenaming {len(mapping)} HTML files using git mv...\n")
    success_count = 0
    
    for old_path, new_path in sorted(mapping.items()):
        try:
            # Use forward slashes for git mv
            old_path_git = old_path.replace('\\', '/')
            new_path_git = new_path.replace('\\', '/')
            
            subprocess.run(
                ['git', 'mv', old_path_git, new_path_git],
                check=True,
                capture_output=True
            )
            print(f"✓ {old_path_git}")
            print(f"  → {new_path_git}")
            success_count += 1
        except subprocess.CalledProcessError as e:
            print(f"✗ ERROR: Failed to rename '{old_path_git}'")
            print(f"  {e.stderr.decode().strip()}")
        except Exception as e:
            print(f"✗ ERROR: Unexpected error renaming '{old_path}': {e}")
    
    print(f"\nSuccessfully renamed {success_count}/{len(mapping)} files.")
    return success_count


def update_references(mapping: Dict[str, str]) -> int:
    """Update all references to renamed HTML files."""
    print(f"\nUpdating references to {len(mapping)} renamed HTML files...")
    
    # Build filename mappings
    filename_mapping = {}
    path_mapping = {}
    
    for old_path, new_path in mapping.items():
        old_path_norm = old_path.replace('\\', '/')
        new_path_norm = new_path.replace('\\', '/')
        
        old_name = Path(old_path_norm).name
        new_name = Path(new_path_norm).name
        
        filename_mapping[old_name] = new_name
        path_mapping[old_path_norm] = new_path_norm
        
        # Also map relative paths
        old_rel = f"pages/mindmaps/{old_name}"
        new_rel = f"pages/mindmaps/{new_name}"
        path_mapping[old_rel] = new_rel
        
        # Map full URL paths
        old_url = f"https://lufftw.github.io/neetcode/pages/mindmaps/{old_name}"
        new_url = f"https://lufftw.github.io/neetcode/pages/mindmaps/{new_name}"
        path_mapping[old_url] = new_url
    
    # Get all files that might contain references
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
    
    files_to_check = [f for f in files_to_check if f.strip()]
    
    updated_count = 0
    for filepath in files_to_check:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            
            # Strategy 1: Replace full paths
            for old_path, new_path in path_mapping.items():
                if old_path in content:
                    content = content.replace(old_path, new_path)
            
            # Strategy 2: Replace filenames in various contexts
            for old_name, new_name in filename_mapping.items():
                # In markdown links: [text](path/to/old_name.html)
                content = re.sub(
                    rf'(\[.*?\]\([^)]*?){re.escape(old_name)}(\))',
                    rf'\1{new_name}\2',
                    content
                )
                
                # In URLs: https://.../old_name.html
                content = re.sub(
                    rf'(https?://[^/]+/[^/]+/){re.escape(old_name)}',
                    rf'\1{new_name}',
                    content
                )
                
                # Standalone filename (with word boundaries)
                content = re.sub(
                    rf'([\s\(\[\'"]){re.escape(old_name)}([\s\)\]\'".,;:!?])',
                    rf'\1{new_name}\2',
                    content
                )
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_count += 1
                print(f"  ✓ Updated: {filepath}")
        
        except Exception as e:
            print(f"  ✗ WARNING: Could not process {filepath}: {e}")
    
    print(f"\nUpdated references in {updated_count} files")
    return updated_count


def main():
    """Main entry point."""
    print("=" * 70)
    print("Rename Mindmap HTML Files to Kebab-Case")
    print("=" * 70)
    print()
    
    print("Step 1: Creating rename mapping...")
    mapping = create_rename_mapping()
    
    if not mapping:
        print("\nNo files need renaming.")
        return 0
    
    print(f"\nFound {len(mapping)} files to rename:")
    for old_path, new_path in mapping.items():
        print(f"  {Path(old_path).name} → {Path(new_path).name}")
    
    # Auto-proceed (no confirmation needed)
    # print("\n" + "=" * 70)
    # response = input("Proceed with renaming? (y/N): ").strip().lower()
    # if response != 'y':
    #     print("Cancelled.")
    #     return 0
    
    print("\nStep 2: Renaming files...")
    rename_count = rename_files(mapping)
    
    print("\nStep 3: Updating references...")
    update_count = update_references(mapping)
    
    print("\n" + "=" * 70)
    print(f"✓ Complete!")
    print(f"  - Renamed {rename_count} files")
    print(f"  - Updated {update_count} files with references")
    print("=" * 70)
    
    return 0


if __name__ == '__main__':
    exit(main())

