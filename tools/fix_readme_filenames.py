#!/usr/bin/env python3
"""Fix filename errors in docs/patterns/README.md"""

import re
from pathlib import Path

def fix_readme():
    readme_path = Path("docs/patterns/README.md")
    
    with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    # Fix the example file listing (lines 101-106)
    # Replace incorrect filenames with correct 4-digit format
    replacements = [
        (r'@03-base\.md', '0003-base.md'),
        (r'@76-min-window\.md', '0076-min-window.md'),
        (r'B09-min-subarray\.md', '0209-min-subarray.md'),
        (r'C40-k-distinct\.md', '0340-k-distinct.md'),
        (r'D38-anagrams\.md', '0438-anagrams.md'),
        (r'E67-permutation\.md', '0567-permutation.md'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Fix the config example (line 116)
    # Replace any incorrect filename patterns in the problem_files array
    # Match patterns like "76-min-window.md" or special characters before numbers
    # But avoid matching already correct 4-digit numbers
    content = re.sub(
        r'"([^\d"]*?)(\d{1,3})([^"]*?\.md)"',
        lambda m: f'"{m.group(1)}{m.group(2).zfill(4)}{m.group(3)}"',
        content
    )
    
    # Fix over-padding (5 digits back to 4)
    content = re.sub(
        r'"(\d{5})([^"]*?\.md)"',
        lambda m: f'"{m.group(1)[1:]}{m.group(2)}"',
        content
    )
    
    # Fix any remaining special character issues
    # Replace any non-ASCII characters before numbers in filenames
    content = re.sub(
        r'([^\x00-\x7F])(\d{1,3})(-.*?\.md)',
        lambda m: f'{m.group(2).zfill(4)}{m.group(3)}',
        content
    )
    
    if content != original:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {readme_path}")
        return True
    else:
        print(f"No changes needed in {readme_path}")
        return False

if __name__ == '__main__':
    fix_readme()

