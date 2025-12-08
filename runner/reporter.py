# runner/reporter.py
"""
Test Result Reporter - Format and display test results.
"""
from typing import List, Dict, Any

from runner.compare import normalize_output


def truncate_input(input_data: str, max_length: int = 200) -> str:
    """Truncate long input for display."""
    if len(input_data) <= max_length:
        return input_data
    return input_data[:max_length] + f"... ({len(input_data)} chars total)"


def format_validation_label(validation_mode: str) -> str:
    """Format validation mode as a label for output."""
    return f"[{validation_mode}]"


def save_failed_case(problem: str, input_data: str, tests_dir: str) -> str:
    """Save a failed generated case to tests/ folder."""
    import os
    
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


def print_benchmark_summary(all_results: List[Dict[str, Any]]) -> None:
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


def run_method_tests(problem: str, method_name: str, method_info: Dict[str, Any],
                     input_files: List[str], benchmark: bool = False,
                     compare_mode: str = "exact", module: Any = None,
                     generator_module: Any = None, generate_count: int = 0,
                     seed: int = None, save_failed: bool = False,
                     tests_dir: str = "tests") -> Dict[str, Any]:
    """Run all test cases for a specific solution method."""
    from runner.executor import run_one_case, run_generated_case
    
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
    
    import os
    
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

