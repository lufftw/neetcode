"""
Batch fix all test files to canonical JSON format.

Fixes:
1. Single numbers that should be arrays: 1 -> [1]
2. Spaces in arrays: [0, 1] -> [0,1]
3. Python booleans: True/False -> true/false
4. Single quotes: ['a'] -> ["a"]
5. Space-separated values: 1 2 3 -> [1,2,3]
"""
import json
import re
from pathlib import Path

tests_dir = Path('tests')
fixed_in = 0
fixed_out = 0

def fix_content(content: str, is_output: bool = False) -> tuple[str, bool]:
    """Fix content to canonical format. Returns (fixed_content, was_changed)."""
    lines = content.strip().split('\n')
    new_lines = []
    changed = False
    
    for line in lines:
        original_line = line
        line = line.strip()
        
        if not line:
            new_lines.append('')
            continue
        
        # Try to parse and re-serialize as JSON
        try:
            # Handle Python-style booleans first
            if line == 'True':
                new_lines.append('true')
                changed = True
                continue
            elif line == 'False':
                new_lines.append('false')
                changed = True
                continue
            
            # Handle single quotes -> double quotes for parsing
            line_for_parse = line.replace("'", '"')
            
            # Try JSON parse
            if line_for_parse.startswith('[') or line_for_parse.startswith('{'):
                parsed = json.loads(line_for_parse)
                canonical = json.dumps(parsed, separators=(',', ':'))
                if canonical != line:
                    changed = True
                new_lines.append(canonical)
                continue
            
            # Handle quoted strings
            if line_for_parse.startswith('"'):
                parsed = json.loads(line_for_parse)
                canonical = json.dumps(parsed)
                if canonical != line:
                    changed = True
                new_lines.append(canonical)
                continue
            
            # Handle numbers
            try:
                if '.' in line:
                    float(line)
                else:
                    int(line)
                new_lines.append(line)
                continue
            except ValueError:
                pass
            
            # Handle space-separated numbers (convert to array)
            if re.match(r'^-?\d+(\s+-?\d+)+$', line):
                nums = list(map(int, line.split()))
                canonical = json.dumps(nums, separators=(',', ':'))
                new_lines.append(canonical)
                changed = True
                continue
            
            # Plain text, keep as-is
            new_lines.append(line)
            
        except (json.JSONDecodeError, ValueError):
            # Can't parse, keep original
            new_lines.append(line)
    
    return '\n'.join(new_lines), changed

def needs_array_wrapper(filepath: Path) -> bool:
    """Check if a single number should be wrapped as array based on problem type."""
    # Problems that return arrays
    array_return_problems = [
        '0001_two_sum',
        '0015_3sum', '0016_3sum_closest',
        '0026_remove_duplicates', '0027_remove_element',
        '0039_combination_sum', '0040_combination_sum_ii',
        '0046_permutations', '0047_permutations_ii',
        '0075_sort_colors', '0077_combinations', '0078_subsets',
        '0080_remove_duplicates', '0088_merge_sorted_array',
        '0090_subsets_ii', '0093_restore_ip_addresses',
        '0131_palindrome_partitioning',
        '0215_kth_largest',  # This returns int, not array
        '0216_combination_sum_iii',
        '0283_move_zeroes',
        '0876_middle',  # Linked list
        '0905_sort_array', '0922_sort_array',
        '0977_squares',
    ]
    
    name = filepath.stem
    for pattern in array_return_problems:
        if pattern in name:
            # Check if it's .in file (input should be array)
            if filepath.suffix == '.in':
                return True
            # For .out, check if this problem returns array
            if pattern not in ['0215_kth_largest']:
                return True
    return False

# Process all test files
for filepath in sorted(tests_dir.glob('*.*')):
    if filepath.suffix not in ['.in', '.out']:
        continue
    if '.bak' in filepath.name:
        continue
    
    content = filepath.read_text(encoding='utf-8')
    is_output = filepath.suffix == '.out'
    
    fixed_content, changed = fix_content(content, is_output)
    
    # Check for single number that should be array (in .in files mainly)
    lines = fixed_content.strip().split('\n')
    new_lines = []
    for i, line in enumerate(lines):
        # If line is just a number and file needs array
        if re.match(r'^-?\d+$', line.strip()) and needs_array_wrapper(filepath):
            # Check context - if it's the first line of an array problem's .in
            # or the output of an array-returning problem
            if (filepath.suffix == '.in' and i == 0) or \
               (filepath.suffix == '.out' and needs_array_wrapper(filepath)):
                # Wrap as array
                new_lines.append(f'[{line.strip()}]')
                changed = True
                continue
        new_lines.append(line)
    
    fixed_content = '\n'.join(new_lines)
    
    if changed:
        # Ensure trailing newline
        if not fixed_content.endswith('\n'):
            fixed_content += '\n'
        filepath.write_text(fixed_content, encoding='utf-8')
        if is_output:
            fixed_out += 1
            print(f"Fixed .out: {filepath.name}")
        else:
            fixed_in += 1
            print(f"Fixed .in:  {filepath.name}")

print(f"\nTotal fixed: {fixed_in} .in files, {fixed_out} .out files")


