# runner/display/benchmark.py
"""
Benchmark Display - Visual performance comparison output.

Provides:
- ASCII bar chart for performance comparison
- Detailed benchmark summary table
- Complexity display integration
"""
from typing import List, Dict, Any, Optional

from runner.display.reporter import get_box_chars
from runner.analysis.memory_profiler import MethodMemoryMetrics, format_bytes


def print_visual_benchmark(all_results: List[Dict[str, Any]], 
                           problem_name: str = "Performance Comparison",
                           bar_width: int = 20,
                           approach_mapping: Optional[Dict[str, dict]] = None) -> None:
    """Print a visual ASCII bar chart for performance comparison."""
    if not all_results:
        return
    
    chars = get_box_chars()
    
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
    # Column order per cli-output-contract.md:
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


__all__ = [
    'print_visual_benchmark',
    'print_benchmark_summary',
]

