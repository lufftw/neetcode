#!/usr/bin/env python3
"""
Rename HTML files in docs/pages/mindmaps from snake_case to kebab-case.

This script renames the HTML files and updates all references.
"""

import subprocess
from pathlib import Path
from typing import Dict


# Mapping of old snake_case names to new kebab-case names
HTML_RENAME_MAPPING = {
    'algorithm_usage.html': 'algorithm-usage.html',
    'company_coverage.html': 'company-coverage.html',
    'data_structure.html': 'data-structure.html',
    'difficulty_topics.html': 'difficulty-topics.html',
    'family_derivation.html': 'family-derivation.html',
    'pattern_hierarchy.html': 'pattern-hierarchy.html',
    'problem_relations.html': 'problem-relations.html',
    'roadmap_paths.html': 'roadmap-paths.html',
    'solution_variants.html': 'solution-variants.html',
}


def rename_html_files() -> int:
    """Rename HTML files using git mv."""
    mindmaps_dir = Path("docs/pages/mindmaps")
    
    print("Renaming HTML files in docs/pages/mindmaps...")
    print()
    
    success_count = 0
    for old_name, new_name in HTML_RENAME_MAPPING.items():
        old_path = mindmaps_dir / old_name
        new_path = mindmaps_dir / new_name
        
        if not old_path.exists():
            print(f"SKIP: {old_path} does not exist")
            continue
        
        try:
            # Check if file is tracked by git
            result = subprocess.run(
                ['git', 'ls-files', '--error-unmatch', str(old_path)],
                capture_output=True,
                check=False
            )
            
            if result.returncode == 0:
                # File is tracked, use git mv
                old_path_git = str(old_path).replace('\\', '/')
                new_path_git = str(new_path).replace('\\', '/')
                
                subprocess.run(
                    ['git', 'mv', old_path_git, new_path_git],
                    check=True,
                    capture_output=True
                )
                print(f"OK (git mv): {old_path_git}")
                print(f"   -> {new_path_git}")
            else:
                # File is not tracked, use regular file system rename
                import shutil
                shutil.move(str(old_path), str(new_path))
                print(f"OK (fs mv): {old_path}")
                print(f"   -> {new_path}")
            
            success_count += 1
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to rename {old_path}")
            error_msg = e.stderr.decode() if e.stderr else str(e)
            print(f"  {error_msg}")
        except Exception as e:
            print(f"ERROR: Unexpected error renaming {old_path}: {e}")
    
    print()
    print(f"Successfully renamed {success_count}/{len(HTML_RENAME_MAPPING)} files.")
    return success_count


def update_references() -> int:
    """Update all references to renamed HTML files."""
    print("\nUpdating references to renamed HTML files...")
    
    # Build mappings
    filename_mapping = {}
    path_mapping = {}
    
    for old_name, new_name in HTML_RENAME_MAPPING.items():
        filename_mapping[old_name] = new_name
        
        # Full paths
        old_path = f"docs/pages/mindmaps/{old_name}"
        new_path = f"docs/pages/mindmaps/{new_name}"
        path_mapping[old_path] = new_path
        
        # URLs
        old_url = f"https://lufftw.github.io/neetcode/pages/mindmaps/{old_name}"
        new_url = f"https://lufftw.github.io/neetcode/pages/mindmaps/{new_name}"
        path_mapping[old_url] = new_url
        
        # Relative paths
        old_rel = f"pages/mindmaps/{old_name}"
        new_rel = f"pages/mindmaps/{new_name}"
        path_mapping[old_rel] = new_rel
        
        # Relative paths with ../
        old_rel_up = f"../pages/mindmaps/{old_name}"
        new_rel_up = f"../pages/mindmaps/{new_name}"
        path_mapping[old_rel_up] = new_rel_up
    
    # Get all files that might contain references
    extensions = ['.md', '.yml', '.yaml', '.py', '.txt', '.json', '.toml', '.html']
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
            
            # Replace all path variants
            for old_path, new_path in path_mapping.items():
                if old_path in content:
                    content = content.replace(old_path, new_path)
            
            # Replace filenames in various contexts
            for old_name, new_name in filename_mapping.items():
                # In markdown links: [text](path/to/old_name.html)
                import re
                content = re.sub(
                    rf'(\[.*?\]\([^)]*?){re.escape(old_name)}(\))',
                    rf'\1{new_name}\2',
                    content
                )
                
                # In URLs
                content = re.sub(
                    rf'(https?://[^/]+/[^/]+/){re.escape(old_name)}',
                    rf'\1{new_name}',
                    content
                )
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_count += 1
                print(f"  OK: Updated {filepath}")
        
        except Exception as e:
            print(f"  WARNING: Could not process {filepath}: {e}")
    
    print(f"\nUpdated references in {updated_count} files")
    return updated_count


def main():
    """Main entry point."""
    print("=" * 70)
    print("Rename Mindmap HTML Files to Kebab-Case")
    print("=" * 70)
    print()
    
    print("Step 1: Renaming HTML files...")
    rename_count = rename_html_files()
    
    print("\nStep 2: Updating references...")
    update_count = update_references()
    
    print("\n" + "=" * 70)
    print(f"Complete!")
    print(f"  - Renamed {rename_count} HTML files")
    print(f"  - Updated {update_count} files with references")
    print("=" * 70)
    
    return 0


if __name__ == '__main__':
    exit(main())

