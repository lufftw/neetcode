# runner/test_runner.py
"""
Test Runner - Multi-solution testing with performance comparison.

Usage:
    python runner/test_runner.py 0001_two_sum                    # Run default solution
    python runner/test_runner.py 0023 --method heap              # Run specific solution
    python runner/test_runner.py 0023 --all                      # Run all solutions
    python runner/test_runner.py 0023 --all --benchmark          # All solutions + benchmark
"""
import subprocess
import glob
import os
import sys
import time
import argparse
import importlib.util
from typing import Optional, Dict, List, Any

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from runner.util import compare_result

PYTHON_EXE = sys.executable


def normalize_output(s: str) -> str:
    """Normalize output by removing trailing whitespace and extra newlines."""
    lines = s.strip().splitlines()
    lines = [line.rstrip() for line in lines]
    return "\n".join(lines)


def load_solution_module(problem: str):
    """
    Dynamically load solution module to get SOLUTIONS metadata and COMPARE_MODE.
    
    Returns:
        tuple: (module, solutions_meta, compare_mode)
            - module: Loaded module object
            - solutions_meta: SOLUTIONS dictionary (if exists)
            - compare_mode: Comparison mode ("exact" | "sorted" | "set")
    """
    solution_path = os.path.join("solutions", f"{problem}.py")
    if not os.path.exists(solution_path):
        return None, None, "exact"
    
    spec = importlib.util.spec_from_file_location(f"solution_{problem}", solution_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"⚠️ Error loading module: {e}")
        return None, None, "exact"
    
    # Get SOLUTIONS metadata (if exists)
    solutions_meta = getattr(module, 'SOLUTIONS', None)
    
    # Get COMPARE_MODE (default: "exact")
    compare_mode = getattr(module, 'COMPARE_MODE', 'exact')
    
    return module, solutions_meta, compare_mode


def run_one_case(problem: str, input_path: str, output_path: str, 
                 method: Optional[str] = None, benchmark: bool = False,
                 compare_mode: str = "exact", module: Any = None) -> tuple[Optional[bool], float, str, Optional[str], str]:
    """
    Run a single test case.
    
    Args:
        problem: Problem name
        input_path: Input file path
        output_path: Expected output file path
        method: Solution method name (optional)
        benchmark: Whether to measure time
        compare_mode: Comparison mode ("exact" | "sorted" | "set")
        module: Loaded solution module (for JUDGE_FUNC)
    
    Returns: 
        tuple: (passed, elapsed_ms, actual, expected, validation_mode)
            - passed: bool or None (None = skipped)
            - elapsed_ms: float
            - actual: str
            - expected: str or None
            - validation_mode: "judge" | "judge-only" | "exact" | "sorted" | "set" | "skip"
    """
    # Check if .out file exists
    has_out_file = os.path.exists(output_path)
    judge_func = getattr(module, 'JUDGE_FUNC', None) if module else None
    
    # Read input
    with open(input_path, "r", encoding="utf-8") as f:
        input_data = f.read()
    
    # Read expected output (if exists)
    if has_out_file:
        with open(output_path, "r", encoding="utf-8") as f:
            expected = f.read()
    else:
        expected = None
    
    # Handle missing .out file
    if not has_out_file and not judge_func:
        # No .out and no JUDGE_FUNC -> skip
        return None, 0.0, "", None, "skip"
    
    solution_path = os.path.join("solutions", f"{problem}.py")
    if not os.path.exists(solution_path):
        print(f"❌ Solution file not found: {solution_path}")
        return False, 0.0, "", expected, "error"
    
    # Prepare environment variables to pass method parameter
    env = os.environ.copy()
    if method:
        env['SOLUTION_METHOD'] = method
    
    start_time = time.perf_counter()
    result = subprocess.run(
        [PYTHON_EXE, solution_path],
        input=input_data,
        text=True,
        capture_output=True,
        env=env
    )
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    
    actual = result.stdout
    
    # Determine validation mode and run comparison
    if judge_func:
        # JUDGE_FUNC mode
        ok = compare_result(actual, expected, input_data, module, compare_mode)
        validation_mode = "judge" if has_out_file else "judge-only"
    else:
        # COMPARE_MODE (requires .out file)
        ok = compare_result(actual, expected, input_data, module, compare_mode)
        validation_mode = compare_mode  # "exact" / "sorted" / "set"
    
    return ok, elapsed_ms, actual, expected, validation_mode


def format_validation_label(validation_mode: str) -> str:
    """Format validation mode as a label for output."""
    return f"[{validation_mode}]"


def run_method_tests(problem: str, method_name: str, method_info: Dict[str, Any],
                     input_files: List[str], benchmark: bool = False,
                     compare_mode: str = "exact", module: Any = None) -> Dict[str, Any]:
    """Run all test cases for a specific solution method."""
    results = {
        "method": method_name,
        "display_name": method_info.get("method", method_name),
        "complexity": method_info.get("complexity", "Unknown"),
        "description": method_info.get("description", ""),
        "cases": [],
        "passed": 0,
        "total": 0,
        "skipped": 0,
        "times": [],
        "validation_summary": {}  # Track count by validation mode
    }
    
    print(f"\n📌 Method: {method_name}")
    if method_info.get("complexity"):
        print(f"   Complexity: {method_info['complexity']}")
    if method_info.get("description"):
        print(f"   Description: {method_info['description']}")
    print()
    
    for in_path in input_files:
        out_path = in_path.replace(".in", ".out")
        case_name = os.path.basename(in_path).replace(".in", "")
        
        ok, elapsed_ms, actual, expected, validation_mode = run_one_case(
            problem, in_path, out_path, method_name, benchmark, compare_mode, module
        )
        
        # Track validation mode counts
        results["validation_summary"][validation_mode] = \
            results["validation_summary"].get(validation_mode, 0) + 1
        
        # Handle skipped cases
        if validation_mode == "skip":
            results["skipped"] += 1
            print(f"   {case_name}: ⚠️ SKIP (missing .out, no JUDGE_FUNC)")
            continue
        
        results["total"] += 1
        results["times"].append(elapsed_ms)
        
        label = format_validation_label(validation_mode)
        
        if ok:
            results["passed"] += 1
            if benchmark:
                print(f"   {case_name}: ✅ PASS ({elapsed_ms:.2f}ms) {label}")
            else:
                print(f"   {case_name}: ✅ PASS {label}")
        else:
            print(f"   {case_name}: ❌ FAIL {label}")
            # Show diff for debugging
            if expected is not None:
                print(f"      Expected: {normalize_output(expected)[:100]}...")
            print(f"      Actual:   {normalize_output(actual)[:100]}...")
        
        results["cases"].append({
            "name": case_name,
            "passed": ok,
            "time_ms": elapsed_ms,
            "validation_mode": validation_mode
        })
    
    return results


def print_benchmark_summary(all_results: List[Dict[str, Any]]):
    """Print performance comparison table."""
    print("\n" + "=" * 60)
    print("📊 Performance Comparison")
    print("=" * 60)
    
    # Header
    print(f"{'Method':<20} {'Avg Time':<12} {'Complexity':<15} {'Pass Rate'}")
    print("-" * 60)
    
    for result in all_results:
        method = result["method"]
        complexity = result["complexity"]
        avg_time = sum(result["times"]) / len(result["times"]) if result["times"] else 0
        pass_rate = f"{result['passed']}/{result['total']}"
        
        print(f"{method:<20} {avg_time:>8.2f}ms   {complexity:<15} {pass_rate}")
    
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="LeetCode Test Runner - Multi-solution testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python runner/test_runner.py 0001_two_sum
  python runner/test_runner.py 0023 --method heap
  python runner/test_runner.py 0023 --all
  python runner/test_runner.py 0023 --all --benchmark
        """
    )
    parser.add_argument("problem", help="Problem name (e.g., 0001_two_sum)")
    parser.add_argument("--method", "-m", help="Specific solution method to test")
    parser.add_argument("--all", "-a", action="store_true", help="Test all solutions")
    parser.add_argument("--benchmark", "-b", action="store_true", help="Show execution time comparison")
    parser.add_argument("--tests-dir", "-t", default="tests", help="Tests directory (default: tests)")
    
    args = parser.parse_args()
    
    problem = args.problem
    tests_dir = args.tests_dir
    
    # Find test input files
    pattern = os.path.join(tests_dir, f"{problem}_*.in")
    input_files = sorted(glob.glob(pattern))
    if not input_files:
        print(f"⚠️ No test input files found: {pattern}")
        sys.exit(1)
    
    # Load solution module to get SOLUTIONS metadata and COMPARE_MODE
    module, solutions_meta, compare_mode = load_solution_module(problem)
    
    # Check if JUDGE_FUNC is defined
    has_judge_func = hasattr(module, 'JUDGE_FUNC') if module else False
    
    print(f"\n{'=' * 60}")
    print(f"🧪 Testing: {problem}")
    if has_judge_func:
        print(f"⚖️  Judge: JUDGE_FUNC (custom validation)")
    elif compare_mode != "exact":
        print(f"📋 Compare Mode: {compare_mode}")
    print(f"{'=' * 60}")
    
    # Determine which solutions to test
    if args.all and solutions_meta:
        # Test all solutions
        methods_to_test = list(solutions_meta.keys())
    elif args.method:
        # Test specific solution - verify method exists
        if solutions_meta and args.method not in solutions_meta:
            available = list(solutions_meta.keys())
            print(f"❌ Solution method '{args.method}' not found")
            print(f"   Available methods: {', '.join(available)}")
            sys.exit(1)
        methods_to_test = [args.method]
    elif solutions_meta and "default" in solutions_meta:
        # Has SOLUTIONS but no method specified, use default
        methods_to_test = ["default"]
    else:
        # No SOLUTIONS metadata, use legacy mode
        methods_to_test = [None]
    
    all_results = []
    
    for method in methods_to_test:
        if method is None:
            # Legacy mode: no method specified
            print(f"\n📌 Running default solution...")
            print()
            passed = 0
            total = 0
            skipped = 0
            times = []
            validation_summary = {}
            
            for in_path in input_files:
                out_path = in_path.replace(".in", ".out")
                case_name = os.path.basename(in_path).replace(".in", "")
                
                ok, elapsed_ms, actual, expected, validation_mode = run_one_case(
                    problem, in_path, out_path, None, args.benchmark, compare_mode, module
                )
                
                # Track validation mode counts
                validation_summary[validation_mode] = \
                    validation_summary.get(validation_mode, 0) + 1
                
                # Handle skipped cases
                if validation_mode == "skip":
                    skipped += 1
                    print(f"   {case_name}: ⚠️ SKIP (missing .out, no JUDGE_FUNC)")
                    continue
                
                total += 1
                times.append(elapsed_ms)
                
                label = format_validation_label(validation_mode)
                
                if ok:
                    passed += 1
                    if args.benchmark:
                        print(f"   {case_name}: ✅ PASS ({elapsed_ms:.2f}ms) {label}")
                    else:
                        print(f"   {case_name}: ✅ PASS {label}")
                else:
                    print(f"   {case_name}: ❌ FAIL {label}")
                    # Show diff for debugging
                    if expected is not None:
                        print(f"      Expected: {normalize_output(expected)[:100]}...")
                    print(f"      Actual:   {normalize_output(actual)[:100]}...")
            
            print(f"\nSummary: {passed} / {total} cases passed.")
            if skipped > 0:
                print(f"Skipped: {skipped} cases (missing .out)")
            
            if args.benchmark and times:
                avg_time = sum(times) / len(times)
                print(f"Average Time: {avg_time:.2f}ms")
        else:
            # Multi-solution mode
            method_info = solutions_meta.get(method, {"method": method}) if solutions_meta else {"method": method}
            result = run_method_tests(
                problem, method, method_info, input_files, args.benchmark, compare_mode, module
            )
            all_results.append(result)
            print(f"\n   Result: {result['passed']} / {result['total']} cases passed.")
    
    # Print benchmark summary for multi-solution mode
    if len(all_results) > 1 and args.benchmark:
        print_benchmark_summary(all_results)
    elif len(all_results) == 1:
        result = all_results[0]
        print(f"\nSummary: {result['passed']} / {result['total']} cases passed.")


if __name__ == "__main__":
    main()
