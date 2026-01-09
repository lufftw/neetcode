"""
Mismatch Analyzer - Generate detailed classification report.

Analyzes all problems to classify mismatch types and generate
actionable insights for the canonical format migration.
"""

import sys
import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Optional, Set
from pathlib import Path

# Setup paths
_PROJECT_ROOT = Path(__file__).parent.parent.parent
_TOOLS_PATH = _PROJECT_ROOT / "tools" / "leetcode-api"
_CODEGEN_PATH = _PROJECT_ROOT / "src" / "codegen"

if str(_TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(_TOOLS_PATH))
if str(_CODEGEN_PATH) not in sys.path:
    sys.path.insert(0, str(_CODEGEN_PATH))

try:
    from .checker import TestChecker, CheckStatus
    from .core.stub_parser import parse_code_stub
    from .core.io_schema import infer_io_schema, ParamFormat
    from .core.example_parser import parse_examples
except ImportError:
    from checker import TestChecker, CheckStatus
    from core.stub_parser import parse_code_stub
    from core.io_schema import infer_io_schema, ParamFormat
    from core.example_parser import parse_examples


class MismatchType(Enum):
    """Classification of mismatch types."""
    PARSE_FAIL_INPUT = "parse_fail_input"           # Can't parse Input from HTML
    PARSE_FAIL_OUTPUT = "parse_fail_output"         # Can't parse Output from HTML
    TYPE_UNSUPPORTED = "type_unsupported"           # LinkedList/Tree etc.
    SEPARATOR_DIFF = "separator_diff"               # Comma vs space
    NORMALIZATION_ONLY = "normalization_only"       # Whitespace/newline/case
    SERIALIZATION_DIFF = "serialization_diff"       # List format, bool, quotes
    VALUE_DIFF = "value_diff"                       # Actual value differs
    DIMENSION_FORMAT = "dimension_format"           # 2D array rows/cols prefix
    BOOLEAN_CASE = "boolean_case"                   # true vs True
    QUOTE_STYLE = "quote_style"                     # " vs '
    OUTPUT_FORMAT = "output_format"                 # Array vs space-separated


class SuggestedFix(Enum):
    """Suggested fix type."""
    AUTO_NORMALIZE = "auto_normalize"       # Can be auto-fixed
    PARSER_FIX = "parser_fix"               # Need to fix parser
    MANUAL_REVIEW = "manual_review"         # Needs human review
    FORMAT_MIGRATION = "format_migration"   # Need to migrate to canonical


@dataclass
class ProblemAnalysis:
    """Analysis result for a single problem."""
    problem_id: str
    slug: str
    
    # Source info
    has_solution: bool = False
    has_existing_tests: bool = False
    existing_test_count: int = 0
    
    # Generatability
    can_parse_examples: bool = False
    parsed_example_count: int = 0
    
    # Type info
    param_types: List[str] = field(default_factory=list)
    return_type: str = ""
    has_linkedlist: bool = False
    has_tree: bool = False
    
    # Mismatch classification
    mismatch_types: List[str] = field(default_factory=list)
    
    # Details per example
    example_details: List[Dict] = field(default_factory=list)
    
    # Suggestions
    suggested_fix: str = ""
    
    # Error info
    error: str = ""


def _detect_separator(text: str) -> str:
    """Detect which separator is used in text."""
    if not text:
        return "unknown"
    
    # Count occurrences
    comma_count = text.count(',')
    space_in_values = False
    
    # Check if spaces appear between values (not just around commas)
    import re
    # Pattern for space-separated numbers
    if re.search(r'\d\s+\d', text):
        space_in_values = True
    
    if comma_count > 0 and not space_in_values:
        return "comma"
    elif space_in_values and comma_count == 0:
        return "space"
    elif comma_count > 0 and space_in_values:
        return "mixed"
    
    return "none"


def _classify_diff(expected: str, actual: str) -> Set[MismatchType]:
    """Classify the type of difference between expected and actual."""
    types = set()
    
    if not expected or not actual:
        return types
    
    # Exact match
    if expected == actual:
        return types
    
    # Normalize for comparison
    exp_norm = expected.strip()
    act_norm = actual.strip()
    
    # Check separator difference
    exp_sep = _detect_separator(exp_norm)
    act_sep = _detect_separator(act_norm)
    if exp_sep != act_sep and exp_sep != "none" and act_sep != "none":
        types.add(MismatchType.SEPARATOR_DIFF)
    
    # Check boolean case
    if exp_norm.lower() in ('true', 'false') and act_norm.lower() in ('true', 'false'):
        if exp_norm.lower() == act_norm.lower() and exp_norm != act_norm:
            types.add(MismatchType.BOOLEAN_CASE)
    
    # Check quote style
    if ('"' in exp_norm and "'" in act_norm) or ("'" in exp_norm and '"' in act_norm):
        types.add(MismatchType.QUOTE_STYLE)
    
    # Check array format vs space-separated
    if exp_norm.startswith('[') and not act_norm.startswith('['):
        types.add(MismatchType.OUTPUT_FORMAT)
    elif not exp_norm.startswith('[') and act_norm.startswith('['):
        types.add(MismatchType.OUTPUT_FORMAT)
    
    # Check whitespace-only difference
    import re
    exp_no_ws = re.sub(r'\s+', '', exp_norm)
    act_no_ws = re.sub(r'\s+', '', act_norm)
    if exp_no_ws == act_no_ws:
        types.add(MismatchType.NORMALIZATION_ONLY)
    
    # Check serialization diff (comma spacing in arrays)
    exp_normalized = re.sub(r'\s*,\s*', ',', exp_norm)
    act_normalized = re.sub(r'\s*,\s*', ',', act_norm)
    if exp_normalized == act_normalized and exp_norm != act_norm:
        types.add(MismatchType.SERIALIZATION_DIFF)
    
    # If nothing specific found, mark as value diff
    if not types:
        types.add(MismatchType.VALUE_DIFF)
    
    return types


def analyze_problem(checker: TestChecker, problem_id: str) -> ProblemAnalysis:
    """Analyze a single problem in detail."""
    # Resolve problem
    normalized_id, slug = checker._resolve_problem(problem_id)
    
    if not normalized_id:
        return ProblemAnalysis(
            problem_id=problem_id,
            slug="",
            error="Problem not found"
        )
    
    analysis = ProblemAnalysis(problem_id=normalized_id, slug=slug)
    analysis.has_solution = True
    
    # Check existing tests
    tests_dir = checker.tests_dir
    existing_tests = list(tests_dir.glob(f"{normalized_id}_*.in"))
    analysis.has_existing_tests = len(existing_tests) > 0
    analysis.existing_test_count = len(existing_tests)
    
    # Fetch question
    question = checker._fetch_question(slug)
    if not question:
        analysis.error = "Failed to fetch question"
        return analysis
    
    # Parse stub for type info
    if question.Code:
        try:
            stub = parse_code_stub(question.Code)
            schema = infer_io_schema(stub)
            
            analysis.param_types = [f"{p.name}: {p.type_hint}" for p in schema.params]
            analysis.return_type = schema.return_type
            analysis.has_linkedlist = "ListNode" in str(schema.needs_helpers)
            analysis.has_tree = "TreeNode" in str(schema.needs_helpers)
            
            if analysis.has_linkedlist or analysis.has_tree:
                analysis.mismatch_types.append(MismatchType.TYPE_UNSUPPORTED.value)
        except Exception as e:
            analysis.error = f"Stub parse error: {e}"
    
    # Parse examples
    parse_result = parse_examples(question.Body)
    analysis.can_parse_examples = parse_result.success
    analysis.parsed_example_count = len(parse_result.examples)
    
    if not parse_result.success:
        analysis.mismatch_types.append(MismatchType.PARSE_FAIL_INPUT.value)
        analysis.suggested_fix = SuggestedFix.PARSER_FIX.value
        return analysis
    
    # Check each example
    for example in parse_result.examples:
        ex_detail = {
            "num": example.number,
            "raw_input": example.raw_input[:100] if example.raw_input else "",
            "raw_output": example.output[:100] if example.output else "",
            "parsed_inputs": example.inputs,
            "mismatch_types": [],
        }
        
        # Check if can parse input
        if not example.inputs and example.raw_input:
            ex_detail["mismatch_types"].append(MismatchType.PARSE_FAIL_INPUT.value)
            if MismatchType.PARSE_FAIL_INPUT.value not in analysis.mismatch_types:
                analysis.mismatch_types.append(MismatchType.PARSE_FAIL_INPUT.value)
        
        if not example.output:
            ex_detail["mismatch_types"].append(MismatchType.PARSE_FAIL_OUTPUT.value)
            if MismatchType.PARSE_FAIL_OUTPUT.value not in analysis.mismatch_types:
                analysis.mismatch_types.append(MismatchType.PARSE_FAIL_OUTPUT.value)
        
        # Compare with existing test if available
        in_file = tests_dir / f"{normalized_id}_{example.number}.in"
        out_file = tests_dir / f"{normalized_id}_{example.number}.out"
        
        if in_file.exists():
            actual_in = in_file.read_text(encoding="utf-8").strip()
            ex_detail["actual_in"] = actual_in[:100]
            
            # Classify input differences
            # Build expected input from parsed values
            expected_in_parts = []
            for name, value in example.inputs.items():
                # Strip brackets and quotes for comparison
                clean_value = value.strip()
                if clean_value.startswith('[') and clean_value.endswith(']'):
                    inner = clean_value[1:-1]
                    inner = inner.replace('"', '').replace("'", '')
                    expected_in_parts.append(inner)
                elif clean_value.startswith('"') or clean_value.startswith("'"):
                    expected_in_parts.append(clean_value[1:-1])
                else:
                    expected_in_parts.append(clean_value)
            
            expected_in = "\n".join(expected_in_parts)
            
            diff_types = _classify_diff(expected_in, actual_in)
            for dt in diff_types:
                if dt.value not in ex_detail["mismatch_types"]:
                    ex_detail["mismatch_types"].append(dt.value)
                if dt.value not in analysis.mismatch_types:
                    analysis.mismatch_types.append(dt.value)
        
        if out_file.exists():
            actual_out = out_file.read_text(encoding="utf-8").strip()
            ex_detail["actual_out"] = actual_out[:100]
            
            # Classify output differences
            diff_types = _classify_diff(example.output, actual_out)
            for dt in diff_types:
                if dt.value not in ex_detail["mismatch_types"]:
                    ex_detail["mismatch_types"].append(dt.value)
                if dt.value not in analysis.mismatch_types:
                    analysis.mismatch_types.append(dt.value)
        
        analysis.example_details.append(ex_detail)
    
    # Determine suggested fix
    if not analysis.mismatch_types:
        analysis.suggested_fix = "none"
    elif all(t in [MismatchType.NORMALIZATION_ONLY.value, MismatchType.SERIALIZATION_DIFF.value, 
                   MismatchType.BOOLEAN_CASE.value, MismatchType.QUOTE_STYLE.value]
             for t in analysis.mismatch_types):
        analysis.suggested_fix = SuggestedFix.AUTO_NORMALIZE.value
    elif MismatchType.PARSE_FAIL_INPUT.value in analysis.mismatch_types:
        analysis.suggested_fix = SuggestedFix.PARSER_FIX.value
    elif MismatchType.TYPE_UNSUPPORTED.value in analysis.mismatch_types:
        analysis.suggested_fix = SuggestedFix.PARSER_FIX.value
    elif MismatchType.SEPARATOR_DIFF.value in analysis.mismatch_types or \
         MismatchType.OUTPUT_FORMAT.value in analysis.mismatch_types:
        analysis.suggested_fix = SuggestedFix.FORMAT_MIGRATION.value
    else:
        analysis.suggested_fix = SuggestedFix.MANUAL_REVIEW.value
    
    return analysis


def analyze_all(limit: Optional[int] = None) -> List[ProblemAnalysis]:
    """Analyze all problems."""
    checker = TestChecker()
    analyses = []
    
    solution_files = sorted(checker.solutions_dir.glob("*.py"))
    
    count = 0
    for solution_file in solution_files:
        if solution_file.name.startswith("_"):
            continue
        
        problem_id = solution_file.stem
        print(f"Analyzing {problem_id}...", end=" ", flush=True)
        
        try:
            analysis = analyze_problem(checker, problem_id)
            analyses.append(analysis)
            print(f"[{len(analysis.mismatch_types)} issues]")
        except Exception as e:
            print(f"[ERROR: {e}]")
            analyses.append(ProblemAnalysis(
                problem_id=problem_id,
                slug="",
                error=str(e)
            ))
        
        count += 1
        if limit and count >= limit:
            break
    
    return analyses


def generate_report(analyses: List[ProblemAnalysis], format: str = "text") -> str:
    """Generate report from analyses."""
    if format == "json":
        return json.dumps([asdict(a) for a in analyses], indent=2, ensure_ascii=False)
    
    lines = []
    lines.append("=" * 80)
    lines.append("MISMATCH ANALYSIS REPORT")
    lines.append("=" * 80)
    lines.append("")
    
    # Summary statistics
    total = len(analyses)
    with_tests = sum(1 for a in analyses if a.has_existing_tests)
    can_parse = sum(1 for a in analyses if a.can_parse_examples)
    has_linkedlist = sum(1 for a in analyses if a.has_linkedlist)
    has_tree = sum(1 for a in analyses if a.has_tree)
    
    # Count mismatch types
    type_counts = {}
    for a in analyses:
        for mt in a.mismatch_types:
            type_counts[mt] = type_counts.get(mt, 0) + 1
    
    # Count suggested fixes
    fix_counts = {}
    for a in analyses:
        if a.suggested_fix:
            fix_counts[a.suggested_fix] = fix_counts.get(a.suggested_fix, 0) + 1
    
    lines.append("## SUMMARY")
    lines.append(f"Total problems: {total}")
    lines.append(f"With existing tests: {with_tests}")
    lines.append(f"Can parse examples: {can_parse}")
    lines.append(f"Has LinkedList: {has_linkedlist}")
    lines.append(f"Has Tree: {has_tree}")
    lines.append("")
    
    lines.append("## MISMATCH TYPE DISTRIBUTION")
    for mt, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        pct = count / total * 100
        lines.append(f"  {mt}: {count} ({pct:.1f}%)")
    lines.append("")
    
    lines.append("## SUGGESTED FIX DISTRIBUTION")
    for fix, count in sorted(fix_counts.items(), key=lambda x: -x[1]):
        pct = count / total * 100
        lines.append(f"  {fix}: {count} ({pct:.1f}%)")
    lines.append("")
    
    lines.append("## PROBLEM DETAILS")
    lines.append("-" * 80)
    
    for a in analyses:
        status = "OK" if not a.mismatch_types else "MISMATCH"
        lines.append(f"\n### {a.problem_id} ({a.slug}) [{status}]")
        
        if a.error:
            lines.append(f"  ERROR: {a.error}")
            continue
        
        lines.append(f"  Tests: {a.existing_test_count} existing, {a.parsed_example_count} from LeetCode")
        lines.append(f"  Types: {', '.join(a.param_types[:3])}{'...' if len(a.param_types) > 3 else ''}")
        
        if a.has_linkedlist:
            lines.append(f"  [!] Has LinkedList")
        if a.has_tree:
            lines.append(f"  [!] Has Tree")
        
        if a.mismatch_types:
            lines.append(f"  Mismatch types: {', '.join(a.mismatch_types)}")
            lines.append(f"  Suggested fix: {a.suggested_fix}")
        
        # Show first example detail
        if a.example_details:
            ex = a.example_details[0]
            lines.append(f"  Example 1 preview:")
            if ex.get("mismatch_types"):
                lines.append(f"    Issues: {', '.join(ex['mismatch_types'])}")
            if "actual_in" in ex:
                lines.append(f"    Expected IN: {ex.get('raw_input', '')[:50]}")
                lines.append(f"    Actual IN:   {ex.get('actual_in', '')[:50]}")
            if "actual_out" in ex:
                lines.append(f"    Expected OUT: {ex.get('raw_output', '')[:50]}")
                lines.append(f"    Actual OUT:   {ex.get('actual_out', '')[:50]}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    print("Running full analysis...")
    analyses = analyze_all()
    
    # Print text report
    report = generate_report(analyses, format="text")
    print(report)
    
    # Save JSON report
    json_report = generate_report(analyses, format="json")
    report_path = _PROJECT_ROOT / "docs" / "in-progress" / "new-problem-tests-autogen" / "mismatch-report.json"
    report_path.write_text(json_report, encoding="utf-8")
    print(f"\nJSON report saved to: {report_path}")


