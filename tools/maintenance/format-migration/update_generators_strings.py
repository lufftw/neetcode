"""
Phase 5 (Part 2): Update string-based generators to use JSON format.
"""
import re
from pathlib import Path

# Generators that handle strings
string_generators = [
    '0003_longest_substring_without_repeating_characters.py',
    '0076_minimum_window_substring.py',  # Already done
    '0093_restore_ip_addresses.py',
    '0125_valid_palindrome.py',
    '0131_palindrome_partitioning.py',
    '0340_longest_substring_with_at_most_k_distinct.py',
    '0438_find_all_anagrams_in_a_string.py',
    '0567_permutation_in_string.py',
    '0680_valid_palindrome_ii.py',
]

# Integer-based that need edge case updates
int_generators = [
    '0004_median_of_two_sorted_arrays.py',
    '0077_combinations.py',
    '0079_word_search.py',
    '0216_combination_sum_iii.py',
]

def update_file(filepath: Path):
    content = filepath.read_text(encoding='utf-8')
    original = content
    
    # Add import json if not present
    if 'import json' not in content:
        # Add after first import line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('import ') and 'json' not in line:
                lines.insert(i, 'import json')
                break
        content = '\n'.join(lines)
    
    # Pattern: yield f"{var1}\n{var2}" -> yield f"{json.dumps(var1)}\n{json.dumps(var2)}"
    # But be careful - var2 might be an int (like k)
    
    # Pattern for string vars: f"{s}\n{t}" where s, t are strings
    content = re.sub(
        r'yield f"\{(\w+)\}\\n\{(\w+)\}"',
        r'yield f"{json.dumps(\1)}\\n{json.dumps(\2) if isinstance(\2, str) else \2}"',
        content
    )
    
    # Simpler pattern for return statements
    content = re.sub(
        r'return f"\{(\w+)\}\\n\{(\w+)\}"',
        r'return f"{json.dumps(\1)}\\n{json.dumps(\2) if isinstance(\2, str) else \2}"',
        content
    )
    
    if content != original:
        filepath.write_text(content, encoding='utf-8')
        return True
    return False

generators_dir = Path('generators')
updated = 0

for filename in string_generators + int_generators:
    filepath = generators_dir / filename
    if filepath.exists():
        try:
            if update_file(filepath):
                print(f"Updated: {filename}")
                updated += 1
            else:
                print(f"No changes needed: {filename}")
        except Exception as e:
            print(f"Error {filename}: {e}")
    else:
        print(f"Not found: {filename}")

print(f"\nTotal updated: {updated}")

