"""
Example Parser - Extract examples from LeetCode Question.Body HTML.

This module parses the HTML problem description to extract Input/Output examples.
It uses regex-based parsing (proven faster than DOM parsing in our benchmarks).

Architecture:
    Question.Body (HTML) → ExampleParser → List[Example]

Responsibility:
    - Parse Example blocks from HTML
    - Extract Input/Output values per parameter
    - Handle various HTML formats (old and new LeetCode formats)
"""

import re
import html
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple


@dataclass
class Example:
    """
    A single parsed example from LeetCode.
    
    Attributes:
        number: Example number (1, 2, 3, ...)
        inputs: Dict mapping parameter name to raw value string
        output: Raw output value string
        explanation: Optional explanation text
        img: Optional image tag (preserved as-is)
        raw_input: Original Input: line (for debugging)
        raw_output: Original Output: line (for debugging)
    """
    number: int
    inputs: Dict[str, str] = field(default_factory=dict)
    output: str = ""
    explanation: str = ""
    img: Optional[str] = None
    raw_input: str = ""
    raw_output: str = ""
    
    def __repr__(self) -> str:
        inputs_str = ", ".join(f"{k}={v[:20]}..." if len(v) > 20 else f"{k}={v}" 
                               for k, v in self.inputs.items())
        return f"Example({self.number}: {inputs_str} → {self.output[:30]}...)"


@dataclass
class ParseResult:
    """
    Result of parsing examples from HTML.
    
    Attributes:
        examples: Successfully parsed examples
        warnings: List of warning messages for partial failures
        success: True if at least one example was parsed
    """
    examples: List[Example] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    success: bool = True
    
    def __repr__(self) -> str:
        return f"ParseResult({len(self.examples)} examples, {len(self.warnings)} warnings)"


def _extract_text_from_html(html_content: str) -> str:
    """
    Extract plain text from HTML, preserving structure.
    
    Reuses logic from tools/docstring/formatter.py.
    """
    if not html_content:
        return ""
    
    # Decode HTML entities
    text = html.unescape(html_content)
    
    # Remove script and style tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Replace block elements with newlines
    text = re.sub(r'</(p|div|h[1-6]|pre|br)[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<(p|div|h[1-6]|pre)[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    
    # Remove all remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Clean up whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    
    return text.strip()


def _parse_input_line(input_text: str) -> Dict[str, str]:
    """
    Parse Input: line into parameter name-value pairs.
    
    Handles formats like:
        - "nums = [2,7,11,15], target = 9"
        - "l1 = [2,4,3], l2 = [5,6,4]"
        - "n = 4"
        - "s = \"abcabcbb\""
        - "board = [[\"A\",\"B\"],[\"C\",\"D\"]], word = \"ABCD\""
    
    Args:
        input_text: The text after "Input:" 
        
    Returns:
        Dict mapping parameter names to value strings
    """
    result = {}
    input_text = input_text.strip()
    
    if not input_text:
        return result
    
    # Pattern: name = value (where value can be complex like [[...]])
    # We need to carefully match brackets and quotes
    
    current_pos = 0
    while current_pos < len(input_text):
        # Find parameter name
        name_match = re.match(r'\s*(\w+)\s*=\s*', input_text[current_pos:])
        if not name_match:
            break
        
        param_name = name_match.group(1)
        value_start = current_pos + name_match.end()
        
        # Find value end - handle nested brackets and quotes
        value_end = _find_value_end(input_text, value_start)
        value = input_text[value_start:value_end].strip()
        
        result[param_name] = value
        
        # Move past the value and any comma
        current_pos = value_end
        if current_pos < len(input_text) and input_text[current_pos] == ',':
            current_pos += 1
    
    return result


def _find_value_end(text: str, start: int) -> int:
    """
    Find where a value ends in an input string.
    
    Handles nested brackets [], quotes "", and escapes.
    """
    pos = start
    bracket_depth = 0
    in_string = False
    string_char = None
    
    while pos < len(text):
        char = text[pos]
        
        # Handle escape sequences in strings
        if in_string and char == '\\' and pos + 1 < len(text):
            pos += 2
            continue
        
        # Handle string boundaries
        if char in ('"', "'") and not in_string:
            in_string = True
            string_char = char
        elif char == string_char and in_string:
            in_string = False
            string_char = None
        
        # Handle brackets (only outside strings)
        elif not in_string:
            if char == '[':
                bracket_depth += 1
            elif char == ']':
                bracket_depth -= 1
            elif char == ',' and bracket_depth == 0:
                # Found parameter separator
                return pos
        
        pos += 1
    
    return pos


def _extract_examples_from_html(html_body: str) -> List[dict]:
    """
    Extract all examples from HTML Body.
    
    Reuses the regex-based approach from tools/docstring/formatter.py
    which was benchmarked to be 50-110x faster than BeautifulSoup.
    
    Handles two HTML formats:
    1. New format: <p><strong class="example">Example N:</strong></p><pre>...</pre>
    2. Old format: <p><strong>Example N:</strong></p><p>Input:...</p>
    """
    if not html_body:
        return []
    
    examples = []
    
    # Pattern to find Example blocks
    example_pattern = r'<p>\s*<strong[^>]*>\s*Example\s*(\d+):\s*</strong>\s*</p>(.*?)(?=<p>\s*<strong[^>]*>\s*(?:Example\s*\d+:|Constraints?:|Follow[\s-]?up|Note:)|<p>\s*&nbsp;\s*</p>\s*<p>\s*<strong>Constraints|<strong>Follow-up|$)'
    matches = re.findall(example_pattern, html_body, re.DOTALL | re.IGNORECASE)
    
    for num, content in matches:
        example = {'number': int(num), 'img': None, 'input': '', 'output': '', 'explanation': ''}
        
        # Extract <img> tag if present
        img_match = re.search(r'(<img[^>]*>)', content, re.IGNORECASE)
        if img_match:
            example['img'] = img_match.group(1)
        
        # Check if content is in <pre> block (new LeetCode format)
        pre_match = re.search(r'<pre[^>]*>(.*?)</pre>', content, re.DOTALL | re.IGNORECASE)
        if pre_match:
            pre_content = pre_match.group(1)
            
            # Extract Input from <pre> block
            input_match = re.search(r'<strong>Input:</strong>\s*(.*?)(?=\n<strong>|$)', pre_content, re.DOTALL | re.IGNORECASE)
            if input_match:
                input_text = re.sub(r'<[^>]+>', '', input_match.group(1))
                example['input'] = html.unescape(input_text).strip()
            
            # Extract Output from <pre> block
            output_match = re.search(r'<strong>Output:</strong>\s*(.*?)(?=\n<strong>|$)', pre_content, re.DOTALL | re.IGNORECASE)
            if output_match:
                output_text = re.sub(r'<[^>]+>', '', output_match.group(1))
                example['output'] = html.unescape(output_text).strip()
            
            # Extract Explanation from <pre> block
            expl_match = re.search(r'<strong>Explanation:</strong>\s*(.*?)$', pre_content, re.DOTALL | re.IGNORECASE)
            if expl_match:
                expl_text = re.sub(r'<[^>]+>', '', expl_match.group(1))
                example['explanation'] = html.unescape(expl_text).strip()
        else:
            # Old format
            input_match = re.search(r'<strong[^>]*>\s*Input:\s*</strong>\s*(.*?)(?=<strong|$)', content, re.DOTALL | re.IGNORECASE)
            if input_match:
                input_text = re.sub(r'<[^>]+>', '', input_match.group(1))
                example['input'] = html.unescape(input_text).strip()
            
            output_match = re.search(r'<strong[^>]*>\s*Output:\s*</strong>\s*(.*?)(?=<strong|$)', content, re.DOTALL | re.IGNORECASE)
            if output_match:
                output_text = re.sub(r'<[^>]+>', '', output_match.group(1))
                example['output'] = html.unescape(output_text).strip()
            
            expl_match = re.search(r'<strong[^>]*>\s*Explanation:\s*</strong>\s*(.*?)(?=<p>|<strong>|$)', content, re.DOTALL | re.IGNORECASE)
            if expl_match:
                expl_text = re.sub(r'<[^>]+>', '', expl_match.group(1))
                example['explanation'] = html.unescape(expl_text).strip()
        
        examples.append(example)
    
    return examples


def parse_examples(html_body: str) -> ParseResult:
    """
    Parse examples from LeetCode Question.Body HTML.
    
    This is the main entry point for example parsing.
    
    Args:
        html_body: HTML content from Question.Body
        
    Returns:
        ParseResult with parsed examples and any warnings
        
    Example:
        >>> result = parse_examples(question.Body)
        >>> for ex in result.examples:
        ...     print(f"Example {ex.number}: {ex.inputs} → {ex.output}")
    """
    result = ParseResult()
    
    if not html_body:
        result.success = False
        result.warnings.append("Empty HTML body")
        return result
    
    # Extract raw examples from HTML
    raw_examples = _extract_examples_from_html(html_body)
    
    if not raw_examples:
        result.success = False
        result.warnings.append("No examples found in HTML")
        return result
    
    # Parse each example
    for raw in raw_examples:
        try:
            # Parse input parameters
            inputs = _parse_input_line(raw['input'])
            
            if not inputs and raw['input']:
                # Couldn't parse, but there was input text
                result.warnings.append(
                    f"Example {raw['number']}: Could not parse Input: '{raw['input'][:50]}...'"
                )
            
            if not raw['output']:
                result.warnings.append(f"Example {raw['number']}: Missing Output")
            
            example = Example(
                number=raw['number'],
                inputs=inputs,
                output=raw['output'],
                explanation=raw['explanation'],
                img=raw['img'],
                raw_input=raw['input'],
                raw_output=raw['output'],
            )
            result.examples.append(example)
            
        except Exception as e:
            result.warnings.append(f"Example {raw['number']}: Parse error - {e}")
    
    result.success = len(result.examples) > 0
    return result


def format_example_for_test(
    example: Example,
    param_names: List[str],
    separator: str = ","
) -> Tuple[str, str]:
    """
    Format a parsed example into .in and .out file content.
    
    This converts the parsed Example into the test file format.
    The actual formatting logic depends on the IOSchema, but this
    provides a simple default conversion.
    
    Args:
        example: Parsed Example object
        param_names: List of parameter names in order (from signature)
        separator: Separator to use for arrays
        
    Returns:
        Tuple of (in_content, out_content) strings
        
    Example:
        >>> in_content, out_content = format_example_for_test(
        ...     example, ["nums", "target"], separator=","
        ... )
    """
    in_lines = []
    
    for name in param_names:
        value = example.inputs.get(name, "")
        
        # Convert LeetCode format to test format
        # Remove surrounding quotes for strings
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        # Remove brackets for arrays and join with separator
        elif value.startswith('[') and value.endswith(']'):
            inner = value[1:-1]
            # Handle nested arrays (2D)
            if '],[' in inner or inner.startswith('['):
                # Keep as-is for now, complex handling in io_schema
                pass
            else:
                # Simple 1D array - normalize separator
                inner = inner.replace('"', '').replace("'", '')
                inner = re.sub(r'\s*,\s*', separator, inner)
                value = inner
        
        in_lines.append(value)
    
    in_content = "\n".join(in_lines)
    out_content = example.output
    
    return in_content, out_content


if __name__ == "__main__":
    # Demo - requires leetcode-api
    import sys
    sys.path.insert(0, "tools/leetcode-api")
    
    try:
        from question_api import get_question
        
        test_slugs = ["two-sum", "add-two-numbers", "word-search"]
        
        for slug in test_slugs:
            print(f"\n{'='*60}")
            print(f"Testing: {slug}")
            print('='*60)
            
            q = get_question(slug)
            if not q:
                print(f"Failed to fetch {slug}")
                continue
            
            result = parse_examples(q.Body)
            print(f"Parse result: {result}")
            
            for ex in result.examples:
                print(f"\n  Example {ex.number}:")
                print(f"    Inputs: {ex.inputs}")
                print(f"    Output: {ex.output}")
            
            if result.warnings:
                print(f"\n  Warnings:")
                for w in result.warnings:
                    print(f"    - {w}")
                    
    except ImportError as e:
        print(f"Demo requires leetcode-api: {e}")


