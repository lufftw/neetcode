"""
Phase 5: Update all generators to output canonical JSON format.

Strategy:
1. Find all return/yield statements that use legacy format
2. Replace with json.dumps() serialization
3. Add import json if needed
"""
import re
from pathlib import Path

generators_dir = Path('generators')
updated = 0
errors = []

def add_json_import(content: str) -> str:
    """Add 'import json' if not present."""
    if 'import json' in content:
        return content
    
    # Add after other imports
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            continue
        if line.strip() and not line.startswith('#') and not line.startswith('"""'):
            # Insert before this line
            lines.insert(i, 'import json')
            break
    else:
        # Add at beginning after docstring
        for i, line in enumerate(lines):
            if '"""' in line and i > 0:
                # End of docstring
                lines.insert(i + 1, 'import json')
                break
    
    return '\n'.join(lines)

def update_generator(filepath: Path) -> bool:
    """Update a single generator file."""
    content = filepath.read_text(encoding='utf-8')
    original = content
    
    # Pattern 1: ' '.join(map(str, nums)) -> json.dumps(nums, separators=(',',':'))
    content = re.sub(
        r"' '\.join\(map\(str,\s*(\w+)\)\)",
        r'json.dumps(\1, separators=(",",":"))',
        content
    )
    
    # Pattern 2: ','.join(map(str, nums)) -> json.dumps(nums, separators=(',',':'))
    content = re.sub(
        r"','\.join\(map\(str,\s*(\w+)\)\)",
        r'json.dumps(\1, separators=(",",":"))',
        content
    )
    
    # Pattern 3: Hardcoded edge cases "1 2 3" -> json.dumps([1,2,3], ...)
    # This is tricky, need manual review for complex cases
    
    # Pattern 4: f"{var1}\n{var2}" multi-param - need to wrap each in json.dumps
    # Skip for now, handle manually
    
    # Pattern 5: return f"..." with space-separated -> JSON
    content = re.sub(
        r'return f"{\s*(\w+)\s*}"',
        r'return json.dumps(\1, separators=(",",":"))',
        content
    )
    
    if content != original:
        # Add import json
        content = add_json_import(content)
        filepath.write_text(content, encoding='utf-8')
        return True
    return False

# Process all generators
for filepath in sorted(generators_dir.glob('*.py')):
    if filepath.name.startswith('_'):
        continue
    try:
        if update_generator(filepath):
            print(f"Updated: {filepath.name}")
            updated += 1
        else:
            print(f"No changes: {filepath.name}")
    except Exception as e:
        errors.append((filepath.name, str(e)))
        print(f"Error: {filepath.name} - {e}")

print(f"\nTotal updated: {updated}")
if errors:
    print(f"Errors: {len(errors)}")
    for name, err in errors:
        print(f"  - {name}: {err}")

