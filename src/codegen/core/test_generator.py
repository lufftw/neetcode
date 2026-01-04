"""
Test File Generator - Generate .in/.out test files from LeetCode examples.

This module extracts examples from LeetCode problem HTML and generates
test files in canonical JSON literal format.

Output Format:
    tests/{id4}_{slug}_{i}.in   - Input file (one JSON literal per line)
    tests/{id4}_{slug}_{i}.out  - Output file (single JSON literal)
"""

import json
import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pathlib import Path

from .example_parser import parse_examples, Example, ParseResult
from .io_schema import IOSchema, infer_io_schema, ParamFormat
from .stub_parser import StubInfo, parse_code_stub


@dataclass
class TestFile:
    """Represents a generated test file pair."""
    input_path: Path
    output_path: Path
    input_content: str
    output_content: str
    example_num: int
    warnings: List[str] = field(default_factory=list)
    
    def write(self, dry_run: bool = False) -> bool:
        """Write test files. Returns True if successful."""
        if dry_run:
            return True
        try:
            self.input_path.parent.mkdir(parents=True, exist_ok=True)
            self.input_path.write_text(self.input_content + '\n', encoding='utf-8')
            self.output_path.write_text(self.output_content + '\n', encoding='utf-8')
            return True
        except Exception:
            return False


@dataclass
class TestGenerationResult:
    """Result of test generation for a problem."""
    problem_id: str
    slug: str
    tests: List[TestFile] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    
    @property
    def success(self) -> bool:
        return len(self.tests) > 0 and len(self.errors) == 0
    
    @property
    def test_count(self) -> int:
        return len(self.tests)


def _parse_example_input(input_raw: str, io_schema: IOSchema) -> Dict[str, str]:
    """
    Parse raw example input into parameter values.
    
    Args:
        input_raw: Raw input string from LeetCode example
        io_schema: IO schema for the problem
        
    Returns:
        Dict mapping parameter names to their JSON literal values
    """
    result = {}
    
    # Try to match "name = value" patterns
    # Example: "nums = [2,7,11,15], target = 9"
    parts = re.split(r',\s*(?=[a-zA-Z_]\w*\s*=)', input_raw)
    
    for part in parts:
        part = part.strip()
        if '=' in part:
            match = re.match(r'([a-zA-Z_]\w*)\s*=\s*(.+)', part, re.DOTALL)
            if match:
                name = match.group(1)
                value = match.group(2).strip()
                result[name] = value
    
    return result


def _format_value_to_canonical(value: str) -> str:
    """
    Convert a value to canonical JSON literal format.
    
    Args:
        value: Raw value string (e.g., "[2,7,11,15]", "9", '"abc"')
        
    Returns:
        Canonical JSON literal string
    """
    value = value.strip()
    
    # Try to parse as Python literal and re-serialize as JSON
    import ast
    
    try:
        # Handle Python-style values
        if value.lower() == 'true':
            return 'true'
        if value.lower() == 'false':
            return 'false'
        if value.lower() == 'null' or value == 'None':
            return 'null'
        
        # Parse and re-serialize
        parsed = ast.literal_eval(value)
        return json.dumps(parsed, separators=(',', ':'))
    except (ValueError, SyntaxError):
        pass
    
    # Already valid JSON?
    try:
        parsed = json.loads(value)
        return json.dumps(parsed, separators=(',', ':'))
    except json.JSONDecodeError:
        pass
    
    # Return as-is
    return value


def generate_test_content(example: Example, io_schema: IOSchema) -> tuple:
    """
    Generate .in and .out content from a parsed example.
    
    Args:
        example: Parsed example from HTML
        io_schema: IO schema for the problem
        
    Returns:
        Tuple of (input_content, output_content, warnings)
    """
    warnings = []
    input_lines = []
    
    # Use example.inputs which is already parsed as Dict[str, str]
    parsed_input = example.inputs
    
    if not parsed_input:
        # Fallback: try to parse from raw_input
        parsed_input = _parse_example_input(example.raw_input, io_schema)
    
    if not parsed_input:
        # Still nothing - try splitting raw_input by lines
        lines = example.raw_input.strip().split('\n')
        if len(lines) == len(io_schema.params):
            for i, param in enumerate(io_schema.params):
                input_lines.append(_format_value_to_canonical(lines[i].strip()))
        else:
            warnings.append(f"Could not parse input: {example.raw_input[:50]}...")
            # Just use the raw input
            for param in io_schema.params:
                input_lines.append(example.raw_input.strip())
    else:
        # Use parsed values in parameter order
        for param in io_schema.params:
            if param.name in parsed_input:
                value = _format_value_to_canonical(parsed_input[param.name])
                input_lines.append(value)
            else:
                warnings.append(f"Missing parameter: {param.name}")
                input_lines.append("")
    
    # Format output - use example.output or raw_output
    output_value = example.output or example.raw_output
    output_content = _format_value_to_canonical(output_value)
    
    return '\n'.join(input_lines), output_content, warnings


def generate_tests_for_problem(
    problem_id: int,
    html_body: str,
    code_stub: str,
    tests_dir: Optional[Path] = None,
    force: bool = False,
) -> TestGenerationResult:
    """
    Generate test files for a LeetCode problem.
    
    Args:
        problem_id: Problem ID (will be zero-padded to 4 digits)
        html_body: Question.Body HTML content
        code_stub: Question.Code Python stub
        tests_dir: Output directory for test files
        force: Overwrite existing files
        
    Returns:
        TestGenerationResult with generated test files
    """
    # Import here to avoid circular imports
    import sys
    from pathlib import Path as PathLib
    _PROJECT_ROOT = PathLib(__file__).parent.parent.parent.parent
    
    if tests_dir is None:
        tests_dir = _PROJECT_ROOT / "tests"
    
    # Parse stub to get slug info
    stub_info = parse_code_stub(code_stub)
    io_schema = infer_io_schema(stub_info)
    
    # We need the slug from elsewhere - placeholder for now
    # The caller should provide it or we derive from the datasource
    slug = "unknown"  # Will be overridden
    
    id4 = f"{problem_id:04d}"
    result = TestGenerationResult(problem_id=id4, slug=slug)
    
    # Parse examples from HTML
    parse_result = parse_examples(html_body)
    
    if not parse_result.examples:
        result.errors.append("No examples found in HTML body")
        return result
    
    result.warnings.extend(parse_result.warnings)
    
    # Generate test files for each example
    for example in parse_result.examples:
        # Example class doesn't have 'issues' attribute, so skip this check
        
        if (not example.inputs and not example.raw_input) or (not example.output and not example.raw_output):
            result.warnings.append(f"Example {example.number}: Empty input or output")
            continue
        
        input_content, output_content, gen_warnings = generate_test_content(example, io_schema)
        result.warnings.extend(gen_warnings)
        
        # Determine file paths
        input_path = tests_dir / f"{id4}_{slug}_{example.number}.in"
        output_path = tests_dir / f"{id4}_{slug}_{example.number}.out"
        
        # Check for existing files
        if (input_path.exists() or output_path.exists()) and not force:
            result.warnings.append(f"Example {example.number}: Files exist (use --force to overwrite)")
            continue
        
        test_file = TestFile(
            input_path=input_path,
            output_path=output_path,
            input_content=input_content,
            output_content=output_content,
            example_num=example.number,
            warnings=gen_warnings,
        )
        result.tests.append(test_file)
    
    return result


def generate_tests_from_datasource(
    problem_id: int,
    tests_dir: Optional[Path] = None,
    force: bool = False,
    dry_run: bool = False,
) -> TestGenerationResult:
    """
    Generate test files using LeetCodeDataSource.
    
    Args:
        problem_id: LeetCode problem number
        tests_dir: Output directory (default: tests/)
        force: Overwrite existing files
        dry_run: Don't write files, just return what would be generated
        
    Returns:
        TestGenerationResult
    """
    import sys
    from pathlib import Path as PathLib
    _PROJECT_ROOT = PathLib(__file__).parent.parent.parent.parent
    _TOOLS_PATH = _PROJECT_ROOT / "tools" / "leetcode-api"
    
    if str(_TOOLS_PATH) not in sys.path:
        sys.path.insert(0, str(_TOOLS_PATH))
    
    from leetcode_datasource import LeetCodeDataSource
    
    if tests_dir is None:
        tests_dir = _PROJECT_ROOT / "tests"
    
    ds = LeetCodeDataSource()
    question = ds.get_by_frontend_id(problem_id)
    
    if not question:
        result = TestGenerationResult(
            problem_id=f"{problem_id:04d}",
            slug="unknown",
        )
        result.errors.append(f"Failed to fetch problem {problem_id}")
        return result
    
    # Get slug
    slug = question.titleSlug.replace("-", "_")
    
    # Parse stub and examples
    stub_info = parse_code_stub(question.Code)
    io_schema = infer_io_schema(stub_info)
    parse_result = parse_examples(question.Body)
    
    id4 = f"{problem_id:04d}"
    result = TestGenerationResult(problem_id=id4, slug=slug)
    
    if not parse_result.examples:
        result.errors.append("No examples found in HTML body")
        return result
    
    result.warnings.extend(parse_result.warnings)
    
    # Generate test files
    for example in parse_result.examples:
        # Example class doesn't have 'issues' attribute
        
        if (not example.inputs and not example.raw_input) or (not example.output and not example.raw_output):
            result.warnings.append(f"Example {example.number}: Empty input or output")
            continue
        
        input_content, output_content, gen_warnings = generate_test_content(example, io_schema)
        result.warnings.extend(gen_warnings)
        
        # Determine file paths
        input_path = tests_dir / f"{id4}_{slug}_{example.number}.in"
        output_path = tests_dir / f"{id4}_{slug}_{example.number}.out"
        
        # Check for existing files
        if (input_path.exists() or output_path.exists()) and not force:
            result.warnings.append(f"Example {example.number}: Files exist (use --force to overwrite)")
            continue
        
        test_file = TestFile(
            input_path=input_path,
            output_path=output_path,
            input_content=input_content,
            output_content=output_content,
            example_num=example.number,
            warnings=gen_warnings,
        )
        result.tests.append(test_file)
    
    # Write files if not dry run
    if not dry_run:
        for test in result.tests:
            if not test.write():
                result.errors.append(f"Failed to write Example {test.example_num}")
    
    return result


if __name__ == "__main__":
    # Test with Two Sum (force to show content even if files exist)
    result = generate_tests_from_datasource(1, force=True, dry_run=True)
    
    print(f"Problem: {result.problem_id}_{result.slug}")
    print(f"Tests generated: {result.test_count}")
    print(f"Warnings: {len(result.warnings)}")
    print(f"Errors: {len(result.errors)}")
    
    for test in result.tests:
        print(f"\n--- Example {test.example_num} ---")
        print(f"Input ({test.input_path.name}):")
        print(test.input_content)
        print(f"Output ({test.output_path.name}):")
        print(test.output_content)
    
    if result.warnings:
        print("\nWarnings:")
        for w in result.warnings:
            print(f"  - {w}")
    
    if result.errors:
        print("\nErrors:")
        for e in result.errors:
            print(f"  - {e}")

