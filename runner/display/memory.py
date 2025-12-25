# runner/display/memory.py
"""
Memory Display - Memory profiling output functions.

Per Cli_Output_Memory.md:
- print_memory_trace: Run-level memory traces per method
- print_memory_per_case: Top-K cases by peak RSS (debug mode)
- print_trace_compare: Multi-method memory comparison with ranking
"""
from typing import List, Dict, Any, Optional

from runner.analysis.memory_profiler import (
    MethodMemoryMetrics,
    format_bytes,
    generate_memory_trace,
)
from runner.analysis.input_scale import format_input_scale, get_input_scale_legend

# Try to import tabulate for pretty tables
try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


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
    - First: Per-method case summary with Top-K
    - Last: Global Top-K across all methods (separate tables for RSS vs Alloc)
    """
    from runner.analysis.memory_profiler import CaseMemoryMetrics
    
    print()
    print("Memory Per-Case Analysis")
    print("=" * 60)
    
    # Collect ALL cases from ALL methods, separated by measurement type
    rss_cases: List[tuple] = []    # (method_name, case_metrics) - subprocess/psutil
    alloc_cases: List[tuple] = []  # (method_name, case_metrics) - in-process/tracemalloc
    
    # =========================================
    # 1. Per-method Case Memory Summary
    # =========================================
    for r in all_results:
        method = r["method"]
        memory_metrics: Optional[MethodMemoryMetrics] = r.get("memory_metrics")
        
        if not memory_metrics or not memory_metrics.case_metrics:
            print(f"\nCase Memory Summary ({method})")
            print("N/A (no memory data)")
            continue
        
        # Separate cases by measurement type
        method_rss_cases = []
        method_alloc_cases = []
        for c in memory_metrics.case_metrics:
            if c.peak_rss_bytes is not None:
                mtype = getattr(c, 'measurement_type', 'rss')
                if mtype == "alloc":
                    method_alloc_cases.append((method, c))
                    alloc_cases.append((method, c))
                else:
                    method_rss_cases.append((method, c))
                    rss_cases.append((method, c))
        
        if not method_rss_cases and not method_alloc_cases:
            print(f"\nCase Memory Summary ({method})")
            print("N/A (measurement unavailable)")
            continue
        
        # Print method summary
        print(f"\nCase Memory Summary ({method})")
        
        # RSS cases (subprocess)
        if method_rss_cases:
            method_rss_values = [c[1].peak_rss_bytes for c in method_rss_cases]
            rss_peak = max(method_rss_values)
            sorted_rss = sorted(method_rss_values)
            rss_p95 = sorted_rss[min(int(len(sorted_rss) * 0.95), len(sorted_rss) - 1)]
            rss_median = sorted_rss[len(sorted_rss) // 2]
            
            print(f"[RSS] cases={len(method_rss_cases)} | "
                  f"Peak={format_bytes(rss_peak)} | "
                  f"P95={format_bytes(rss_p95)} | "
                  f"Median={format_bytes(rss_median)}")
        
        # Alloc cases (tracemalloc)
        if method_alloc_cases:
            method_alloc_values = [c[1].peak_rss_bytes for c in method_alloc_cases]
            alloc_peak = max(method_alloc_values)
            sorted_alloc = sorted(method_alloc_values)
            alloc_p95 = sorted_alloc[min(int(len(sorted_alloc) * 0.95), len(sorted_alloc) - 1)]
            alloc_median = sorted_alloc[len(sorted_alloc) // 2]
            
            print(f"[Alloc] cases={len(method_alloc_cases)} | "
                  f"Peak={format_bytes(alloc_peak)} | "
                  f"P95={format_bytes(alloc_p95)} | "
                  f"Median={format_bytes(alloc_median)}")
        
        # Print Top-K for RSS cases
        if method_rss_cases:
            print()
            method_rss_cases.sort(key=lambda x: x[1].peak_rss_bytes or 0, reverse=True)
            top_rss = method_rss_cases[:top_k]
            
            print(f"Top {len(top_rss)} by Peak RSS (subprocess):")
            _print_case_table(top_rss, "Peak RSS")
        
        # Print Top-K for Alloc cases
        if method_alloc_cases:
            print()
            method_alloc_cases.sort(key=lambda x: x[1].peak_rss_bytes or 0, reverse=True)
            top_alloc = method_alloc_cases[:top_k]
            
            print(f"Top {len(top_alloc)} by Peak Alloc (in-process):")
            _print_case_table(top_alloc, "Peak Alloc")
    
    # =========================================
    # 2. Global Top-K (separate tables)
    # =========================================
    print()
    print("=" * 60)
    print(f"Global Summary")
    
    # Global RSS summary
    if rss_cases:
        all_rss_values = [c[1].peak_rss_bytes for c in rss_cases]
        print(f"[RSS] {len(rss_cases)} cases | "
              f"Peak={format_bytes(max(all_rss_values))} | "
              f"Median={format_bytes(sorted(all_rss_values)[len(all_rss_values)//2])}")
    
    # Global Alloc summary
    if alloc_cases:
        all_alloc_values = [c[1].peak_rss_bytes for c in alloc_cases]
        print(f"[Alloc] {len(alloc_cases)} cases | "
              f"Peak={format_bytes(max(all_alloc_values))} | "
              f"Median={format_bytes(sorted(all_alloc_values)[len(all_alloc_values)//2])}")
    
    # Global Top-K for RSS
    if rss_cases:
        print()
        rss_cases.sort(key=lambda x: x[1].peak_rss_bytes or 0, reverse=True)
        top_global_rss = rss_cases[:top_k]
        
        print(f"Top {len(top_global_rss)} by Peak RSS (subprocess, across all methods):")
        _print_global_case_table(top_global_rss, "Peak RSS")
    
    # Global Top-K for Alloc
    if alloc_cases:
        print()
        alloc_cases.sort(key=lambda x: x[1].peak_rss_bytes or 0, reverse=True)
        top_global_alloc = alloc_cases[:top_k]
        
        print(f"Top {len(top_global_alloc)} by Peak Alloc (in-process, across all methods):")
        _print_global_case_table(top_global_alloc, "Peak Alloc")
    
    if not rss_cases and not alloc_cases:
        print("N/A (no memory data collected)")
    
    print()
    
    # Print legend once at the very end
    print(get_input_scale_legend())
    print()


def _print_case_table(cases: List[tuple], metric_name: str) -> None:
    """Print a per-method case table."""
    print()
    headers = ["Rank", "Case ID", metric_name, "Time", "Input Scale", "Input Bytes"]
    rows = []
    for rank, (_, case) in enumerate(cases, 1):
        rows.append([
            rank,
            case.case_name,
            format_bytes(case.peak_rss_bytes),
            f"{case.elapsed_ms:.1f}ms",
            format_input_scale(case.input_scale),
            format_bytes(case.input_bytes),
        ])
    
    if HAS_TABULATE:
        print(tabulate(rows, headers=headers, tablefmt="simple"))
    else:
        max_case = max(len(r[1]) for r in rows) if rows else 20
        print(f"{'Rank':<5} | {'Case ID':<{max_case}} | {metric_name:>14} | "
              f"{'Time':>10} | {'Input Scale':<20} | {'Input Bytes':>12}")
        print("-" * (5 + max_case + 14 + 10 + 20 + 12 + 15))
        for row in rows:
            print(f"{row[0]:<5} | {row[1]:<{max_case}} | {row[2]:>14} | "
                  f"{row[3]:>10} | {row[4]:<20} | {row[5]:>12}")


def _print_global_case_table(cases: List[tuple], metric_name: str) -> None:
    """Print a global case table with method column."""
    print()
    headers = ["Rank", "Method", "Case ID", metric_name, "Time", "Input Scale", "Input Bytes"]
    rows = []
    for rank, (method, case) in enumerate(cases, 1):
        rows.append([
            rank,
            method,
            case.case_name,
            format_bytes(case.peak_rss_bytes),
            f"{case.elapsed_ms:.1f}ms",
            format_input_scale(case.input_scale),
            format_bytes(case.input_bytes),
        ])
    
    if HAS_TABULATE:
        print(tabulate(rows, headers=headers, tablefmt="simple"))
    else:
        max_method = max(len(r[1]) for r in rows) if rows else 10
        max_case = max(len(r[2]) for r in rows) if rows else 20
        print(f"{'Rank':<5} | {'Method':<{max_method}} | {'Case ID':<{max_case}} | "
              f"{metric_name:>10} | {'Time':>10} | {'Input Scale':<20} | {'Input Bytes':>12}")
        print("-" * (5 + max_method + max_case + 10 + 10 + 20 + 12 + 18))
        for row in rows:
            print(f"{row[0]:<5} | {row[1]:<{max_method}} | {row[2]:<{max_case}} | "
                  f"{row[3]:>10} | {row[4]:>10} | {row[5]:<20} | {row[6]:>12}")


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
    
    # Build ranking table data
    headers = ["Rank", "Method", "Peak RSS", "P95 RSS", "Δ Peak (vs best)", "Stability", "Notes"]
    rows = []
    
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
        
        rows.append([rank, method, peak_str, p95_str, delta_str, stability_str, notes])
    
    # Print table
    if HAS_TABULATE:
        print(tabulate(rows, headers=headers, tablefmt="simple"))
    else:
        # Fallback to manual formatting
        max_method_len = max(len(m["method"]) for m in method_data)
        print(f"{'Rank':<5}  {'Method':<{max_method_len}}  {'Peak RSS':>10}  {'P95 RSS':>10}  "
              f"{'Δ Peak (vs best)':>18}  {'Stability':>20}  Notes")
        print("-" * (5 + max_method_len + 10 + 10 + 18 + 20 + 15 + 12))
        for row in rows:
            print(f"{row[0]:<5}  {row[1]:<{max_method_len}}  {row[2]:>10}  {row[3]:>10}  "
                  f"{row[4]:>18}  {row[5]:>20}  {row[6]}")
    
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


__all__ = [
    'print_memory_trace',
    'print_memory_per_case',
    'print_trace_compare',
]

