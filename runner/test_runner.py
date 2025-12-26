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
from typing import Optional, List, Dict, Any, Tuple

# Enable UTF-8 output on Windows for emoji support
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import from runner package (new subpackage structure)
from runner import (
    # utils
    load_solution_module,
    load_generator_module,
    normalize_output,
    build_method_mapping,
    # display
    truncate_input,
    format_validation_label,
    save_failed_case,
    print_benchmark_summary,
    print_visual_benchmark,
    print_memory_trace,
    print_memory_per_case,
    print_trace_compare,
    # analysis
    HAS_PSUTIL,
    # core
    run_one_case,
    run_generated_case,
    PYTHON_EXE,
    run_method_tests,
    run_legacy_tests,
)

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


def _parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
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

Memory profiling examples:
  python runner/test_runner.py 0023 --all --benchmark  # includes memory in table
  python runner/test_runner.py 0023 --all --memory-trace
  python runner/test_runner.py 0023 --all --trace-compare
  python runner/test_runner.py 0023 --memory-per-case
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
    
    # Memory profiling arguments
    parser.add_argument("--memory-trace", action="store_true",
                        help="Show run-level memory traces per method")
    parser.add_argument("--memory-per-case", action="store_true",
                        help="Show Top-K cases by peak RSS (debug mode)")
    parser.add_argument("--trace-compare", action="store_true",
                        help="Show multi-method memory comparison with ranking")
    
    return parser.parse_args()


def _load_modules(problem: str, input_files: List[str], generate_count: int, 
                  args: argparse.Namespace) -> tuple:
    """Load solution and generator modules."""
    # Try to load solution module with given problem name
    module, solutions_meta, compare_mode = load_solution_module(problem)
    
    # If not found and we have test files, try to extract full problem name
    if module is None and input_files:
        first_test_file = os.path.basename(input_files[0])
        match = re.match(r'^(.+?)_\d+\.in$', first_test_file)
        if match:
            full_problem_name = match.group(1)
            if full_problem_name != problem:
                print(f"💡 Problem name '{problem}' not found, trying '{full_problem_name}'...")
                problem = full_problem_name
                module, solutions_meta, compare_mode = load_solution_module(problem)
    
    # Load generator module if needed
    generator_module = None
    has_judge_func = hasattr(module, 'JUDGE_FUNC') if module else False
    
    if generate_count > 0 or args.estimate:
        generator_module = load_generator_module(problem)
        if not generator_module:
            if generate_count > 0:
                print(f"⚠️ No generator found: generators/{problem}.py")
                if args.generate_only is not None:
                    sys.exit(1)
                print(f"   Continuing with tests/ only...")
                generate_count = 0
        elif generate_count > 0 and not has_judge_func:
            print(f"❌ Generator requires JUDGE_FUNC in solution file")
            sys.exit(1)
    
    return problem, module, solutions_meta, compare_mode, generator_module, generate_count, has_judge_func


def _run_complexity_estimation(args: argparse.Namespace, generator_module: Any,
                               problem: str, module: Any, 
                               methods_to_test: List[str],
                               profile_memory: bool = False) -> Tuple[Dict[str, Any], Dict[str, List]]:
    """
    Run complexity estimation for all methods.
    
    Returns:
        Tuple of (estimation_results, memory_samples_by_method)
    """
    from runner.analysis.complexity import ComplexityEstimator
    
    estimation_results = {}
    memory_samples_by_method = {}
    
    print(f"\n{'=' * 60}")
    print(f"📈 Complexity Estimation")
    print(f"{'=' * 60}")
    
    if not ComplexityEstimator.is_available():
        print(f"❌ big-O package not installed")
        print(f"   Install with: pip install big-O")
        return estimation_results, memory_samples_by_method
    
    if not ComplexityEstimator.can_estimate(generator_module):
        reason = ComplexityEstimator.get_unavailable_reason(generator_module)
        print(f"❌ Cannot estimate complexity: {reason}")
        print(f"\n   To enable complexity estimation, add to your generator:")
        print(f"   ```python")
        print(f"   def generate_for_complexity(n: int) -> str:")
        print(f"       '''Generate test case with input size = n'''")
        print(f"       # Return test input string for size n")
        print(f"       ...")
        print(f"   ```")
        return estimation_results, memory_samples_by_method
    
    # Run estimation for each method
    methods = methods_to_test if methods_to_test[0] is not None else [None]
    for method in methods:
        method_name = method or "default"
        print(f"\n📌 Estimating: {method_name}")
        
        estimator = ComplexityEstimator(
            generator_module=generator_module,
            problem=problem,
            solution_module=module,
            method=method,
            profile_memory=profile_memory
        )
        est_result = estimator.estimate()
        
        if est_result:
            estimation_results[method_name] = est_result
            print(f"\n   ✅ Estimated: {est_result.complexity}")
            print(f"      Confidence: {est_result.confidence:.2f}")
            print(f"      Details: {est_result.details}")
        else:
            print(f"\n   ❌ Estimation failed")
        
        # Collect memory samples if profiling enabled
        if profile_memory:
            memory_samples_by_method[method_name] = estimator.get_memory_metrics()
    
    return estimation_results, memory_samples_by_method


def _print_summary(result: Dict[str, Any], input_files: List[str], 
                   args: argparse.Namespace, generate_count: int) -> None:
    """Print summary for a single result."""
    total_all = result['total'] + result['gen_total']
    passed_all = result['passed'] + result['gen_passed']
    print(f"\nSummary: {passed_all} / {total_all} cases passed.")
    
    if input_files and result['gen_total'] > 0:
        print(f"   ├─ Static (tests/): {result['passed']}/{result['total']}")
        print(f"   └─ Generated: {result['gen_passed']}/{result['gen_total']}")
    
    if result.get('skipped', 0) > 0:
        print(f"Skipped: {result['skipped']} cases (missing .out)")
    
    if args.benchmark and result['times']:
        avg_time = sum(result['times']) / len(result['times'])
        print(f"Average Time: {avg_time:.2f}ms")
    
    # Reproduction hint for failed generated tests
    failed_inputs = result.get('_failed_inputs', [])
    if failed_inputs and args.seed:
        print(f"\n💡 To reproduce: python runner/test_runner.py {args.problem} --generate {generate_count} --seed {args.seed}")


def main():
    args = _parse_args()
    
    problem = args.problem
    tests_dir = args.tests_dir
    
    # Determine generator settings
    generate_count = args.generate_only or args.generate or 0
    generate_only = args.generate_only is not None
    
    # Determine if memory profiling is needed
    # Enable if --benchmark is set (for table columns) or any memory flag is set
    profile_memory = (args.benchmark or args.memory_trace or 
                      args.memory_per_case or args.trace_compare)
    
    # Check psutil availability for memory profiling
    if profile_memory and not HAS_PSUTIL:
        print("⚠️ Memory profiling requires psutil: pip install psutil")
        print("   Continuing without memory metrics...")
        profile_memory = False
    
    # Find test input files (skip if generate-only)
    if generate_only:
        input_files = []
    else:
        pattern = os.path.join(tests_dir, f"{problem}_*.in")
        all_files = sorted(glob.glob(pattern))
        input_files = [f for f in all_files if "_failed_" not in f]
    
    # Check if we have anything to run
    if not input_files and generate_count == 0:
        print(f"⚠️ No test input files found and no --generate specified")
        sys.exit(1)
    
    # Load modules
    (problem, module, solutions_meta, compare_mode, generator_module, 
     generate_count, has_judge_func) = _load_modules(
        problem, input_files, generate_count, args
    )
    
    # Build approach mapping from class comments
    approach_mapping = None
    if solutions_meta:
        solution_path = os.path.join("solutions", f"{problem}.py")
        approach_mapping = build_method_mapping(solution_path, solutions_meta)
    
    # Print header
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
    if profile_memory:
        print(f"🧠 Memory profiling: enabled")
    print(f"{'=' * 60}")
    
    # Determine which solutions to test
    if args.all and solutions_meta:
        methods_to_test = list(solutions_meta.keys())
    elif args.method:
        if solutions_meta and args.method not in solutions_meta:
            available = list(solutions_meta.keys())
            print(f"❌ Solution method '{args.method}' not found")
            print(f"   Available methods: {', '.join(available)}")
            sys.exit(1)
        methods_to_test = [args.method]
    elif solutions_meta and "default" in solutions_meta:
        methods_to_test = ["default"]
    else:
        methods_to_test = [None]  # Legacy mode
    
    all_results = []
    
    # Run tests
    for method in methods_to_test:
        if method is None:
            # Legacy mode
            result = run_legacy_tests(
                problem, input_files, args.benchmark, compare_mode, module,
                generator_module, generate_count, args.seed, 
                args.save_failed, tests_dir, profile_memory=profile_memory
            )
            all_results.append(result)
            _print_summary(result, input_files, args, generate_count)
        else:
            # Multi-solution mode
            method_info = solutions_meta.get(method, {"method": method})
            approach_info = approach_mapping.get(method) if approach_mapping else None
            
            result = run_method_tests(
                problem, method, method_info, input_files, args.benchmark, 
                compare_mode, module, generator_module, generate_count, 
                args.seed, args.save_failed, tests_dir, approach_info=approach_info,
                profile_memory=profile_memory
            )
            all_results.append(result)
            
            total_all = result['total'] + result['gen_total']
            passed_all = result['passed'] + result['gen_passed']
            print(f"\n   Result: {passed_all} / {total_all} cases passed.")
            if input_files and result['gen_total'] > 0:
                print(f"      ├─ Static: {result['passed']}/{result['total']}")
                print(f"      └─ Generated: {result['gen_passed']}/{result['gen_total']}")
    
    # Complexity estimation (run before benchmark display)
    estimation_results = {}
    if args.estimate:
        estimation_results, memory_samples = _run_complexity_estimation(
            args, generator_module, problem, module, methods_to_test,
            profile_memory=profile_memory
        )
        # Store estimation results in all_results
        for result in all_results:
            method_name = result["method"]
            if method_name in estimation_results:
                result["estimated_complexity"] = estimation_results[method_name]
            
            # Merge estimation memory samples into method's memory_metrics
            if profile_memory and method_name in memory_samples:
                from runner.memory_profiler import CaseMemoryMetrics
                memory_metrics = result.get("memory_metrics")
                if memory_metrics:
                    for i, (size, peak_bytes, elapsed_ms, input_bytes) in enumerate(memory_samples[method_name]):
                        case_metrics = CaseMemoryMetrics(
                            case_name=f"est_n{size}_{i+1}",
                            peak_rss_bytes=peak_bytes,
                            input_bytes=input_bytes,
                            input_scale={'n': size},
                            elapsed_ms=elapsed_ms,
                            measurement_type="alloc"  # tracemalloc measurement
                        )
                        memory_metrics.add_case(case_metrics)
    
    # Print benchmark summary (with memory columns if profiling enabled)
    # Output order per CLI_OUTPUT_CONTRACT.md Section 6:
    # 1. Time visual bar chart (existing)
    # 2. Benchmark table (--benchmark)
    # 3. Run-level memory traces (--memory-trace)
    # 4. Overall comparison (--trace-compare)
    # 5. Case-level debug output (--memory-per-case)
    
    if len(all_results) > 1 and args.benchmark:
        print_benchmark_summary(all_results, problem_name=problem, 
                               approach_mapping=approach_mapping,
                               show_memory=profile_memory)
    elif len(all_results) == 1 and methods_to_test[0] is not None:
        result = all_results[0]
        print(f"\nSummary: {result['passed']} / {result['total']} cases passed.")
    
    # Memory trace output (--memory-trace)
    if args.memory_trace:
        print_memory_trace(all_results)
    
    # Trace comparison output (--trace-compare)
    if args.trace_compare:
        print_trace_compare(all_results)
    
    # Per-case memory debug output (--memory-per-case)
    if args.memory_per_case:
        print_memory_per_case(all_results)


if __name__ == "__main__":
    main()
