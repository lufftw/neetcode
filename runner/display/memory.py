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


__all__ = [
    'print_memory_trace',
    'print_memory_per_case',
    'print_trace_compare',
]

