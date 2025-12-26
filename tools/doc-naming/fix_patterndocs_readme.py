#!/usr/bin/env python3
"""
Fix filename errors in docs/tools/patterndocs/README.md caused by rename script.

This script fixes:
1. @03-base.md -> 0003-base.md (missing leading zeros and @ symbol)
2. 0076_variant.md -> 0076-variant.md (underscore to hyphen)
3. Missing leading zeros in filenames (e.g., 76-min-window.md -> 0076-min-window.md)
4. Special character issues in filenames
"""

import re
from pathlib import Path


def fix_filename_in_content(content: str) -> str:
    """Fix all filename errors in the content."""
    
    # Pattern 1: Fix @03-base.md -> 0003-base.md (in directory listings)
    # Matches: ├──@ followed by 1-3 digits, then - and filename
    content = re.sub(
        r'├──@(\d{1,3})(-[\w-]+\.md)',
        lambda m: f"├── {m.group(1).zfill(4)}{m.group(2)}",
        content
    )
    
    # Pattern 2: Fix "from@03-base.md" -> "from 0003-base.md"
    content = re.sub(
        r'from@(\d{1,3})(-[\w-]+\.md)',
        lambda m: f"from {m.group(1).zfill(4)}{m.group(2)}",
        content
    )
    
    # Pattern 3: Fix "Content from@03-base.md" -> "Content from 0003-base.md"
    content = re.sub(
        r'Content from@(\d{1,3})(-[\w-]+\.md)',
        lambda m: f"Content from {m.group(1).zfill(4)}{m.group(2)}",
        content
    )
    
    # Pattern 4: Fix filenames with underscore instead of hyphen
    # Matches: 4 digits, underscore, then rest of filename
    content = re.sub(
        r'(\d{4})_([\w-]+\.md)',
        lambda m: f"{m.group(1)}-{m.group(2)}",
        content
    )
    
    # Pattern 5: Fix filenames missing leading zeros (1-3 digits) in quotes
    # Matches: quote, then 1-3 digits, then - and filename
    content = re.sub(
        r'"(\d{1,3})(-[\w-]+\.md)"',
        lambda m: f'"{m.group(1).zfill(4)}{m.group(2)}"',
        content
    )
    
    # Pattern 6: Fix special characters before numbers in filenames (in TOML examples)
    # Matches: non-ASCII or special char, then 1-3 digits, then - and filename
    # This handles cases like "40-k-distinct.md" with special char prefix
    content = re.sub(
        r'"([^\x00-\x7F])(\d{1,3})(-[\w-]+\.md)"',
        lambda m: f'"{m.group(2).zfill(4)}{m.group(3)}"',
        content
    )
    
    # Pattern 7: Fix over-padding (5 digits back to 4)
    content = re.sub(
        r'(\d{5})(-[\w-]+\.md)',
        lambda m: f"{m.group(1)[1:]}{m.group(2)}",
        content
    )
    
    return content


def fix_readme():
    """Fix the README file."""
    readme_path = Path("docs/tools/patterndocs/README.md")
    
    print(f"Reading {readme_path}...")
    with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    print("Fixing filename errors...")
    content = fix_filename_in_content(content)
    
    if content != original:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {readme_path}")
        print("\nChanges made:")
        
        # Show what was changed
        original_lines = original.split('\n')
        new_lines = content.split('\n')
        for i, (old, new) in enumerate(zip(original_lines, new_lines), 1):
            if old != new:
                print(f"  Line {i}:")
                print(f"    Old: {old}")
                print(f"    New: {new}")
        
        return True
    else:
        print(f"No changes needed in {readme_path}")
        return False


if __name__ == '__main__':
    fix_readme()

