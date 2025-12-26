#!/usr/bin/env python3
"""
Fix references to renamed HTML files in docs/pages/mindmaps.

Updates all references from snake_case to kebab-case filenames.
"""

import re
from pathlib import Path
from typing import Dict


# Mapping of old snake_case names to new kebab-case names
HTML_RENAME_MAPPING = {
    'algorithm_usage.html': 'algorithm-usage.html',
    'company_coverage.html': 'company-coverage.html',
    'data_structure.html': 'data-structure.html',
    'difficulty_topics.html': 'difficulty-topics.html',
    'family_derivation.html': 'family-derivation.html',
    'neetcode_ontology_agent_evolved_en.html': 'neetcode-ontology-agent-evolved-en.html',
    'neetcode_ontology_agent_evolved_zh-TW.html': 'neetcode-ontology-agent-evolved-zh-tw.html',
    'neetcode_ontology_ai_en.html': 'neetcode-ontology-ai-en.html',
    'neetcode_ontology_ai_zh-TW.html': 'neetcode-ontology-ai-zh-tw.html',
    'pattern_hierarchy.html': 'pattern-hierarchy.html',
    'problem_relations.html': 'problem-relations.html',
    'roadmap_paths.html': 'roadmap-paths.html',
    'solution_variants.html': 'solution-variants.html',
}


def update_file_references(filepath: str) -> bool:
    """Update HTML file references in a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        updated = False
        
        # Replace all old HTML filenames with new ones
        for old_name, new_name in HTML_RENAME_MAPPING.items():
            # Pattern 1: Full URL
            old_url = f"https://lufftw.github.io/neetcode/pages/mindmaps/{old_name}"
            new_url = f"https://lufftw.github.io/neetcode/pages/mindmaps/{new_name}"
            if old_url in content:
                content = content.replace(old_url, new_url)
                updated = True
            
            # Pattern 2: Relative path in URL
            old_path = f"pages/mindmaps/{old_name}"
            new_path = f"pages/mindmaps/{new_name}"
            if old_path in content:
                content = content.replace(old_path, new_path)
                updated = True
            
            # Pattern 3: Just filename (in various contexts)
            # Use regex to match filename with word boundaries
            escaped_old = re.escape(old_name)
            pattern = re.compile(
                rf'(["\']?pages/mindmaps/){escaped_old}(["\']?)',
                re.IGNORECASE
            )
            if pattern.search(content):
                content = pattern.sub(rf'\1{new_name}\2', content)
                updated = True
            
            # Pattern 4: Standalone filename in URLs
            pattern2 = re.compile(
                rf'(https?://[^/]+/[^/]+/){escaped_old}([^"\'>\s]*)',
                re.IGNORECASE
            )
            if pattern2.search(content):
                content = pattern2.sub(rf'\1{new_name}\2', content)
                updated = True
        
        if updated and content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    except Exception as e:
        print(f"  ERROR: Could not process {filepath}: {e}")
        return False


def main():
    """Main entry point."""
    print("=" * 70)
    print("Fix HTML File References")
    print("=" * 70)
    print()
    
    # Files that likely contain HTML references
    files_to_check = [
        'README.md',
        'README_zh-TW.md',
        'docs/mkdocs-content-guide.md',
        'docs/mindmaps/index.md',
        'docs/tools/ai-markmap-agent/README.md',
        'docs/tools/README.md',
        'docs/github-pages-setup.md',
        'docs/build-docs-manual.md',
        'tools/ai-markmap-agent/convert_to_html.toml',
        'tools/ai-markmap-agent/convert_to_html.py',
        'tools/ai-markmap-agent/docs/design-v4.md',
        'tools/ai-markmap-agent/docs/design-v3.md',
        'tools/ai-markmap-agent/docs/design-v2.md',
        'tools/ai_mindmap/html_generator.py',
        'tools/generate_mindmaps_ai.toml',
    ]
    
    print(f"Checking {len(files_to_check)} files for HTML references...")
    print()
    
    updated_count = 0
    for filepath in files_to_check:
        if not Path(filepath).exists():
            continue
        
        if update_file_references(filepath):
            print(f"  OK: Updated {filepath}")
            updated_count += 1
    
    print()
    print("=" * 70)
    print(f"Complete! Updated {updated_count} files.")
    print("=" * 70)
    
    return 0


if __name__ == '__main__':
    exit(main())

