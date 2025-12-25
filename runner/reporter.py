# runner/reporter.py
"""
Test Result Reporter - Format and display test results.

Enhanced display features:
- Visual ASCII bar chart for performance comparison
- Approach name extraction from class comments
- Adaptive table formatting
"""
import sys
import os
from typing import List, Dict, Any, Optional

from runner.compare import normalize_output


def _supports_unicode() -> bool:
    """Check if the terminal supports Unicode box-drawing characters."""
    try:
        encoding = sys.stdout.encoding or 'utf-8'
        # Test all the Unicode characters we want to use
        test_chars = '═║╔╗╚╝╠╣█░'
        for char in test_chars:
            char.encode(encoding)
        return True
    except (UnicodeEncodeError, LookupError):
        return False


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


def print_visual_benchmark(all_results: List[Dict[str, Any]], 
                           problem_name: str = "Performance Comparison",
                           bar_width: int = 20,
                           approach_mapping: Optional[Dict[str, dict]] = None) -> None:
    """
    Print a visual ASCII bar chart for performance comparison.
    
    Example output (Unicode):
       ╔════════════════════════════════════════════╗
       ║ Two Sum - Performance Comparison           ║
       ╠════════════════════════════════════════════╣
       ║ default: ████████░░░░░░░░░░░░  85ms        ║
       ║   → Hash Map (O(n))                        ║
       ║ naive:   ████████████████████  450ms       ║
       ║   → Brute Force (O(n²))                    ║
       ╚════════════════════════════════════════════╝
    """
    if not all_results:
        return
    
    # Choose character set based on terminal support
    use_unicode = _supports_unicode()
    if use_unicode:
        TL, TR, BL, BR = '╔', '╗', '╚', '╝'  # corners
        H, V = '═', '║'  # horizontal and vertical
        ML, MR = '╠', '╣'  # middle left/right
        BAR_FULL, BAR_EMPTY = '█', '░'
        ARROW = '→'
    else:
        TL, TR, BL, BR = '+', '+', '+', '+'
        H, V = '=', '|'
        ML, MR = '+', '+'
        BAR_FULL, BAR_EMPTY = '#', '.'
        ARROW = '->'
    
    # Calculate average times for each method
    method_times = []
    for result in all_results:
        method = result["method"]
        avg_time = sum(result["times"]) / len(result["times"]) if result["times"] else 0
        approach = None
        complexity = result.get("complexity", "")
        
        # Get approach info if available
        if approach_mapping and method in approach_mapping:
            info = approach_mapping[method]
            approach = info.get('approach')
            if not complexity:
                complexity = info.get('complexity', '')
        
        method_times.append((method, avg_time, approach, complexity))
    
    # Find max time for scaling
    max_time = max(t for _, t, _, _ in method_times) if method_times else 1
    if max_time == 0:
        max_time = 1  # Avoid division by zero
    
    # Calculate widths
    max_method_len = max(len(m) for m, _, _, _ in method_times)
    max_time_str_len = max(len(f"{t:.0f}ms") for _, t, _, _ in method_times)
    
    # Content width for bar line: method + ": " + bar + "  " + time
    bar_line_width = max_method_len + 2 + bar_width + 2 + max_time_str_len
    
    # Title line (no emoji for better compatibility)
    title = f"{problem_name} - Performance"
    title_len = len(title)
    
    # Box width (content + 2 spaces padding on each side)
    box_width = max(bar_line_width + 4, title_len + 4)
    inner_width = box_width - 2  # Inside the box (excluding V on each side)
    
    # Print the box
    print()
    print(f"   {TL}{H * inner_width}{TR}")
    
    # Title row (centered)
    title_padding = inner_width - title_len
    left_pad = title_padding // 2
    right_pad = title_padding - left_pad
    print(f"   {V}{' ' * left_pad}{title}{' ' * right_pad}{V}")
    
    print(f"   {ML}{H * inner_width}{MR}")
    
    # Bar rows (no approach in box)
    for method, avg_time, approach, complexity in method_times:
        # Calculate bar length proportional to time
        if max_time > 0:
            bar_len = int((avg_time / max_time) * bar_width)
        else:
            bar_len = 0
        empty_len = bar_width - bar_len
        
        # Build the bar
        bar = BAR_FULL * bar_len + BAR_EMPTY * empty_len
        
        # Format time string
        time_str = f"{avg_time:.0f}ms"
        
        # Build the bar row content
        method_padded = f"{method}:".ljust(max_method_len + 1)
        time_padded = time_str.rjust(max_time_str_len)
        bar_content = f" {method_padded} {bar}  {time_padded} "
        
        # Pad to fill the box
        bar_padding = inner_width - len(bar_content)
        print(f"   {V}{bar_content}{' ' * bar_padding}{V}")
    
    print(f"   {BL}{H * inner_width}{BR}")
    
    # Print legend below the box (method -> approach mapping)
    has_approaches = any(approach for _, _, approach, _ in method_times)
    if has_approaches:
        print()
        for method, _, approach, _ in method_times:
            if approach:
                print(f"   {method:<{max_method_len}}  {ARROW} {approach}")
    print()


def print_benchmark_summary(all_results: List[Dict[str, Any]], 
                            problem_name: str = "Performance Comparison",
                            approach_mapping: Optional[Dict[str, dict]] = None) -> None:
    """Print performance comparison table with visual bar chart."""
    # Print visual bar chart first
    if len(all_results) > 1:
        print_visual_benchmark(all_results, problem_name, approach_mapping=approach_mapping)
    
    print("=" * 70)
    print("Performance Comparison (Details)")
    print("=" * 70)
    
    # Check if any results have generated tests
    has_generated = any(r.get("gen_total", 0) > 0 for r in all_results)
    
    # Build approach lookup
    approach_lookup = {}
    if approach_mapping:
        for method in approach_mapping:
            info = approach_mapping[method]
            approach_lookup[method] = info.get('approach', '')
    
    # Calculate column widths
    max_method_len = max(len(r["method"]) for r in all_results)
    max_method_len = max(max_method_len, 6)  # "Method"
    
    # Print table header
    print()
    if has_generated:
        print(f"{'Method':<{max_method_len}}  {'Avg Time':>10}  {'Static':>8}  {'Generated':>10}  Complexity")
        print(f"{'-' * max_method_len}  {'-' * 10}  {'-' * 8}  {'-' * 10}  {'-' * 20}")
    else:
        print(f"{'Method':<{max_method_len}}  {'Avg Time':>10}  {'Pass Rate':>10}  Complexity")
        print(f"{'-' * max_method_len}  {'-' * 10}  {'-' * 10}  {'-' * 20}")
    
    for result in all_results:
        method = result["method"]
        complexity = result["complexity"]
        avg_time = sum(result["times"]) / len(result["times"]) if result["times"] else 0
        
        static_rate = f"{result['passed']}/{result['total']}"
        gen_passed = result.get("gen_passed", 0)
        gen_total = result.get("gen_total", 0)
        
        if has_generated and gen_total > 0:
            gen_rate = f"{gen_passed}/{gen_total}"
            print(f"{method:<{max_method_len}}  {avg_time:>8.2f}ms  {static_rate:>8}  {gen_rate:>10}  {complexity}")
        else:
            print(f"{method:<{max_method_len}}  {avg_time:>8.2f}ms  {static_rate:>10}  {complexity}")
    
    # Print legend below the table (method -> approach mapping)
    has_approaches = any(approach_lookup.get(r["method"]) for r in all_results)
    if has_approaches:
        print()
        for result in all_results:
            method = result["method"]
            approach = approach_lookup.get(method)
            if approach:
                print(f"{method:<{max_method_len}}  → {approach}")
    
    print()
    print("=" * 70)


def run_method_tests(problem: str, method_name: str, method_info: Dict[str, Any],
                     input_files: List[str], benchmark: bool = False,
                     compare_mode: str = "exact", module: Any = None,
                     generator_module: Any = None, generate_count: int = 0,
                     seed: int = None, save_failed: bool = False,
                     tests_dir: str = "tests",
                     approach_info: Optional[dict] = None) -> Dict[str, Any]:
    """Run all test cases for a specific solution method."""
    from runner.executor import run_one_case, run_generated_case
    
    # Get approach from parsed class comments or fallback to description
    approach = None
    if approach_info:
        approach = approach_info.get('approach')
    if not approach:
        approach = method_info.get('description')
    
    results = {
        "method": method_name,
        "display_name": method_info.get("method", method_name),
        "complexity": method_info.get("complexity", "Unknown"),
        "description": method_info.get("description", ""),
        "approach": approach,
        "cases": [],
        "passed": 0,
        "total": 0,
        "skipped": 0,
        "times": [],
        "validation_summary": {},  # Track count by validation mode
        "gen_passed": 0,
        "gen_total": 0
    }
    
    # Enhanced method header display
    print(f"\n{'─' * 50}")
    print(f"📌 Shorthand: {method_name}")
    if approach:
        print(f"   Approach: {approach}")
    if method_info.get("complexity"):
        print(f"   Complexity: {method_info['complexity']}")
    print(f"{'─' * 50}")
    
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

