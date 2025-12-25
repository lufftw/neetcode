# runner/reporter.py
"""
Test Result Reporter - Format and display test results.

Note: Test execution logic moved to method_runner.py

Memory Profiling Display (per Cli_Output_Memory.md):
- --benchmark: includes Peak RSS, P95 RSS columns in table
- --memory-trace: run-level memory traces per method
- --memory-per-case: Top-K cases by peak RSS (debug)
- --trace-compare: multi-method memory comparison
"""
import sys
import os
from typing import List, Dict, Any, Optional

from runner.memory_profiler import (
    MethodMemoryMetrics,
    format_bytes,
    generate_memory_trace,
)


def _supports_unicode() -> bool:
    """Check if terminal supports Unicode box-drawing characters."""
    try:
        encoding = sys.stdout.encoding or 'utf-8'
        for char in '═║╔╗╚╝╠╣█░':
            char.encode(encoding)
        return True
    except (UnicodeEncodeError, LookupError):
        return False


def truncate_input(input_data: str, max_length: int = 200) -> str:
    """Truncate long input for display."""
    return input_data if len(input_data) <= max_length else input_data[:max_length] + f"... ({len(input_data)} chars)"


def format_validation_label(validation_mode: str) -> str:
    """Format validation mode as a label."""
    return f"[{validation_mode}]"


def save_failed_case(problem: str, input_data: str, tests_dir: str) -> str:
    """Save a failed generated case to tests/ folder."""
    n = 1
    while os.path.exists(os.path.join(tests_dir, f"{problem}_failed_{n}.in")):
        n += 1
    filepath = os.path.join(tests_dir, f"{problem}_failed_{n}.in")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(input_data if input_data.endswith('\n') else input_data + '\n')
    return filepath


def print_visual_benchmark(all_results: List[Dict[str, Any]], 
                           problem_name: str = "Performance Comparison",
                           bar_width: int = 20,
                           approach_mapping: Optional[Dict[str, dict]] = None) -> None:
    """Print a visual ASCII bar chart for performance comparison."""
    if not all_results:
        return
    
    # Character set based on terminal support
    u = _supports_unicode()
    chars = {'TL': '╔' if u else '+', 'TR': '╗' if u else '+', 'BL': '╚' if u else '+', 
             'BR': '╝' if u else '+', 'H': '═' if u else '=', 'V': '║' if u else '|',
             'ML': '╠' if u else '+', 'MR': '╣' if u else '+',
             'BAR_FULL': '█' if u else '#', 'BAR_EMPTY': '░' if u else '.', 'ARROW': '→' if u else '->'}
    
    # Collect method data
    method_times = []
    for r in all_results:
        method, times = r["method"], r["times"]
        avg = sum(times) / len(times) if times else 0
        approach = approach_mapping.get(method, {}).get('approach') if approach_mapping else None
        complexity = r.get("complexity", "") or (approach_mapping.get(method, {}).get('complexity', '') if approach_mapping else '')
        method_times.append((method, avg, approach, complexity, r.get("estimated_complexity")))
    
    max_time = max((t for _, t, _, _, _ in method_times), default=1) or 1
    max_method_len = max(len(m) for m, _, _, _, _ in method_times)
    max_time_str_len = max(len(f"{t:.0f}ms") for _, t, _, _, _ in method_times)
    
    _draw_chart_box(method_times, problem_name, bar_width, max_time, max_method_len, max_time_str_len, chars)
    _print_chart_legend(method_times, max_method_len, chars['ARROW'])
    _print_estimated_complexity(method_times, max_method_len)
    print()


def _draw_chart_box(method_times: List[tuple], problem_name: str, bar_width: int,
                    max_time: float, max_method_len: int, max_time_str_len: int,
                    chars: dict) -> None:
    """Draw the chart box with bars."""
    TL, TR, BL, BR = chars['TL'], chars['TR'], chars['BL'], chars['BR']
    H, V, ML, MR = chars['H'], chars['V'], chars['ML'], chars['MR']
    BAR_FULL, BAR_EMPTY = chars['BAR_FULL'], chars['BAR_EMPTY']
    
    bar_line_width = max_method_len + 2 + bar_width + 2 + max_time_str_len
    title = f"{problem_name} - Performance"
    box_width = max(bar_line_width + 4, len(title) + 4)
    inner_width = box_width - 2
    
    print()
    print(f"   {TL}{H * inner_width}{TR}")
    
    # Title row (centered)
    title_padding = inner_width - len(title)
    left_pad = title_padding // 2
    right_pad = title_padding - left_pad
    print(f"   {V}{' ' * left_pad}{title}{' ' * right_pad}{V}")
    
    print(f"   {ML}{H * inner_width}{MR}")
    
    # Bar rows
    for method, avg_time, _, _, _ in method_times:
        bar_len = int((avg_time / max_time) * bar_width) if max_time > 0 else 0
        bar = BAR_FULL * bar_len + BAR_EMPTY * (bar_width - bar_len)
        time_str = f"{avg_time:.0f}ms"
        
        method_padded = f"{method}:".ljust(max_method_len + 1)
        time_padded = time_str.rjust(max_time_str_len)
        bar_content = f" {method_padded} {bar}  {time_padded} "
        bar_padding = inner_width - len(bar_content)
        print(f"   {V}{bar_content}{' ' * bar_padding}{V}")
    
    print(f"   {BL}{H * inner_width}{BR}")


def _print_chart_legend(method_times: List[tuple], max_method_len: int, 
                        arrow: str) -> None:
    """Print legend below the chart."""
    has_approaches = any(approach for _, _, approach, _, _ in method_times)
    if has_approaches:
        print()
        for method, _, approach, _, _ in method_times:
            if approach:
                print(f"   {method:<{max_method_len}}  {arrow} {approach}")


def _print_estimated_complexity(method_times: List[tuple], 
                                max_method_len: int) -> None:
    """Print estimated complexity section if available."""
    has_estimates = any(est for _, _, _, _, est in method_times)
    if has_estimates:
        print()
        print("   📈 Estimated Complexity:")
        max_complexity_len = max(
            len(est.complexity) for _, _, _, _, est in method_times if est
        ) if has_estimates else 0
        
        for method, _, _, _, estimated in method_times:
            if estimated:
                complexity_str = estimated.complexity.ljust(max_complexity_len)
                print(f"   {method:<{max_method_len}}: {complexity_str}  [confidence: {estimated.confidence:.2f}]")


def print_benchmark_summary(all_results: List[Dict[str, Any]], 
                            problem_name: str = "Performance Comparison",
                            approach_mapping: Optional[Dict[str, dict]] = None,
                            show_memory: bool = True) -> None:
    """Print performance comparison table with visual bar chart and memory metrics."""
    if len(all_results) > 1:
        print_visual_benchmark(all_results, problem_name, approach_mapping=approach_mapping)
    
    print("=" * 70)
    print("Performance Comparison (Details)")
    print("=" * 70)
    
    has_gen = any(r.get("gen_total", 0) > 0 for r in all_results)
    has_est = any(r.get("estimated_complexity") for r in all_results)
    has_memory = show_memory and any(r.get("memory_metrics") for r in all_results)
    approach_lookup = {m: approach_mapping[m].get('approach', '') for m in approach_mapping} if approach_mapping else {}
    max_len = max(max(len(r["method"]) for r in all_results), 6)
    
    _print_table(all_results, max_len, has_gen, has_est, approach_lookup, has_memory)
    print()
    print("=" * 70)


def _print_table(all_results: List[Dict[str, Any]], max_method_len: int,
                 has_generated: bool, has_estimated: bool, approach_lookup: dict,
                 has_memory: bool = False) -> None:
    """Print table header, rows, and legend with optional memory columns."""
    print()
    
    # Build header based on available data
    # Column order per CLI_OUTPUT_CONTRACT.md:
    # Method | Avg Time | Pass Rate | Declared | Estimated | Peak RSS | P95 RSS
    
    header_parts = [f"{'Method':<{max_method_len}}", f"{'Avg Time':>10}"]
    sep_parts = [f"{'-'*max_method_len}", f"{'-'*10}"]
    
    if has_generated:
        header_parts.extend([f"{'Static':>8}", f"{'Generated':>10}"])
        sep_parts.extend([f"{'-'*8}", f"{'-'*10}"])
    else:
        header_parts.append(f"{'Pass Rate':>10}")
        sep_parts.append(f"{'-'*10}")
    
    if has_estimated:
        header_parts.extend([f"{'Declared':>12}", f"{'Estimated':>12}"])
        sep_parts.extend([f"{'-'*12}", f"{'-'*12}"])
    else:
        # Show "Complexity" for backward compatibility when no estimation
        header_parts.append("Complexity")
        sep_parts.append(f"{'-'*20}")
    
    if has_memory:
        header_parts.extend([f"{'Peak RSS':>10}", f"{'P95 RSS':>10}"])
        sep_parts.extend([f"{'-'*10}", f"{'-'*10}"])
    
    print("  ".join(header_parts))
    print("  ".join(sep_parts))
    
    # Rows
    for r in all_results:
        method, times = r["method"], r["times"]
        avg = sum(times) / len(times) if times else 0
        static_rate = f"{r['passed']}/{r['total']}"
        gen_total = r.get("gen_total", 0)
        gen_rate = f"{r.get('gen_passed', 0)}/{gen_total}"
        
        row_parts = [f"{method:<{max_method_len}}", f"{avg:>8.2f}ms"]
        
        if has_generated and gen_total > 0:
            row_parts.extend([f"{static_rate:>8}", f"{gen_rate:>10}"])
        else:
            row_parts.append(f"{static_rate:>10}")
        
        if has_estimated:
            est_str = r.get("estimated_complexity").complexity if r.get("estimated_complexity") else "-"
            row_parts.extend([f"{r['complexity']:>12}", f"{est_str:>12}"])
        else:
            # Show full complexity string for backward compatibility
            row_parts.append(f"{r['complexity']}")
        
        if has_memory:
            memory_metrics: Optional[MethodMemoryMetrics] = r.get("memory_metrics")
            if memory_metrics:
                peak_str = format_bytes(memory_metrics.peak_rss_bytes)
                p95_str = format_bytes(memory_metrics.p95_rss_bytes)
            else:
                peak_str = "N/A"
                p95_str = "N/A"
            row_parts.extend([f"{peak_str:>10}", f"{p95_str:>10}"])
        
        print("  ".join(row_parts))
    
    # Legend
    if any(approach_lookup.get(r["method"]) for r in all_results):
        print()
        for r in all_results:
            if approach_lookup.get(r["method"]):
                print(f"{r['method']:<{max_method_len}}  → {approach_lookup[r['method']]}")


# --- Memory Profiling Display Functions ---

def print_memory_trace(all_results: List[Dict[str, Any]]) -> None:
    """
    Print run-level memory traces for each method.
    
    Per Cli_Output_Memory.md Section 3:
    - Shows one sparkline per method
    - Does NOT print case-level traces by default
    - Applies strictly to active_methods
    """
    print()
    print("Memory Trace (Run-level RSS)")
    print()
    
    for r in all_results:
        method = r["method"]
        memory_metrics: Optional[MethodMemoryMetrics] = r.get("memory_metrics")
        
        if not memory_metrics or not memory_metrics.case_metrics:
            print(f"{method}:")
            print("   N/A (no memory data)")
            continue
        
        # Collect RSS samples from case metrics
        rss_samples = [m.peak_rss_bytes for m in memory_metrics.case_metrics 
                       if m.peak_rss_bytes is not None]
        
        if not rss_samples:
            print(f"{method}:")
            print("   N/A (RSS measurement unavailable)")
            continue
        
        # Generate sparkline
        trace = generate_memory_trace(rss_samples)
        peak_str = format_bytes(memory_metrics.peak_rss_bytes)
        p95_str = format_bytes(memory_metrics.p95_rss_bytes)
        
        print(f"{method}:")
        print(f"{trace}")
        print(f"Peak {peak_str} | P95 {p95_str}")
        print()


def print_memory_per_case(all_results: List[Dict[str, Any]], top_k: int = 5) -> None:
    """
    Print case-level memory debugging info.
    
    Per Cli_Output_Memory.md Section 4:
    - Debug-only flag
    - Compact method-level summary first
    - Then Top-K cases by peak RSS
    """
    print()
    
    for r in all_results:
        method = r["method"]
        memory_metrics: Optional[MethodMemoryMetrics] = r.get("memory_metrics")
        
        if not memory_metrics or not memory_metrics.case_metrics:
            print(f"Case Memory Summary ({method})")
            print("N/A (no memory data)")
            print()
            continue
        
        # Method-level summary
        total_cases = len(memory_metrics.case_metrics)
        valid_cases = [m for m in memory_metrics.case_metrics if m.peak_rss_bytes is not None]
        
        if not valid_cases:
            print(f"Case Memory Summary ({method})")
            print(f"cases={total_cases} | Peak=N/A | P95=N/A | Median=N/A")
            print()
            continue
        
        # Calculate median
        sorted_rss = sorted(m.peak_rss_bytes for m in valid_cases if m.peak_rss_bytes)
        median_rss = sorted_rss[len(sorted_rss) // 2] if sorted_rss else None
        
        print(f"Case Memory Summary ({method})")
        print(f"cases={total_cases} | Peak={format_bytes(memory_metrics.peak_rss_bytes)} | "
              f"P95={format_bytes(memory_metrics.p95_rss_bytes)} | "
              f"Median={format_bytes(median_rss)}")
        print()
        
        # Top K cases table
        top_cases = memory_metrics.get_top_cases(top_k)
        if top_cases:
            print(f"Top {len(top_cases)} memory cases (by peak RSS):")
            print()
            print(f"{'Rank':<5} | {'Case ID':<12} | {'Case Peak RSS':>14} | {'Time':>8} | {'Input Bytes':>12}")
            print(f"{'-'*5}-+-{'-'*12}-+-{'-'*14}-+-{'-'*8}-+-{'-'*12}")
            
            for rank, case in enumerate(top_cases, 1):
                rss_str = format_bytes(case.peak_rss_bytes)
                time_str = f"{case.elapsed_ms:.1f}ms"
                input_str = format_bytes(case.input_bytes)
                print(f"{rank:<5} | {case.case_name:<12} | {rss_str:>14} | {time_str:>8} | {input_str:>12}")
        
        print()


def print_trace_compare(all_results: List[Dict[str, Any]]) -> None:
    """
    Print multi-method memory comparison.
    
    Per Cli_Output_Memory.md Section 5:
    - Memory Ranking Table (primary output)
    - Supporting traces (secondary)
    - Effective when active_methods > 1
    """
    if len(all_results) < 2:
        print()
        print("Memory Comparison Summary")
        print("(Single method - use --memory-trace for detailed view)")
        print()
        return
    
    print()
    print("Memory Comparison Summary")
    print()
    
    # Collect and sort by Peak RSS
    method_data = []
    for r in all_results:
        method = r["method"]
        memory_metrics: Optional[MethodMemoryMetrics] = r.get("memory_metrics")
        
        if memory_metrics and memory_metrics.peak_rss_bytes is not None:
            method_data.append({
                "method": method,
                "peak_rss": memory_metrics.peak_rss_bytes,
                "p95_rss": memory_metrics.p95_rss_bytes,
                "stability": memory_metrics.stability_percent,
                "stability_class": memory_metrics.stability_classification,
                "metrics": memory_metrics,
            })
        else:
            method_data.append({
                "method": method,
                "peak_rss": None,
                "p95_rss": None,
                "stability": None,
                "stability_class": "N/A",
                "metrics": memory_metrics,
            })
    
    # Sort by peak RSS (None values at end)
    method_data.sort(key=lambda x: (x["peak_rss"] is None, x["peak_rss"] or 0))
    
    # Find best (lowest) peak RSS for delta calculation
    best_peak = None
    for m in method_data:
        if m["peak_rss"] is not None:
            best_peak = m["peak_rss"]
            break
    
    # Print ranking table
    max_method_len = max(len(m["method"]) for m in method_data)
    
    print(f"{'Rank':<5} | {'Method':<{max_method_len}} | {'Peak RSS':>10} | {'P95 RSS':>10} | "
          f"{'Δ Peak (vs best)':>18} | {'Stability':>20} | Notes")
    print(f"{'-'*5}-+-{'-'*max_method_len}-+-{'-'*10}-+-{'-'*10}-+-{'-'*18}-+-{'-'*20}-+-{'-'*15}")
    
    for rank, m in enumerate(method_data, 1):
        method = m["method"]
        peak_str = format_bytes(m["peak_rss"])
        p95_str = format_bytes(m["p95_rss"])
        
        # Calculate delta vs best
        if m["peak_rss"] is not None and best_peak is not None:
            delta_bytes = m["peak_rss"] - best_peak
            delta_pct = (delta_bytes / best_peak * 100) if best_peak > 0 else 0
            delta_str = f"+{format_bytes(delta_bytes)} ({delta_pct:+.0f}%)" if delta_bytes > 0 else "+0B (0%)"
        else:
            delta_str = "N/A"
        
        # Stability with percentage
        if m["stability"] is not None:
            stability_str = f"{m['stability_class']} (Δ={m['stability']:.1f}%)"
        else:
            stability_str = "N/A"
        
        # Notes
        notes = ""
        if m["stability"] is not None and m["stability"] > 15:
            notes = "higher spikes"
        
        print(f"{rank:<5} | {method:<{max_method_len}} | {peak_str:>10} | {p95_str:>10} | "
              f"{delta_str:>18} | {stability_str:>20} | {notes}")
    
    # Supporting traces
    print()
    print("Memory Trace Comparison (Run-level RSS)")
    print()
    
    max_method_len = max(len(m["method"]) for m in method_data)
    
    for m in method_data:
        method = m["method"]
        metrics = m["metrics"]
        
        if metrics and metrics.case_metrics:
            rss_samples = [c.peak_rss_bytes for c in metrics.case_metrics 
                          if c.peak_rss_bytes is not None]
            if rss_samples:
                trace = generate_memory_trace(rss_samples)
                print(f"{method:<{max_method_len}} : {trace}")
            else:
                print(f"{method:<{max_method_len}} : N/A")
        else:
            print(f"{method:<{max_method_len}} : N/A")
    
    print()
