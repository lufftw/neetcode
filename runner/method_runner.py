# runner/method_runner.py
"""
Method Runner - Execute test cases for a specific solution method.

Extracted from reporter.py for better separation of concerns.
This module handles the actual test execution logic, while reporter.py
focuses on display formatting.

Memory profiling integrated per Memory_Metrics.md specification:
- Method-level aggregation by default (Peak RSS, P95 RSS)
- Case-level metrics collected for --memory-per-case debugging
"""
import os
from typing import List, Dict, Any, Optional

from runner.executor import run_one_case, run_generated_case
from runner.compare import normalize_output
from runner.reporter import truncate_input, format_validation_label, save_failed_case
from runner.memory_profiler import (
    CaseMemoryMetrics,
    MethodMemoryMetrics,
    format_bytes,
)


def run_method_tests(problem: str, method_name: str, method_info: Dict[str, Any],
                     input_files: List[str], benchmark: bool = False,
                     compare_mode: str = "exact", module: Any = None,
                     generator_module: Any = None, generate_count: int = 0,
                     seed: int = None, save_failed: bool = False,
                     tests_dir: str = "tests",
                     approach_info: Optional[dict] = None,
                     profile_memory: bool = False) -> Dict[str, Any]:
    """
    Run all test cases for a specific solution method.
    
    Args:
        problem: Problem name
        method_name: Solution method shorthand (e.g., "default", "heap")
        method_info: Metadata from SOLUTIONS dict
        input_files: List of .in file paths
        benchmark: Whether to show timing
        compare_mode: Comparison mode (exact, sorted, set)
        module: Loaded solution module
        generator_module: Loaded generator module (optional)
        generate_count: Number of generated tests (0 = none)
        seed: Random seed for reproducibility
        save_failed: Whether to save failed cases
        tests_dir: Directory for test files
        approach_info: Parsed approach info from class comments
        profile_memory: Whether to collect memory metrics
    
    Returns:
        Dict with test results including memory metrics
    """
    # Get approach from parsed class comments or fallback to description
    approach = None
    if approach_info:
        approach = approach_info.get('approach')
    if not approach:
        approach = method_info.get('description')
    
    # Extract aux_space from complexity string or method_info
    aux_space = "Undeclared"
    complexity_str = method_info.get("complexity", "")
    if complexity_str:
        # Try to extract space complexity (e.g., "O(n) time, O(1) space")
        import re
        space_match = re.search(r'Space:\s*([^,\n]+)', complexity_str, re.IGNORECASE)
        if space_match:
            aux_space = space_match.group(1).strip()
        elif 'space' in complexity_str.lower():
            # Look for space part after comma
            parts = complexity_str.split(',')
            for part in parts:
                if 'space' in part.lower():
                    aux_space = part.strip()
                    break
    
    # Initialize memory metrics tracker
    memory_metrics = MethodMemoryMetrics(
        method_name=method_name,
        aux_space=aux_space
    )
    
    results = {
        "method": method_name,
        "display_name": method_info.get("method", method_name),
        "complexity": method_info.get("complexity", "Unknown"),
        "aux_space": aux_space,
        "description": method_info.get("description", ""),
        "approach": approach,
        "cases": [],
        "passed": 0,
        "total": 0,
        "skipped": 0,
        "times": [],
        "validation_summary": {},
        "gen_passed": 0,
        "gen_total": 0,
        "memory_metrics": memory_metrics,
    }
    
    # Enhanced method header display
    print(f"\n{'─' * 50}")
    print(f"📌 Shorthand: {method_name}")
    if approach:
        print(f"   Approach: {approach}")
    if method_info.get("complexity"):
        print(f"   Complexity: {method_info['complexity']}")
    print(f"{'─' * 50}")
    
    # Run static tests
    if input_files:
        _run_static_tests(results, problem, method_name, input_files, 
                         benchmark, compare_mode, module, profile_memory)
    
    # Run generated tests
    if generator_module and generate_count > 0:
        _run_generated_tests(results, problem, method_name, generator_module,
                            generate_count, seed, benchmark, compare_mode, 
                            module, save_failed, tests_dir, profile_memory)
    
    return results


def _run_static_tests(results: Dict[str, Any], problem: str, method_name: str,
                      input_files: List[str], benchmark: bool,
                      compare_mode: str, module: Any,
                      profile_memory: bool = False) -> None:
    """Run static tests from tests/ directory with optional memory profiling."""
    print("   --- tests/ (static) ---")
    
    memory_metrics: MethodMemoryMetrics = results.get("memory_metrics")
    
    for in_path in input_files:
        out_path = in_path.replace(".in", ".out")
        case_name = os.path.basename(in_path).replace(".in", "")
        
        ok, elapsed_ms, actual, expected, validation_mode, peak_rss, input_bytes = run_one_case(
            problem, in_path, out_path, method_name, benchmark, compare_mode, module,
            profile_memory=profile_memory
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
        
        # Track memory metrics
        if memory_metrics is not None:
            case_metrics = CaseMemoryMetrics(
                case_name=case_name,
                peak_rss_bytes=peak_rss,
                input_bytes=input_bytes,
                elapsed_ms=elapsed_ms
            )
            memory_metrics.add_case(case_metrics)
        
        label = format_validation_label(validation_mode)
        
        if ok:
            results["passed"] += 1
            if benchmark:
                print(f"   {case_name}: ✅ PASS ({elapsed_ms:.2f}ms) {label}")
            else:
                print(f"   {case_name}: ✅ PASS {label}")
        else:
            print(f"   {case_name}: ❌ FAIL {label}")
            if expected is not None:
                print(f"      Expected: {normalize_output(expected)[:100]}...")
            print(f"      Actual:   {normalize_output(actual)[:100]}...")
        
        results["cases"].append({
            "name": case_name,
            "passed": ok,
            "time_ms": elapsed_ms,
            "validation_mode": validation_mode,
            "peak_rss_bytes": peak_rss,
            "input_bytes": input_bytes,
        })


def _run_generated_tests(results: Dict[str, Any], problem: str, method_name: str,
                         generator_module: Any, generate_count: int, seed: int,
                         benchmark: bool, compare_mode: str, module: Any,
                         save_failed: bool, tests_dir: str,
                         profile_memory: bool = False) -> None:
    """Run generated test cases with optional memory profiling."""
    print()
    seed_info = f", seed: {seed}" if seed else ""
    print(f"   --- generators/ ({generate_count} cases{seed_info}) ---")
    
    memory_metrics: MethodMemoryMetrics = results.get("memory_metrics")
    
    generate_func = generator_module.generate
    gen_iter = generate_func(generate_count, seed)
    
    for i, input_data in enumerate(gen_iter, 1):
        case_name = f"gen_{i}"
        
        ok, elapsed_ms, actual, input_used, peak_rss, input_bytes = run_generated_case(
            problem, input_data, case_name, method_name,
            benchmark, compare_mode, module,
            profile_memory=profile_memory
        )
        
        if ok is None:
            print(f"   {case_name}: ⚠️ SKIP (requires JUDGE_FUNC)")
            continue
        
        results["gen_total"] += 1
        results["times"].append(elapsed_ms)
        
        # Track memory metrics
        if memory_metrics is not None:
            case_metrics = CaseMemoryMetrics(
                case_name=case_name,
                peak_rss_bytes=peak_rss,
                input_bytes=input_bytes,
                elapsed_ms=elapsed_ms
            )
            memory_metrics.add_case(case_metrics)
        
        if ok:
            results["gen_passed"] += 1
            if benchmark:
                print(f"   {case_name}: ✅ PASS ({elapsed_ms:.2f}ms) [generated]")
            else:
                print(f"   {case_name}: ✅ PASS [generated]")
        else:
            print(f"   {case_name}: ❌ FAIL [generated]")
            print(f"      ┌─ Input ─────────────────────────────────")
            for line in truncate_input(input_data).split('\n'):
                print(f"      │ {line}")
            print(f"      ├─ Actual ────────────────────────────────")
            print(f"      │ {normalize_output(actual)[:100]}")
            print(f"      └─────────────────────────────────────────")
            
            if save_failed:
                saved_path = save_failed_case(problem, input_data, tests_dir)
                print(f"      💾 Saved to: {saved_path}")


def run_legacy_tests(problem: str, input_files: List[str], benchmark: bool,
                     compare_mode: str, module: Any, generator_module: Any = None,
                     generate_count: int = 0, seed: int = None,
                     save_failed: bool = False, tests_dir: str = "tests",
                     profile_memory: bool = False) -> Dict[str, Any]:
    """
    Run tests in legacy mode (no SOLUTIONS metadata).
    
    This is used when solution files don't define SOLUTIONS dict.
    Returns results dict compatible with multi-solution mode.
    """
    # Initialize memory metrics tracker
    memory_metrics = MethodMemoryMetrics(
        method_name="default",
        aux_space="Undeclared"
    )
    
    results = {
        "method": "default",
        "display_name": "default",
        "complexity": "Unknown",
        "aux_space": "Undeclared",
        "description": "",
        "approach": None,
        "cases": [],
        "passed": 0,
        "total": 0,
        "skipped": 0,
        "times": [],
        "validation_summary": {},
        "gen_passed": 0,
        "gen_total": 0,
        "memory_metrics": memory_metrics,
    }
    
    print(f"\n📌 Running default solution...")
    print()
    
    # Run static tests
    if input_files:
        _run_static_tests_legacy(results, problem, input_files, 
                                  benchmark, compare_mode, module, profile_memory)
    
    # Run generated tests
    if generator_module and generate_count > 0:
        _run_generated_tests_legacy(results, problem, generator_module,
                                    generate_count, seed, benchmark, 
                                    compare_mode, module, save_failed, tests_dir,
                                    profile_memory)
    
    return results


def _run_static_tests_legacy(results: Dict[str, Any], problem: str,
                              input_files: List[str], benchmark: bool,
                              compare_mode: str, module: Any,
                              profile_memory: bool = False) -> None:
    """Run static tests in legacy mode (method=None) with optional memory profiling."""
    print("   --- tests/ (static) ---")
    
    memory_metrics: MethodMemoryMetrics = results.get("memory_metrics")
    
    for in_path in input_files:
        out_path = in_path.replace(".in", ".out")
        case_name = os.path.basename(in_path).replace(".in", "")
        
        ok, elapsed_ms, actual, expected, validation_mode, peak_rss, input_bytes = run_one_case(
            problem, in_path, out_path, None, benchmark, compare_mode, module,
            profile_memory=profile_memory
        )
        
        results["validation_summary"][validation_mode] = \
            results["validation_summary"].get(validation_mode, 0) + 1
        
        if validation_mode == "skip":
            results["skipped"] += 1
            print(f"   {case_name}: ⚠️ SKIP (missing .out, no JUDGE_FUNC)")
            continue
        
        results["total"] += 1
        results["times"].append(elapsed_ms)
        
        # Track memory metrics
        if memory_metrics is not None:
            case_metrics = CaseMemoryMetrics(
                case_name=case_name,
                peak_rss_bytes=peak_rss,
                input_bytes=input_bytes,
                elapsed_ms=elapsed_ms
            )
            memory_metrics.add_case(case_metrics)
        
        label = format_validation_label(validation_mode)
        
        if ok:
            results["passed"] += 1
            if benchmark:
                print(f"   {case_name}: ✅ PASS ({elapsed_ms:.2f}ms) {label}")
            else:
                print(f"   {case_name}: ✅ PASS {label}")
        else:
            print(f"   {case_name}: ❌ FAIL {label}")
            if expected is not None:
                print(f"      Expected: {normalize_output(expected)[:100]}...")
            print(f"      Actual:   {normalize_output(actual)[:100]}...")


def _run_generated_tests_legacy(results: Dict[str, Any], problem: str,
                                 generator_module: Any, generate_count: int,
                                 seed: int, benchmark: bool, compare_mode: str,
                                 module: Any, save_failed: bool, 
                                 tests_dir: str,
                                 profile_memory: bool = False) -> None:
    """Run generated tests in legacy mode (method=None) with optional memory profiling."""
    print()
    seed_info = f", seed: {seed}" if seed else ""
    print(f"   --- generators/ ({generate_count} cases{seed_info}) ---")
    
    memory_metrics: MethodMemoryMetrics = results.get("memory_metrics")
    
    generate_func = generator_module.generate
    gen_iter = generate_func(generate_count, seed)
    failed_inputs = []
    
    for i, input_data in enumerate(gen_iter, 1):
        case_name = f"gen_{i}"
        
        ok, elapsed_ms, actual, input_used, peak_rss, input_bytes = run_generated_case(
            problem, input_data, case_name, None, benchmark, compare_mode, module,
            profile_memory=profile_memory
        )
        
        if ok is None:
            print(f"   {case_name}: ⚠️ SKIP (requires JUDGE_FUNC)")
            continue
        
        results["gen_total"] += 1
        results["times"].append(elapsed_ms)
        
        # Track memory metrics
        if memory_metrics is not None:
            case_metrics = CaseMemoryMetrics(
                case_name=case_name,
                peak_rss_bytes=peak_rss,
                input_bytes=input_bytes,
                elapsed_ms=elapsed_ms
            )
            memory_metrics.add_case(case_metrics)
        
        if ok:
            results["gen_passed"] += 1
            if benchmark:
                print(f"   {case_name}: ✅ PASS ({elapsed_ms:.2f}ms) [generated]")
            else:
                print(f"   {case_name}: ✅ PASS [generated]")
        else:
            print(f"   {case_name}: ❌ FAIL [generated]")
            print(f"      ┌─ Input ─────────────────────────────────")
            for line in truncate_input(input_data).split('\n'):
                print(f"      │ {line}")
            print(f"      ├─ Actual ────────────────────────────────")
            print(f"      │ {normalize_output(actual)[:100]}")
            print(f"      └─────────────────────────────────────────")
            
            if save_failed:
                saved_path = save_failed_case(problem, input_data, tests_dir)
                print(f"      💾 Saved to: {saved_path}")
            
            failed_inputs.append(input_data)
    
    # Store failed inputs for reproduction hint
    results["_failed_inputs"] = failed_inputs

