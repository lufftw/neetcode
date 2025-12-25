# runner/test_runner.py
"""
Test Runner - Multi-solution testing with performance comparison.

📚 Documentation:
    - Quick Reference: runner/README.md
    - Complete Spec: docs/runner/README.md

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

Complexity estimation:
    python runner/test_runner.py 0004 --estimate                 # Estimate time complexity
    (requires generate_for_complexity(n) function in generator)
"""
import glob
import os
import re
import sys
import argparse
from typing import Optional

# Enable UTF-8 output on Windows for emoji support
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import from submodules
from runner.module_loader import load_solution_module, load_generator_module
from runner.executor import run_one_case, run_generated_case, PYTHON_EXE
from runner.reporter import (
    truncate_input, 
    format_validation_label, 
    save_failed_case, 
    print_benchmark_summary,
    print_visual_benchmark,
    run_method_tests
)
from runner.compare import normalize_output
from runner.solution_parser import build_method_mapping

# Re-export for backward compatibility
__all__ = [
    'normalize_output',
    'load_solution_module',
    'load_generator_module',
    'run_one_case',
    'run_generated_case',
    'truncate_input',
    'format_validation_label',
    'save_failed_case',
    'print_benchmark_summary',
    'print_visual_benchmark',
    'run_method_tests',
    'build_method_mapping',
    'PYTHON_EXE',
    'main',
]


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
    
    # Complexity estimation
    parser.add_argument("--estimate", "-e", action="store_true",
                        help="Estimate time complexity (requires generate_for_complexity in generator)")
    
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
    
    # If solution file not found with given problem name, try to extract full name from test files
    if input_files:
        # Try to load solution module with given problem name
        module, solutions_meta, compare_mode = load_solution_module(problem)
        
        # If not found, extract full problem name from first test file
        if module is None:
            first_test_file = os.path.basename(input_files[0])
            # Extract problem name: remove _<number>.in suffix
            # Pattern: 0215_kth_largest_element_in_an_array_1.in -> 0215_kth_largest_element_in_an_array
            match = re.match(r'^(.+?)_\d+\.in$', first_test_file)
            if match:
                full_problem_name = match.group(1)
                if full_problem_name != problem:
                    print(f"💡 Problem name '{problem}' not found, trying '{full_problem_name}'...")
                    problem = full_problem_name
                    module, solutions_meta, compare_mode = load_solution_module(problem)
    else:
        # No test files, just try to load with given problem name
        module, solutions_meta, compare_mode = load_solution_module(problem)
    
    # Check if JUDGE_FUNC is defined
    has_judge_func = hasattr(module, 'JUDGE_FUNC') if module else False
    
    # Build approach mapping from class comments
    approach_mapping = None
    if solutions_meta:
        solution_path = os.path.join("solutions", f"{problem}.py")
        approach_mapping = build_method_mapping(solution_path, solutions_meta)
    
    # Load generator module if needed (for generation or complexity estimation)
    generator_module = None
    if generate_count > 0 or args.estimate:
        generator_module = load_generator_module(problem)
        if not generator_module:
            if generate_count > 0:
                print(f"⚠️ No generator found: generators/{problem}.py")
                if generate_only:
                    sys.exit(1)
                else:
                    print(f"   Continuing with tests/ only...")
                    generate_count = 0
        elif generate_count > 0 and not has_judge_func:
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
    if args.estimate:
        print(f"📈 Complexity estimation: requested")
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
            
            # Get approach info for this method
            approach_info = None
            if approach_mapping and method in approach_mapping:
                approach_info = approach_mapping[method]
            
            result = run_method_tests(
                problem, method, method_info, input_files, args.benchmark, compare_mode, module,
                generator_module, generate_count, args.seed, args.save_failed, tests_dir,
                approach_info=approach_info
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
        print_benchmark_summary(all_results, problem_name=problem, approach_mapping=approach_mapping)
    elif len(all_results) == 1:
        result = all_results[0]
        print(f"\nSummary: {result['passed']} / {result['total']} cases passed.")
    
    # Complexity estimation (separate from random test generation)
    if args.estimate:
        from runner.complexity_estimator import ComplexityEstimator
        
        print(f"\n{'=' * 60}")
        print(f"📈 Complexity Estimation")
        print(f"{'=' * 60}")
        
        if not ComplexityEstimator.is_available():
            print(f"❌ big-O package not installed")
            print(f"   Install with: pip install big-O")
        elif not ComplexityEstimator.can_estimate(generator_module):
            reason = ComplexityEstimator.get_unavailable_reason(generator_module)
            print(f"❌ Cannot estimate complexity: {reason}")
            print(f"\n   To enable complexity estimation, add to your generator:")
            print(f"   ```python")
            print(f"   def generate_for_complexity(n: int) -> str:")
            print(f"       '''Generate test case with input size = n'''")
            print(f"       # Return test input string for size n")
            print(f"       ...")
            print(f"   ```")
        else:
            # Run estimation for each method
            methods = methods_to_test if methods_to_test[0] is not None else [None]
            for method in methods:
                method_name = method or "default"
                print(f"\n📌 Estimating: {method_name}")
                
                estimator = ComplexityEstimator(
                    generator_module=generator_module,
                    problem=problem,
                    solution_module=module,
                    method=method
                )
                result = estimator.estimate()
                
                if result:
                    print(f"\n   ✅ Estimated: {result.complexity}")
                    print(f"      Confidence: {result.confidence:.2f}")
                    print(f"      Details: {result.details}")
                else:
                    print(f"\n   ❌ Estimation failed")


if __name__ == "__main__":
    main()
