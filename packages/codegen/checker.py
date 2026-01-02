"""
Test Consistency Checker - Verify Example ↔ Test file consistency.

This module provides two types of checks:
1. Generatability: Can we parse examples and generate test files?
2. Consistency: Do existing test files match the parsed examples?

Usage:
    python -m codegen check 3              # Check single problem
    python -m codegen check --all          # Check all problems
    python -m codegen check --report       # Generate report
"""

import os
import sys
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple
from pathlib import Path

# Setup paths
_PROJECT_ROOT = Path(__file__).parent.parent.parent
_TOOLS_PATH = _PROJECT_ROOT / "tools" / "leetcode-api"
_CODEGEN_PATH = _PROJECT_ROOT / "packages" / "codegen"

if str(_TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(_TOOLS_PATH))
if str(_CODEGEN_PATH) not in sys.path:
    sys.path.insert(0, str(_CODEGEN_PATH))

# Support both relative and absolute imports
try:
    from .core.stub_parser import parse_code_stub, StubInfo
    from .core.io_schema import infer_io_schema, IOSchema, ParamFormat, format_value_for_test
    from .core.example_parser import parse_examples, Example, ParseResult
except ImportError:
    from core.stub_parser import parse_code_stub, StubInfo
    from core.io_schema import infer_io_schema, IOSchema, ParamFormat, format_value_for_test
    from core.example_parser import parse_examples, Example, ParseResult


class CheckStatus(Enum):
    """Status of a check operation."""
    OK = "ok"                       # Everything matches
    MATCH = "match"                 # Test files match examples
    MISMATCH = "mismatch"           # Test files differ from examples
    MISMATCH_WHITESPACE = "mismatch_whitespace"  # Only whitespace differs
    MISSING_TESTS = "missing_tests"  # No test files exist but examples available
    MISSING_EXAMPLES = "missing_examples"  # Test files exist but can't parse examples
    PARSE_ERROR = "parse_error"     # Failed to parse examples
    FETCH_ERROR = "fetch_error"     # Failed to fetch question data
    NOT_FOUND = "not_found"         # Problem not found


@dataclass
class ExampleCheck:
    """Result of checking a single example."""
    example_num: int
    status: CheckStatus
    expected_in: str = ""
    expected_out: str = ""
    actual_in: str = ""
    actual_out: str = ""
    diff_details: str = ""


@dataclass
class CheckResult:
    """
    Complete result of checking a problem.
    
    Attributes:
        problem_id: Problem ID (e.g., "0001", "3")
        slug: Problem slug (e.g., "two-sum")
        status: Overall status
        examples: Individual example check results
        generatable: Can examples be converted to test format?
        consistent: Do existing tests match examples?
        warnings: List of warning messages
        error: Error message if status is error
    """
    problem_id: str
    slug: str = ""
    status: CheckStatus = CheckStatus.OK
    examples: List[ExampleCheck] = field(default_factory=list)
    generatable: bool = False
    consistent: bool = False
    warnings: List[str] = field(default_factory=list)
    error: str = ""
    
    def __repr__(self) -> str:
        return f"CheckResult({self.problem_id}: {self.status.value}, {len(self.examples)} examples)"
    
    def summary(self) -> str:
        """Generate a one-line summary."""
        status_icon = {
            CheckStatus.OK: "[OK]",
            CheckStatus.MATCH: "[OK]",
            CheckStatus.MISMATCH: "[MISMATCH]",
            CheckStatus.MISMATCH_WHITESPACE: "[WHITESPACE]",
            CheckStatus.MISSING_TESTS: "[MISSING]",
            CheckStatus.MISSING_EXAMPLES: "[NO_EXAMPLES]",
            CheckStatus.PARSE_ERROR: "[PARSE_ERR]",
            CheckStatus.FETCH_ERROR: "[FETCH_ERR]",
            CheckStatus.NOT_FOUND: "[NOT_FOUND]",
        }
        icon = status_icon.get(self.status, "[?]")
        return f"{icon} {self.problem_id} ({self.slug}): {self.status.value}"


class TestChecker:
    """
    Checker for test file consistency.
    
    Provides methods to check:
    1. Whether examples can be parsed and converted to test format
    2. Whether existing test files match the parsed examples
    """
    
    def __init__(
        self,
        solutions_dir: Optional[Path] = None,
        tests_dir: Optional[Path] = None,
    ):
        """
        Initialize the checker.
        
        Args:
            solutions_dir: Path to solutions directory
            tests_dir: Path to tests directory
        """
        self.solutions_dir = solutions_dir or (_PROJECT_ROOT / "solutions")
        self.tests_dir = tests_dir or (_PROJECT_ROOT / "tests")
    
    def check_problem(self, problem_id: str) -> CheckResult:
        """
        Check a single problem for test consistency.
        
        Args:
            problem_id: Problem ID (e.g., "3", "0003", "0001_two_sum")
            
        Returns:
            CheckResult with detailed check information
        """
        # Normalize problem ID
        normalized_id, slug = self._resolve_problem(problem_id)
        
        if not normalized_id:
            return CheckResult(
                problem_id=problem_id,
                status=CheckStatus.NOT_FOUND,
                error=f"Problem not found: {problem_id}",
            )
        
        result = CheckResult(problem_id=normalized_id, slug=slug)
        
        # Step 1: Fetch question data
        question = self._fetch_question(slug)
        if not question:
            result.status = CheckStatus.FETCH_ERROR
            result.error = f"Failed to fetch question data for: {slug}"
            return result
        
        # Step 2: Parse code stub to get signature
        stub_info = self._parse_stub(question.Code)
        if not stub_info:
            result.warnings.append("Could not parse code stub")
        
        io_schema = infer_io_schema(stub_info) if stub_info else None
        
        # Step 3: Parse examples from HTML
        parse_result = parse_examples(question.Body)
        
        if not parse_result.success:
            result.status = CheckStatus.PARSE_ERROR
            result.warnings.extend(parse_result.warnings)
            result.error = "Failed to parse examples from HTML"
            return result
        
        result.warnings.extend(parse_result.warnings)
        result.generatable = len(parse_result.examples) > 0
        
        # Step 4: Check each example against existing test files
        param_names = [p[0] for p in stub_info.params] if stub_info else []
        
        all_match = True
        any_tests_exist = False
        
        for example in parse_result.examples:
            ex_check = self._check_example(
                normalized_id, example, param_names, io_schema
            )
            result.examples.append(ex_check)
            
            if ex_check.status == CheckStatus.MATCH:
                any_tests_exist = True
            elif ex_check.status == CheckStatus.MISMATCH:
                all_match = False
                any_tests_exist = True
            elif ex_check.status == CheckStatus.MISMATCH_WHITESPACE:
                any_tests_exist = True
            elif ex_check.status == CheckStatus.MISSING_TESTS:
                all_match = False
        
        # Determine overall status
        if not any_tests_exist:
            result.status = CheckStatus.MISSING_TESTS
            result.consistent = False
        elif all_match:
            result.status = CheckStatus.MATCH
            result.consistent = True
        else:
            result.status = CheckStatus.MISMATCH
            result.consistent = False
        
        return result
    
    def check_generatable(self, problem_id: str) -> CheckResult:
        """
        Check only if examples can be parsed and converted.
        
        This is a lighter check that doesn't compare against existing files.
        """
        normalized_id, slug = self._resolve_problem(problem_id)
        
        if not normalized_id:
            return CheckResult(
                problem_id=problem_id,
                status=CheckStatus.NOT_FOUND,
                error=f"Problem not found: {problem_id}",
            )
        
        result = CheckResult(problem_id=normalized_id, slug=slug)
        
        question = self._fetch_question(slug)
        if not question:
            result.status = CheckStatus.FETCH_ERROR
            result.error = f"Failed to fetch question data"
            return result
        
        parse_result = parse_examples(question.Body)
        result.warnings.extend(parse_result.warnings)
        
        if parse_result.success and parse_result.examples:
            result.status = CheckStatus.OK
            result.generatable = True
            
            # Add basic info for each example
            for ex in parse_result.examples:
                result.examples.append(ExampleCheck(
                    example_num=ex.number,
                    status=CheckStatus.OK,
                    expected_in=ex.raw_input[:100],
                    expected_out=ex.output[:100],
                ))
        else:
            result.status = CheckStatus.PARSE_ERROR
            result.generatable = False
            result.error = "Could not parse examples"
        
        return result
    
    def check_all(self, limit: Optional[int] = None) -> List[CheckResult]:
        """
        Check all problems in the solutions directory.
        
        Args:
            limit: Maximum number of problems to check
            
        Returns:
            List of CheckResult for each problem
        """
        results = []
        
        # Find all solution files
        solution_files = sorted(self.solutions_dir.glob("*.py"))
        
        count = 0
        for solution_file in solution_files:
            if solution_file.name.startswith("_"):
                continue
            
            problem_id = solution_file.stem
            result = self.check_problem(problem_id)
            results.append(result)
            
            count += 1
            if limit and count >= limit:
                break
        
        return results
    
    def _resolve_problem(self, problem_id: str) -> Tuple[Optional[str], str]:
        """
        Resolve problem ID to normalized ID and slug.
        
        Args:
            problem_id: Raw problem ID (e.g., "3", "0003", "0001_two_sum")
            
        Returns:
            Tuple of (normalized_id, slug) or (None, "") if not found
        """
        # If it's a full filename, extract the ID
        if "_" in problem_id:
            # Already in format like "0001_two_sum"
            parts = problem_id.split("_", 1)
            num_part = parts[0].lstrip("0") or "0"
            slug = parts[1].replace("_", "-") if len(parts) > 1 else ""
            
            # Verify the file exists
            possible_files = list(self.solutions_dir.glob(f"{problem_id}*.py"))
            if possible_files:
                return problem_id, slug
        
        # Try to find by numeric ID
        try:
            num_id = int(problem_id)
            padded_id = f"{num_id:04d}"
            
            # Find matching solution file
            possible_files = list(self.solutions_dir.glob(f"{padded_id}_*.py"))
            if possible_files:
                filename = possible_files[0].stem
                slug = filename.split("_", 1)[1].replace("_", "-") if "_" in filename else ""
                return filename, slug
        except ValueError:
            pass
        
        return None, ""
    
    def _fetch_question(self, slug: str):
        """Fetch question data from cache/API."""
        try:
            from question_api import get_question
            return get_question(slug)
        except ImportError:
            return None
        except Exception:
            return None
    
    def _parse_stub(self, code: str) -> Optional[StubInfo]:
        """Parse code stub to get signature info."""
        if not code:
            return None
        try:
            return parse_code_stub(code)
        except Exception:
            return None
    
    def _check_example(
        self,
        problem_id: str,
        example: Example,
        param_names: List[str],
        io_schema: Optional[IOSchema],
    ) -> ExampleCheck:
        """
        Check a single example against existing test files.
        """
        # Build expected .in content
        expected_in_lines = []
        for name in param_names:
            value = example.inputs.get(name, "")
            # Convert from LeetCode format to test format
            formatted = self._format_value(value, name, io_schema)
            expected_in_lines.append(formatted)
        
        expected_in = "\n".join(expected_in_lines)
        expected_out = example.output
        
        # Read actual test files
        in_file = self.tests_dir / f"{problem_id}_{example.number}.in"
        out_file = self.tests_dir / f"{problem_id}_{example.number}.out"
        
        if not in_file.exists():
            return ExampleCheck(
                example_num=example.number,
                status=CheckStatus.MISSING_TESTS,
                expected_in=expected_in,
                expected_out=expected_out,
            )
        
        actual_in = in_file.read_text(encoding="utf-8").strip()
        actual_out = out_file.read_text(encoding="utf-8").strip() if out_file.exists() else ""
        
        # Compare
        in_match = self._compare_content(expected_in, actual_in)
        out_match = self._compare_content(expected_out, actual_out)
        
        if in_match == "exact" and out_match == "exact":
            status = CheckStatus.MATCH
        elif in_match in ("exact", "whitespace") and out_match in ("exact", "whitespace"):
            status = CheckStatus.MISMATCH_WHITESPACE
        else:
            status = CheckStatus.MISMATCH
        
        diff_details = ""
        if status == CheckStatus.MISMATCH:
            diff_details = self._generate_diff(expected_in, actual_in, expected_out, actual_out)
        
        return ExampleCheck(
            example_num=example.number,
            status=status,
            expected_in=expected_in,
            expected_out=expected_out,
            actual_in=actual_in,
            actual_out=actual_out,
            diff_details=diff_details,
        )
    
    def _format_value(
        self,
        value: str,
        param_name: str,
        io_schema: Optional[IOSchema],
    ) -> str:
        """Format a value from LeetCode format to test format."""
        if not value:
            return ""
        
        value = value.strip()
        
        # Get param schema if available
        param_schema = None
        if io_schema:
            for p in io_schema.params:
                if p.name == param_name:
                    param_schema = p
                    break
        
        # Use schema-based formatting if available
        if param_schema:
            return format_value_for_test(value, param_schema, separator=",")
        
        # Fallback: simple conversion
        # Remove quotes from strings
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
        
        # Remove brackets from arrays
        if value.startswith('[') and value.endswith(']'):
            inner = value[1:-1]
            # Handle nested arrays separately
            if '],[' not in inner and not inner.startswith('['):
                # Simple 1D array - remove quotes and spaces
                inner = inner.replace('"', '').replace("'", '')
                inner = re.sub(r'\s*,\s*', ',', inner)
                return inner
        
        return value
    
    def _compare_content(self, expected: str, actual: str) -> str:
        """
        Compare expected and actual content.
        
        Returns:
            "exact" - exactly equal
            "whitespace" - equal after normalizing whitespace
            "different" - content differs
        """
        if expected == actual:
            return "exact"
        
        # Normalize whitespace (including spaces around commas in arrays)
        def normalize(s: str) -> str:
            s = s.strip()
            # Remove spaces around commas: [0, 1] -> [0,1]
            s = re.sub(r'\s*,\s*', ',', s)
            # Normalize other whitespace
            s = re.sub(r'\s+', ' ', s)
            return s
        
        expected_norm = normalize(expected)
        actual_norm = normalize(actual)
        
        if expected_norm == actual_norm:
            return "whitespace"
        
        return "different"
    
    def _generate_diff(
        self,
        expected_in: str,
        actual_in: str,
        expected_out: str,
        actual_out: str,
    ) -> str:
        """Generate a human-readable diff summary."""
        lines = []
        
        if expected_in != actual_in:
            lines.append(f"Input differs:")
            lines.append(f"  Expected: {expected_in[:80]}{'...' if len(expected_in) > 80 else ''}")
            lines.append(f"  Actual:   {actual_in[:80]}{'...' if len(actual_in) > 80 else ''}")
        
        if expected_out != actual_out:
            lines.append(f"Output differs:")
            lines.append(f"  Expected: {expected_out[:80]}{'...' if len(expected_out) > 80 else ''}")
            lines.append(f"  Actual:   {actual_out[:80]}{'...' if len(actual_out) > 80 else ''}")
        
        return "\n".join(lines)


def generate_report(results: List[CheckResult], format: str = "text") -> str:
    """
    Generate a report from check results.
    
    Args:
        results: List of CheckResult objects
        format: Output format ("text", "markdown", "json")
        
    Returns:
        Formatted report string
    """
    if format == "json":
        import json
        data = []
        for r in results:
            data.append({
                "problem_id": r.problem_id,
                "slug": r.slug,
                "status": r.status.value,
                "generatable": r.generatable,
                "consistent": r.consistent,
                "examples": len(r.examples),
                "warnings": r.warnings,
                "error": r.error,
            })
        return json.dumps(data, indent=2)
    
    # Text/Markdown format
    lines = []
    
    # Summary
    total = len(results)
    ok = sum(1 for r in results if r.status in (CheckStatus.OK, CheckStatus.MATCH))
    mismatch = sum(1 for r in results if r.status == CheckStatus.MISMATCH)
    missing = sum(1 for r in results if r.status == CheckStatus.MISSING_TESTS)
    errors = sum(1 for r in results if r.status in (CheckStatus.PARSE_ERROR, CheckStatus.FETCH_ERROR))
    
    lines.append(f"# Test Consistency Report")
    lines.append(f"")
    lines.append(f"Total: {total} problems")
    lines.append(f"  [OK] Match: {ok}")
    lines.append(f"  [X]  Mismatch: {mismatch}")
    lines.append(f"  [?]  Missing tests: {missing}")
    lines.append(f"  [!]  Errors: {errors}")
    lines.append(f"")
    
    # Details
    lines.append(f"## Details")
    lines.append(f"")
    
    for r in results:
        lines.append(r.summary())
        if r.warnings:
            for w in r.warnings:
                lines.append(f"    Warning: {w}")
        if r.error:
            lines.append(f"    Error: {r.error}")
        
        # Show mismatches
        for ex in r.examples:
            if ex.status == CheckStatus.MISMATCH:
                lines.append(f"    Example {ex.example_num}: MISMATCH")
                if ex.diff_details:
                    for line in ex.diff_details.split("\n"):
                        lines.append(f"      {line}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Demo
    checker = TestChecker()
    
    # Check a single problem
    result = checker.check_problem("1")
    print(f"\n{result.summary()}")
    print(f"Generatable: {result.generatable}")
    print(f"Consistent: {result.consistent}")
    
    for ex in result.examples:
        print(f"  Example {ex.example_num}: {ex.status.value}")
    
    if result.warnings:
        print(f"Warnings:")
        for w in result.warnings:
            print(f"  - {w}")

