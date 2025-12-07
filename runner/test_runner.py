# runner/test_runner.py
"""
Test Runner - Multi-solution testing with performance comparison.

Usage:
    python runner/test_runner.py 0001_two_sum                    # Run default solution
    python runner/test_runner.py 0023 --method heap              # Run specific solution
    python runner/test_runner.py 0023 --all                      # Run all solutions
    python runner/test_runner.py 0023 --all --benchmark          # All solutions + benchmark
    
Generator support:
    python runner/test_runner.py 0004 --generate 10              # tests/ + 10 generated
    python runner/test_runner.py 0004 --generate-only 10         # Only generated cases
    python runner/test_runner.py 0004 --generate 10 --seed 123   # Reproducible
    python runner/test_runner.py 0004 --generate 10 --save-failed  # Save failed inputs
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


def load_generator_module(problem: str):
    """
    Load generator module for a problem.
    
    Returns:
        module or None if generator doesn't exist
    """
    generator_path = os.path.join("generators", f"{problem}.py")
    if not os.path.exists(generator_path):
        return None
    
    spec = importlib.util.spec_from_file_location(f"generator_{problem}", generator_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"⚠️ Error loading generator: {e}")
        return None
    
    # Check if generate function exists
    if not hasattr(module, 'generate'):
        print(f"⚠️ Generator missing 'generate' function: {generator_path}")
        return None
    
    return module


def run_generated_case(problem: str, input_data: str, case_name: str,
                       method: Optional[str], benchmark: bool,
                       compare_mode: str, module: Any) -> tuple[Optional[bool], float, str, str]:
    """
    Run a single generated test case.
    
    Returns:
        tuple: (passed, elapsed_ms, actual, input_data)
    """
    judge_func = getattr(module, 'JUDGE_FUNC', None) if module else None
    
    if not judge_func:
        # Generated cases require JUDGE_FUNC
        return None, 0.0, "", input_data
    
    solution_path = os.path.join("solutions", f"{problem}.py")
    if not os.path.exists(solution_path):
        return False, 0.0, "", input_data
    
    # Prepare environment variables
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
    
    # Validate using JUDGE_FUNC (expected is None for generated cases)
    ok = compare_result(actual, None, input_data, module, compare_mode)
    
    return ok, elapsed_ms, actual, input_data


def truncate_input(input_data: str, max_length: int = 200) -> str:
    """Truncate long input for display."""
    if len(input_data) <= max_length:
        return input_data
    return input_data[:max_length] + f"... ({len(input_data)} chars total)"


def save_failed_case(problem: str, input_data: str, tests_dir: str) -> str:
    """Save a failed generated case to tests/ folder."""
    # Find next available failed case number
    n = 1
    while True:
        filename = f"{problem}_failed_{n}.in"
        filepath = os.path.join(tests_dir, filename)
        if not os.path.exists(filepath):
            break
        n += 1
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(input_data)
        if not input_data.endswith('\n'):
            f.write('\n')
    
    return filepath


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
                     compare_mode: str = "exact", module: Any = None,
                     generator_module: Any = None, generate_count: int = 0,
                     seed: Optional[int] = None, save_failed: bool = False,
                     tests_dir: str = "tests") -> Dict[str, Any]:
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
        "validation_summary": {},  # Track count by validation mode
        "gen_passed": 0,
        "gen_total": 0
    }
    
    print(f"\n📌 Method: {method_name}")
    if method_info.get("complexity"):
        print(f"   Complexity: {method_info['complexity']}")
    if method_info.get("description"):
        print(f"   Description: {method_info['description']}")
    print()
    
    # Run static tests
    if input_files:
        print("   --- tests/ (static) ---")
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
    
    # Run generated tests
    if generator_module and generate_count > 0:
        print()
        seed_info = f", seed: {seed}" if seed else ""
        print(f"   --- generators/ ({generate_count} cases{seed_info}) ---")
        
        generate_func = generator_module.generate
        gen_iter = generate_func(generate_count, seed)
        
        for i, input_data in enumerate(gen_iter, 1):
            case_name = f"gen_{i}"
            
            ok, elapsed_ms, actual, input_used = run_generated_case(
                problem, input_data, case_name, method_name,
                benchmark, compare_mode, module
            )
            
            if ok is None:
                print(f"   {case_name}: ⚠️ SKIP (requires JUDGE_FUNC)")
                continue
            
            results["gen_total"] += 1
            results["times"].append(elapsed_ms)
            
            if ok:
                results["gen_passed"] += 1
                if benchmark:
                    print(f"   {case_name}: ✅ PASS ({elapsed_ms:.2f}ms) [generated]")
                else:
                    print(f"   {case_name}: ✅ PASS [generated]")
            else:
                print(f"   {case_name}: ❌ FAIL [generated]")
                # Show input for debugging
                print(f"      ┌─ Input ─────────────────────────────────")
                for line in truncate_input(input_data).split('\n'):
                    print(f"      │ {line}")
                print(f"      ├─ Actual ────────────────────────────────")
                print(f"      │ {normalize_output(actual)[:100]}")
                print(f"      └─────────────────────────────────────────")
                
                # Save failed case if requested
                if save_failed:
                    saved_path = save_failed_case(problem, input_data, tests_dir)
                    print(f"      💾 Saved to: {saved_path}")
    
    return results


def print_benchmark_summary(all_results: List[Dict[str, Any]]):
    """Print performance comparison table."""
    print("\n" + "=" * 60)
    print("📊 Performance Comparison")
    print("=" * 60)
    
    # Check if any results have generated tests
    has_generated = any(r.get("gen_total", 0) > 0 for r in all_results)
    
    # Header
    if has_generated:
        print(f"{'Method':<20} {'Avg Time':<12} {'Complexity':<15} {'Static':<10} {'Generated'}")
        print("-" * 75)
    else:
        print(f"{'Method':<20} {'Avg Time':<12} {'Complexity':<15} {'Pass Rate'}")
        print("-" * 60)
    
    for result in all_results:
        method = result["method"]
        complexity = result["complexity"]
        avg_time = sum(result["times"]) / len(result["times"]) if result["times"] else 0
        
        static_rate = f"{result['passed']}/{result['total']}"
        gen_passed = result.get("gen_passed", 0)
        gen_total = result.get("gen_total", 0)
        
        if has_generated:
            gen_rate = f"{gen_passed}/{gen_total}" if gen_total > 0 else "-"
            print(f"{method:<20} {avg_time:>8.2f}ms   {complexity:<15} {static_rate:<10} {gen_rate}")
        else:
            print(f"{method:<20} {avg_time:>8.2f}ms   {complexity:<15} {static_rate}")
    
    print("=" * (75 if has_generated else 60))


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

Generator examples:
  python runner/test_runner.py 0004 --generate 10
  python runner/test_runner.py 0004 --generate-only 10
  python runner/test_runner.py 0004 --generate 10 --seed 12345
  python runner/test_runner.py 0004 --generate 10 --save-failed
        """
    )
    parser.add_argument("problem", help="Problem name (e.g., 0001_two_sum)")
    parser.add_argument("--method", "-m", help="Specific solution method to test")
    parser.add_argument("--all", "-a", action="store_true", help="Test all solutions")
    parser.add_argument("--benchmark", "-b", action="store_true", help="Show execution time comparison")
    parser.add_argument("--tests-dir", "-t", default="tests", help="Tests directory (default: tests)")
    
    # Generator arguments
    parser.add_argument("--generate", "-g", type=int, metavar="N",
                        help="Generate N test cases (runs with tests/)")
    parser.add_argument("--generate-only", type=int, metavar="N",
                        help="Generate N test cases (skip tests/)")
    parser.add_argument("--seed", "-s", type=int, help="Random seed for reproducibility")
    parser.add_argument("--save-failed", action="store_true",
                        help="Save failed generated cases to tests/")
    
    args = parser.parse_args()
    
    problem = args.problem
    tests_dir = args.tests_dir
    
    # Determine generator settings
    generate_count = args.generate_only or args.generate or 0
    generate_only = args.generate_only is not None
    
    # Find test input files (skip if generate-only)
    if generate_only:
        input_files = []
    else:
        pattern = os.path.join(tests_dir, f"{problem}_*.in")
        # Exclude failed cases from normal test runs
        all_files = sorted(glob.glob(pattern))
        input_files = [f for f in all_files if "_failed_" not in f]
    
    # Check if we have anything to run
    if not input_files and generate_count == 0:
        print(f"⚠️ No test input files found and no --generate specified")
        sys.exit(1)
    
    # Load solution module to get SOLUTIONS metadata and COMPARE_MODE
    module, solutions_meta, compare_mode = load_solution_module(problem)
    
    # Check if JUDGE_FUNC is defined
    has_judge_func = hasattr(module, 'JUDGE_FUNC') if module else False
    
    # Load generator module if needed
    generator_module = None
    if generate_count > 0:
        generator_module = load_generator_module(problem)
        if not generator_module:
            print(f"⚠️ No generator found: generators/{problem}.py")
            if generate_only:
                sys.exit(1)
            else:
                print(f"   Continuing with tests/ only...")
                generate_count = 0
        elif not has_judge_func:
            print(f"❌ Generator requires JUDGE_FUNC in solution file")
            sys.exit(1)
    
    print(f"\n{'=' * 60}")
    print(f"🧪 Testing: {problem}")
    if has_judge_func:
        print(f"⚖️  Judge: JUDGE_FUNC")
    elif compare_mode != "exact":
        print(f"📋 Compare Mode: {compare_mode}")
    if generator_module and generate_count > 0:
        seed_info = f", seed: {args.seed}" if args.seed else ""
        print(f"🎲 Generator: {generate_count} cases{seed_info}")
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
            gen_passed = 0
            gen_total = 0
            failed_inputs = []  # Track failed generated inputs
            
            # Run static tests from tests/
            if input_files:
                print("   --- tests/ (static) ---")
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
            
            # Run generated tests
            if generator_module and generate_count > 0:
                print()
                seed_info = f", seed: {args.seed}" if args.seed else ""
                print(f"   --- generators/ ({generate_count} cases{seed_info}) ---")
                
                generate_func = generator_module.generate
                gen_iter = generate_func(generate_count, args.seed)
                
                for i, input_data in enumerate(gen_iter, 1):
                    case_name = f"gen_{i}"
                    
                    ok, elapsed_ms, actual, input_used = run_generated_case(
                        problem, input_data, case_name, None, 
                        args.benchmark, compare_mode, module
                    )
                    
                    if ok is None:
                        print(f"   {case_name}: ⚠️ SKIP (requires JUDGE_FUNC)")
                        continue
                    
                    gen_total += 1
                    times.append(elapsed_ms)
                    
                    if ok:
                        gen_passed += 1
                        if args.benchmark:
                            print(f"   {case_name}: ✅ PASS ({elapsed_ms:.2f}ms) [generated]")
                        else:
                            print(f"   {case_name}: ✅ PASS [generated]")
                    else:
                        print(f"   {case_name}: ❌ FAIL [generated]")
                        # Show input for debugging
                        print(f"      ┌─ Input ─────────────────────────────────")
                        for line in truncate_input(input_data).split('\n'):
                            print(f"      │ {line}")
                        print(f"      ├─ Actual ────────────────────────────────")
                        print(f"      │ {normalize_output(actual)[:100]}")
                        print(f"      └─────────────────────────────────────────")
                        
                        # Save failed case if requested
                        if args.save_failed:
                            saved_path = save_failed_case(problem, input_data, tests_dir)
                            print(f"      💾 Saved to: {saved_path}")
                        
                        failed_inputs.append(input_data)
            
            # Summary
            total_all = total + gen_total
            passed_all = passed + gen_passed
            print(f"\nSummary: {passed_all} / {total_all} cases passed.")
            if input_files and gen_total > 0:
                print(f"   ├─ Static (tests/): {passed}/{total}")
                print(f"   └─ Generated: {gen_passed}/{gen_total}")
            if skipped > 0:
                print(f"Skipped: {skipped} cases (missing .out)")
            
            if args.benchmark and times:
                avg_time = sum(times) / len(times)
                print(f"Average Time: {avg_time:.2f}ms")
            
            # Reproduction hint
            if failed_inputs and args.seed:
                print(f"\n💡 To reproduce: python runner/test_runner.py {problem} --generate {generate_count} --seed {args.seed}")
        else:
            # Multi-solution mode
            method_info = solutions_meta.get(method, {"method": method}) if solutions_meta else {"method": method}
            result = run_method_tests(
                problem, method, method_info, input_files, args.benchmark, compare_mode, module,
                generator_module, generate_count, args.seed, args.save_failed, tests_dir
            )
            all_results.append(result)
            
            # Display result
            total_all = result['total'] + result['gen_total']
            passed_all = result['passed'] + result['gen_passed']
            print(f"\n   Result: {passed_all} / {total_all} cases passed.")
            if input_files and result['gen_total'] > 0:
                print(f"      ├─ Static: {result['passed']}/{result['total']}")
                print(f"      └─ Generated: {result['gen_passed']}/{result['gen_total']}")
    
    # Print benchmark summary for multi-solution mode
    if len(all_results) > 1 and args.benchmark:
        print_benchmark_summary(all_results)
    elif len(all_results) == 1:
        result = all_results[0]
        print(f"\nSummary: {result['passed']} / {result['total']} cases passed.")


if __name__ == "__main__":
    main()
