#!/usr/bin/env python3
"""
Update all references to renamed HTML mindmap files from snake_case to kebab-case.

This script updates:
- Python scripts that generate HTML files
- Configuration files
- Documentation files
"""

import re
from pathlib import Path
from typing import Dict, List

# Mapping of old snake_case names to new kebab-case names
HTML_RENAME_MAPPING = {
    'algorithm_usage': 'algorithm-usage',
    'company_coverage': 'company-coverage',
    'data_structure': 'data-structure',
    'difficulty_topics': 'difficulty-topics',
    'family_derivation': 'family-derivation',
    'pattern_hierarchy': 'pattern-hierarchy',
    'problem_relations': 'problem-relations',
    'roadmap_paths': 'roadmap-paths',
    'solution_variants': 'solution-variants',
}


def update_file_content(filepath: Path, mapping: Dict[str, str]) -> bool:
    """Update file content with new kebab-case names."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        
        # Replace in various contexts
        for old_name, new_name in mapping.items():
            # Pattern 1: f"{mm_type}.html" -> f"{kebab_type}.html"
            content = re.sub(
                rf'f"\{{\s*{re.escape(old_name)}\s*}}\.html"',
                rf'f"{{{{ {new_name} }}}}.html"',
                content
            )
            
            # Pattern 2: f"{mm_type}.html" (with quotes)
            content = re.sub(
                rf'f"\{{\s*["\']?{re.escape(old_name)}["\']?\s*}}\.html"',
                rf'f"{{{{ {new_name} }}}}.html"',
                content
            )
            
            # Pattern 3: Direct string replacement: "pattern_hierarchy.html"
            content = content.replace(f'"{old_name}.html"', f'"{new_name}.html"')
            content = content.replace(f"'{old_name}.html'", f"'{new_name}.html'")
            
            # Pattern 4: In file paths: pages_dir / "mindmaps" / f"{mm_type}.html"
            content = re.sub(
                rf'/{re.escape(old_name)}\.html',
                f'/{new_name}.html',
                content
            )
            
            # Pattern 5: Variable assignments: mm_type = "pattern_hierarchy"
            content = re.sub(
                rf'(\w+)\s*=\s*["\']{re.escape(old_name)}["\']',
                rf'\1 = "{new_name}"',
                content
            )
            
            # Pattern 6: Dictionary keys: "pattern_hierarchy": "..."
            content = re.sub(
                rf'["\']{re.escape(old_name)}["\']\s*:',
                f'"{new_name}":',
                content
            )
            
            # Pattern 7: In comments or documentation
            content = content.replace(f'{old_name}.html', f'{new_name}.html')
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"  ERROR: Could not process {filepath}: {e}")
        return False


def update_generate_mindmaps_py() -> bool:
    """Update tools/generate_mindmaps.py to generate kebab-case HTML filenames."""
    filepath = Path("tools/generate_mindmaps.py")
    if not filepath.exists():
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Find the line that generates HTML filename: html_file = pages_dir / "mindmaps" / f"{mm_type}.html"
        # Replace with a function call to convert snake_case to kebab-case
        pattern = r'html_file = pages_dir / "mindmaps" / f"\{mm_type\}\.html"'
        replacement = '''html_file = pages_dir / "mindmaps" / f"{mm_type.replace('_', '-')}.html"'''
        
        content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"  ERROR: Could not update {filepath}: {e}")
        return False


def main():
    """Main entry point."""
    print("=" * 70)
    print("Update HTML Mindmap References to Kebab-Case")
    print("=" * 70)
    print()
    
    updated_files = []
    
    # Files to check and update
    files_to_check = [
        "tools/generate_mindmaps.py",
        "tools/html_meta_description_generator.toml",
        "tools/ai_mindmap/html_generator.py",
        "tools/generate_mindmaps_ai.py",
        "tools/generate_mindmaps_ai.toml",
    ]
    
    print("Step 1: Updating Python scripts...")
    for filepath_str in files_to_check:
        filepath = Path(filepath_str)
        if filepath.exists():
            if update_file_content(filepath, HTML_RENAME_MAPPING):
                print(f"  OK: Updated {filepath}")
                updated_files.append(filepath_str)
            else:
                print(f"  SKIP: No changes needed in {filepath}")
        else:
            print(f"  SKIP: {filepath} does not exist")
    
    print("\nStep 2: Updating generate_mindmaps.py HTML filename generation...")
    if update_generate_mindmaps_py():
        print("  OK: Updated HTML filename generation in tools/generate_mindmaps.py")
        updated_files.append("tools/generate_mindmaps.py")
    else:
        print("  SKIP: No changes needed")
    
    print("\n" + "=" * 70)
    if updated_files:
        print(f"Complete! Updated {len(updated_files)} file(s):")
        for f in updated_files:
            print(f"  - {f}")
    else:
        print("Complete! No files needed updates.")
    print("=" * 70)
    
    return 0


if __name__ == '__main__':
    exit(main())

