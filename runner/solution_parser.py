# runner/solution_parser.py
"""
Solution Parser - Extract approach names and details from solution class comments.

Parses the standard comment block format:
    # ============================================================================
    # Solution N: Approach Name
    # Time: O(?), Space: O(?)
    #   - Key insight or implementation detail
    # ============================================================================
    class SolutionName:

Provides utilities to map class names to their approach descriptions.
"""
import re
import os
from typing import Dict, Optional, Tuple


def parse_class_headers(solution_path: str) -> Dict[str, dict]:
    """
    Parse solution file to extract class header comments.
    
    Args:
        solution_path: Path to the solution .py file
    
    Returns:
        Dict mapping class_name -> {
            'solution_num': int or None,
            'approach': str,
            'time': str or None,
            'space': str or None,
            'details': list of str
        }
    
    Example:
        {
            'SolutionDP': {
                'solution_num': 1,
                'approach': 'Backtracking with DP-Precomputed Palindrome Table',
                'time': 'O(n × 2^n)',
                'space': 'O(n^2)',
                'details': ['Precompute is_palindrome[i][j] for O(1) checks', ...]
            }
        }
    """
    if not os.path.exists(solution_path):
        return {}
    
    with open(solution_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    results = {}
    
    # Pattern to find class header blocks
    # Matches:
    # # ===========...
    # # Solution N: Approach Name
    # # Time: ..., Space: ...
    # #   - details...
    # # ===========...
    # class ClassName:
    
    # Find all class definitions
    class_pattern = re.compile(r'^class\s+(\w+)\s*[:\(]', re.MULTILINE)
    
    for match in class_pattern.finditer(content):
        class_name = match.group(1)
        class_pos = match.start()
        
        # Look for comment block before this class
        # Search backwards from class position
        before_class = content[:class_pos].rstrip()
        
        # Find the comment block (lines starting with #)
        lines_before = before_class.split('\n')
        comment_lines = []
        
        # Collect comment lines backwards until we hit non-comment
        for line in reversed(lines_before):
            stripped = line.strip()
            if stripped.startswith('#'):
                comment_lines.insert(0, stripped)
            elif stripped == '':
                continue  # Skip empty lines
            else:
                break  # Stop at non-comment line
        
        if not comment_lines:
            continue
        
        # Parse the comment block
        header_info = _parse_comment_block(comment_lines)
        if header_info:
            results[class_name] = header_info
    
    return results


def _parse_comment_block(lines: list) -> Optional[dict]:
    """
    Parse a block of comment lines to extract solution info.
    
    Expected format:
        # ============...
        # Solution N: Approach Name
        # Time: O(?), Space: O(?)
        #   - detail 1
        #   - detail 2
        # ============...
    """
    result = {
        'solution_num': None,
        'approach': None,
        'time': None,
        'space': None,
        'details': []
    }
    
    for line in lines:
        # Remove leading # and strip
        text = line.lstrip('#').strip()
        
        # Skip separator lines
        if text.startswith('===') or text.startswith('---'):
            continue
        
        # Match "Solution N: Approach Name"
        sol_match = re.match(r'^Solution\s*(\d+)\s*:\s*(.+)$', text, re.IGNORECASE)
        if sol_match:
            result['solution_num'] = int(sol_match.group(1))
            result['approach'] = sol_match.group(2).strip()
            continue
        
        # Match "Time: O(...), Space: O(...)"
        time_space_match = re.match(r'^Time:\s*(.+?),\s*Space:\s*(.+)$', text, re.IGNORECASE)
        if time_space_match:
            result['time'] = time_space_match.group(1).strip()
            result['space'] = time_space_match.group(2).strip()
            continue
        
        # Match detail lines "- something"
        detail_match = re.match(r'^-\s*(.+)$', text)
        if detail_match:
            result['details'].append(detail_match.group(1).strip())
            continue
    
    # Only return if we found at least an approach name
    if result['approach']:
        return result
    
    return None


def get_approach_info(solution_path: str, class_name: str) -> Optional[dict]:
    """
    Get approach info for a specific class.
    
    Args:
        solution_path: Path to the solution .py file
        class_name: Name of the class to look up
    
    Returns:
        Dict with approach info or None
    """
    headers = parse_class_headers(solution_path)
    return headers.get(class_name)


def format_method_display(shorthand: str, method_info: dict, 
                          approach_info: Optional[dict] = None) -> Tuple[str, str]:
    """
    Format method display info for enhanced output.
    
    Args:
        shorthand: The method key (e.g., "default", "naive")
        method_info: The SOLUTIONS entry dict
        approach_info: Optional parsed class header info
    
    Returns:
        Tuple of (short_name, full_description)
        - short_name: For compact display in charts
        - full_description: For detailed output
    """
    # Build full description
    if approach_info and approach_info.get('approach'):
        approach = approach_info['approach']
        sol_num = approach_info.get('solution_num')
        if sol_num:
            full_desc = f"Solution {sol_num}: {approach}"
        else:
            full_desc = approach
    elif method_info.get('description'):
        full_desc = method_info['description']
    else:
        full_desc = shorthand
    
    return shorthand, full_desc


def build_method_mapping(solution_path: str, solutions_meta: dict) -> Dict[str, dict]:
    """
    Build a complete mapping of method shorthands to their full info.
    
    Args:
        solution_path: Path to the solution .py file
        solutions_meta: The SOLUTIONS dictionary from the solution file
    
    Returns:
        Dict mapping shorthand -> {
            'shorthand': str,
            'class': str,
            'approach': str,
            'complexity': str,
            'time': str,
            'space': str,
            'details': list
        }
    """
    # Parse class headers
    class_headers = parse_class_headers(solution_path)
    
    result = {}
    
    for shorthand, info in solutions_meta.items():
        class_name = info.get('class', '')
        class_info = class_headers.get(class_name, {})
        
        result[shorthand] = {
            'shorthand': shorthand,
            'class': class_name,
            'approach': class_info.get('approach') or info.get('description', shorthand),
            'complexity': info.get('complexity', 'Unknown'),
            'time': class_info.get('time'),
            'space': class_info.get('space'),
            'details': class_info.get('details', []),
            'solution_num': class_info.get('solution_num'),
        }
    
    return result


__all__ = [
    'parse_class_headers',
    'get_approach_info',
    'format_method_display',
    'build_method_mapping',
]

