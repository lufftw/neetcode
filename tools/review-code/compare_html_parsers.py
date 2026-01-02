#!/usr/bin/env python3
"""
Compare HTML Example Parsing Methods

This script compares two approaches for parsing LeetCode example test cases:
- Method A: Regex/String-based (current implementation in tools/docstring/formatter.py)
- Method B: DOM-based using BeautifulSoup

Purpose:
    Development decision tool for validating HTML parsing approaches.
    Used to determine the best method for extracting Example Input/Output
    from LeetCode problem descriptions.

Usage:
    python tools/review-code/compare_html_parsers.py [problem_id]
    
Examples:
    python tools/review-code/compare_html_parsers.py 3
    python tools/review-code/compare_html_parsers.py 1
    python tools/review-code/compare_html_parsers.py 51

Future Work:
    TODO: Add batch testing against all problems in leetcode_datasource database
          to validate regex patterns comprehensively.

Related:
    - tools/docstring/formatter.py::_extract_examples() - Current regex implementation
    - packages/leetcode_datasource - Data source for problem HTML
    - docs/in-progress/new-problem-tests-autogen/ - Feature specification
"""

import sys
import io
import re
import html
import time
from pathlib import Path
from typing import List, Dict, Optional

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from packages.leetcode_datasource import LeetCodeDataSource

# ============================================================
# Method A: Regex/String-based (adapted from tools/docstring/formatter.py)
# ============================================================

def method_a_extract_examples(html_body: str) -> List[Dict]:
    """
    Extract examples using regex/string-based approach.
    Adapted from tools/docstring/formatter.py::_extract_examples()
    """
    if not html_body:
        return []
    
    examples = []
    
    # Pattern to find Example blocks
    example_pattern = r'<p>\s*<strong[^>]*>\s*Example\s*(\d+):\s*</strong>\s*</p>(.*?)(?=<p>\s*<strong[^>]*>\s*(?:Example\s*\d+:|Constraints?:|Follow[\s-]?up|Note:)|<p>\s*&nbsp;\s*</p>\s*<p>\s*<strong>Constraints|<strong>Follow-up|$)'
    matches = re.findall(example_pattern, html_body, re.DOTALL | re.IGNORECASE)
    
    for num, content in matches:
        example = {
            'number': int(num),
            'input': '',
            'output': '',
            'explanation': '',
            'parse_success': True,
            'parse_notes': []
        }
        
        # Check if content is in <pre> block
        pre_match = re.search(r'<pre[^>]*>(.*?)</pre>', content, re.DOTALL | re.IGNORECASE)
        if pre_match:
            pre_content = pre_match.group(1)
            
            # Extract Input
            input_match = re.search(r'<strong>Input:</strong>\s*(.*?)(?=\n<strong>|$)', pre_content, re.DOTALL | re.IGNORECASE)
            if input_match:
                input_text = re.sub(r'<[^>]+>', '', input_match.group(1))
                example['input'] = html.unescape(input_text).strip()
            else:
                example['parse_notes'].append('Input not found in <pre>')
            
            # Extract Output
            output_match = re.search(r'<strong>Output:</strong>\s*(.*?)(?=\n<strong>|$)', pre_content, re.DOTALL | re.IGNORECASE)
            if output_match:
                output_text = re.sub(r'<[^>]+>', '', output_match.group(1))
                example['output'] = html.unescape(output_text).strip()
            else:
                example['parse_notes'].append('Output not found in <pre>')
                example['parse_success'] = False
            
            # Extract Explanation (optional)
            expl_match = re.search(r'<strong>Explanation:</strong>\s*(.*?)$', pre_content, re.DOTALL | re.IGNORECASE)
            if expl_match:
                expl_text = re.sub(r'<[^>]+>', '', expl_match.group(1))
                example['explanation'] = html.unescape(expl_text).strip()
        else:
            # Old format without <pre>
            input_match = re.search(r'<strong[^>]*>\s*Input:\s*</strong>\s*(.*?)(?=<strong|$)', content, re.DOTALL | re.IGNORECASE)
            if input_match:
                input_text = re.sub(r'<[^>]+>', '', input_match.group(1))
                example['input'] = html.unescape(input_text).strip()
            
            output_match = re.search(r'<strong[^>]*>\s*Output:\s*</strong>\s*(.*?)(?=<strong|$)', content, re.DOTALL | re.IGNORECASE)
            if output_match:
                output_text = re.sub(r'<[^>]+>', '', output_match.group(1))
                example['output'] = html.unescape(output_text).strip()
            else:
                example['parse_success'] = False
        
        examples.append(example)
    
    return examples


# ============================================================
# Method B: DOM-based using BeautifulSoup
# ============================================================

def method_b_extract_examples(html_body: str) -> List[Dict]:
    """
    Extract examples using BeautifulSoup DOM parsing.
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return [{
            'number': 0,
            'input': '',
            'output': '',
            'explanation': '',
            'parse_success': False,
            'parse_notes': ['BeautifulSoup not installed (pip install beautifulsoup4)']
        }]
    
    if not html_body:
        return []
    
    soup = BeautifulSoup(html_body, 'html.parser')
    examples = []
    
    # Find all Example headers
    example_headers = soup.find_all('strong', string=re.compile(r'Example\s*\d+:', re.IGNORECASE))
    
    # Also check for class="example"
    example_headers_by_class = soup.find_all('strong', class_='example')
    for h in example_headers_by_class:
        if h not in example_headers:
            example_headers.append(h)
    
    for header in example_headers:
        # Extract example number
        num_match = re.search(r'Example\s*(\d+)', header.get_text(), re.IGNORECASE)
        if not num_match:
            continue
        
        example = {
            'number': int(num_match.group(1)),
            'input': '',
            'output': '',
            'explanation': '',
            'parse_success': True,
            'parse_notes': []
        }
        
        # Find the <pre> block following the header
        # Navigate: header -> parent <p> -> next sibling <pre>
        parent_p = header.find_parent('p')
        if parent_p:
            pre_block = parent_p.find_next_sibling('pre')
            if pre_block:
                pre_text = pre_block.get_text()
                
                # Parse Input
                input_match = re.search(r'Input:\s*(.*?)(?=Output:|$)', pre_text, re.DOTALL)
                if input_match:
                    example['input'] = input_match.group(1).strip()
                else:
                    example['parse_notes'].append('Input not found in <pre>')
                
                # Parse Output
                output_match = re.search(r'Output:\s*(.*?)(?=Explanation:|$)', pre_text, re.DOTALL)
                if output_match:
                    example['output'] = output_match.group(1).strip()
                else:
                    example['parse_success'] = False
                    example['parse_notes'].append('Output not found in <pre>')
                
                # Parse Explanation (optional)
                expl_match = re.search(r'Explanation:\s*(.*?)$', pre_text, re.DOTALL)
                if expl_match:
                    example['explanation'] = expl_match.group(1).strip()
            else:
                example['parse_notes'].append('No <pre> block found after header')
        else:
            example['parse_notes'].append('Header not in <p> element')
        
        examples.append(example)
    
    return examples


# ============================================================
# Comparison Logic
# ============================================================

def compare_results(examples_a: List[Dict], examples_b: List[Dict]) -> Dict:
    """Compare results from both methods."""
    comparison = {
        'method_a_count': len(examples_a),
        'method_b_count': len(examples_b),
        'count_match': len(examples_a) == len(examples_b),
        'examples': []
    }
    
    max_len = max(len(examples_a), len(examples_b)) if examples_a or examples_b else 0
    
    for i in range(max_len):
        ex_a = examples_a[i] if i < len(examples_a) else None
        ex_b = examples_b[i] if i < len(examples_b) else None
        
        ex_comparison = {
            'index': i + 1,
            'input_match': False,
            'output_match': False,
            'method_a': ex_a,
            'method_b': ex_b,
        }
        
        if ex_a and ex_b:
            ex_comparison['input_match'] = ex_a['input'] == ex_b['input']
            ex_comparison['output_match'] = ex_a['output'] == ex_b['output']
        
        comparison['examples'].append(ex_comparison)
    
    return comparison


def print_comparison(problem_id: int, html_body: str):
    """Print detailed comparison of both parsing methods."""
    
    print("=" * 80)
    print(f"HTML Example Parser Comparison - Problem {problem_id}")
    print("=" * 80)
    print()
    
    # Method A: Regex
    print("Running Method A (Regex/String-based)...")
    start_a = time.perf_counter()
    examples_a = method_a_extract_examples(html_body)
    time_a = (time.perf_counter() - start_a) * 1000
    print(f"  Time: {time_a:.3f}ms")
    print(f"  Examples found: {len(examples_a)}")
    print()
    
    # Method B: BeautifulSoup
    print("Running Method B (BeautifulSoup DOM)...")
    start_b = time.perf_counter()
    examples_b = method_b_extract_examples(html_body)
    time_b = (time.perf_counter() - start_b) * 1000
    print(f"  Time: {time_b:.3f}ms")
    print(f"  Examples found: {len(examples_b)}")
    print()
    
    # Detailed comparison
    print("-" * 80)
    print("DETAILED COMPARISON")
    print("-" * 80)
    
    comparison = compare_results(examples_a, examples_b)
    
    for ex in comparison['examples']:
        idx = ex['index']
        print(f"\n{'='*40}")
        print(f"Example {idx}")
        print(f"{'='*40}")
        
        # Method A result
        if ex['method_a']:
            a = ex['method_a']
            print(f"\n[Method A - Regex]")
            print(f"  Input:  {repr(a['input'][:60])}{'...' if len(a['input']) > 60 else ''}")
            print(f"  Output: {repr(a['output'][:60])}{'...' if len(a['output']) > 60 else ''}")
            print(f"  Success: {a['parse_success']}")
            if a['parse_notes']:
                print(f"  Notes: {a['parse_notes']}")
        else:
            print(f"\n[Method A - Regex] NOT FOUND")
        
        # Method B result
        if ex['method_b']:
            b = ex['method_b']
            print(f"\n[Method B - BeautifulSoup]")
            print(f"  Input:  {repr(b['input'][:60])}{'...' if len(b['input']) > 60 else ''}")
            print(f"  Output: {repr(b['output'][:60])}{'...' if len(b['output']) > 60 else ''}")
            print(f"  Success: {b['parse_success']}")
            if b['parse_notes']:
                print(f"  Notes: {b['parse_notes']}")
        else:
            print(f"\n[Method B - BeautifulSoup] NOT FOUND")
        
        # Match status
        if ex['method_a'] and ex['method_b']:
            print(f"\n  Input Match:  {'✅' if ex['input_match'] else '❌'}")
            print(f"  Output Match: {'✅' if ex['output_match'] else '❌'}")
    
    # Summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Method A (Regex):        {len(examples_a)} examples, {time_a:.3f}ms")
    print(f"Method B (BeautifulSoup): {len(examples_b)} examples, {time_b:.3f}ms")
    if time_a > 0:
        print(f"Speed ratio: Method A is {time_b/time_a:.1f}x {'faster' if time_a < time_b else 'slower'}")
    print()
    
    # Count matches
    input_matches = sum(1 for ex in comparison['examples'] if ex['input_match'])
    output_matches = sum(1 for ex in comparison['examples'] if ex['output_match'])
    total = len(comparison['examples'])
    
    print(f"Input agreement:  {input_matches}/{total}")
    print(f"Output agreement: {output_matches}/{total}")
    print()
    
    # Recommendation
    print("-" * 80)
    print("RECOMMENDATION")
    print("-" * 80)
    print()
    print("Method A (Regex/String-based):")
    print("  ✅ Already implemented in tools/docstring/formatter.py")
    print("  ✅ No additional dependencies")
    print("  ✅ Faster execution")
    print("  ✅ Handles known LeetCode HTML patterns")
    print("  ⚠️  May break on unexpected HTML structures")
    print()
    print("Method B (BeautifulSoup):")
    print("  ✅ More robust HTML parsing")
    print("  ✅ Handles malformed HTML better")
    print("  ⚠️  Requires additional dependency (beautifulsoup4)")
    print("  ⚠️  Slower execution")
    print("  ⚠️  Still needs regex for Input/Output extraction")
    print()
    print("💡 DECISION: Use Method A (Regex) for v0")
    print("   - Already battle-tested in existing codebase")
    print("   - No new dependencies")
    print("   - Can iterate if edge cases found")
    print()


def main():
    # Get problem ID from command line or use default
    problem_id = 3
    if len(sys.argv) > 1:
        try:
            problem_id = int(sys.argv[1])
        except ValueError:
            print(f"Usage: python {sys.argv[0]} [problem_id]")
            sys.exit(1)
    
    print(f"Fetching problem {problem_id}...")
    ds = LeetCodeDataSource()
    
    try:
        question = ds.get_by_frontend_id(problem_id)
    except Exception as e:
        print(f"Error fetching problem: {e}")
        sys.exit(1)
    
    if not question.Body:
        print("No HTML body found for this problem")
        sys.exit(1)
    
    print(f"Problem: {question.title}")
    print(f"HTML Body length: {len(question.Body)} chars")
    print()
    
    # Run comparison
    print_comparison(problem_id, question.Body)
    
    # Show raw HTML snippet for reference
    print("-" * 80)
    print("RAW HTML SNIPPET (first 500 chars)")
    print("-" * 80)
    print(question.Body[:500])
    print("..." if len(question.Body) > 500 else "")


if __name__ == "__main__":
    main()

