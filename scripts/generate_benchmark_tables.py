#!/usr/bin/env python3
"""
Generate markdown tables from benchmark data.
Creates:
1. Main table (overview)
2. Appendix (full details)
3. Large n spotlight
4. ASCII box table for README
"""
import json
from pathlib import Path
from tabulate import tabulate

PROJECT_ROOT = Path(__file__).parent.parent


def load_benchmark_data():
    """Load small test benchmark data."""
    path = PROJECT_ROOT / "docs" / "benchmark_data.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def load_large_n_data():
    """Load large n complexity estimation data."""
    path = PROJECT_ROOT / "docs" / "large_n_data.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def get_complexity_diff(methods):
    """Extract complexity difference between fastest and slowest."""
    if len(methods) < 2:
        return "N/A"

    # Get fastest and slowest by time
    fastest = min(methods, key=lambda x: x["avg_time_ms"])
    slowest = max(methods, key=lambda x: x["avg_time_ms"])

    if fastest["complexity"] == slowest["complexity"]:
        return f"Same {fastest['complexity'].split(',')[0]}"

    fast_complexity = fastest["complexity"].split(",")[0].strip()
    slow_complexity = slowest["complexity"].split(",")[0].strip()

    return f"{fast_complexity} -> {slow_complexity}"


def generate_main_table(benchmark_data):
    """Generate main overview table."""
    rows = []

    for problem, data in sorted(benchmark_data.items()):
        methods = data.get("benchmark", {}).get("methods", [])
        if not methods or len(methods) < 2:
            continue

        # Find default, fastest, slowest
        default = next((m for m in methods if m["method"] == "default"), methods[0])
        fastest = min(methods, key=lambda x: x["avg_time_ms"])
        slowest = max(methods, key=lambda x: x["avg_time_ms"])

        # Calculate delta
        if fastest["avg_time_ms"] > 0:
            delta = (slowest["avg_time_ms"] - fastest["avg_time_ms"]) / fastest["avg_time_ms"] * 100
            delta_str = f"+{delta:.0f}%" if delta > 0 else f"{delta:.0f}%"
        else:
            delta_str = "N/A"

        # Add asterisk if slowest has better declared complexity
        # (counter-intuitive result)
        if slowest["avg_time_ms"] < default["avg_time_ms"]:
            delta_str += "*"

        complexity_diff = get_complexity_diff(methods)

        # Short problem name
        short_name = problem.split("_", 1)[1].replace("_", " ").title()[:20]

        rows.append({
            "num": problem.split("_")[0],
            "name": short_name,
            "n_methods": len(methods),
            "default": f"{default['method']} {default['avg_time_ms']:.0f}ms",
            "best": f"{fastest['method']} {fastest['avg_time_ms']:.0f}ms",
            "worst": f"{slowest['method']} {slowest['avg_time_ms']:.0f}ms",
            "delta": delta_str,
            "complexity": complexity_diff
        })

    return rows


def generate_large_n_spotlight(large_n_data, top_n=10):
    """Generate spotlight table for most dramatic speedups."""
    dramatic = []

    for problem, data in large_n_data.items():
        methods = data.get("estimate", {}).get("methods", [])
        if len(methods) < 2:
            continue

        fastest = min(methods, key=lambda x: x["time_n5000_ms"])
        slowest = max(methods, key=lambda x: x["time_n5000_ms"])

        if fastest["time_n5000_ms"] > 0:
            ratio = slowest["time_n5000_ms"] / fastest["time_n5000_ms"]
            if ratio > 10:  # Only include 10x+ speedups
                dramatic.append({
                    "problem": problem,
                    "fastest_method": fastest["method"],
                    "fastest_time": fastest["time_n5000_ms"],
                    "fastest_complexity": fastest.get("estimated_complexity", "?"),
                    "slowest_method": slowest["method"],
                    "slowest_time": slowest["time_n5000_ms"],
                    "slowest_complexity": slowest.get("estimated_complexity", "?"),
                    "ratio": ratio
                })

    # Sort by ratio
    dramatic.sort(key=lambda x: x["ratio"], reverse=True)
    return dramatic[:top_n]


def generate_appendix(benchmark_data):
    """Generate full appendix with all method details."""
    appendix = []

    for problem, data in sorted(benchmark_data.items()):
        methods = data.get("benchmark", {}).get("methods", [])
        if not methods:
            continue

        fastest = min(methods, key=lambda x: x["avg_time_ms"])
        slowest = max(methods, key=lambda x: x["avg_time_ms"])

        problem_entry = {
            "problem": problem,
            "method_count": len(methods),
            "methods": []
        }

        for m in sorted(methods, key=lambda x: x["avg_time_ms"]):
            entry = {
                "method": m["method"],
                "time": f"{m['avg_time_ms']:.1f}ms",
                "complexity": m["complexity"],
                "notes": []
            }
            if m["method"] == fastest["method"]:
                entry["notes"].append("fastest")
            if m["method"] == slowest["method"]:
                entry["notes"].append("slowest")
            if m["method"] == "default":
                entry["notes"].append("default")

            problem_entry["methods"].append(entry)

        appendix.append(problem_entry)

    return appendix


def format_main_table_markdown(rows):
    """Format main table as markdown."""
    lines = [
        "## Benchmark Summary (Small Test Data)",
        "",
        "| # | Problem | N | Default | Best | Worst | Δ Time | Complexity |",
        "|---|---------|---|---------|------|-------|--------|------------|"
    ]

    for r in rows:
        lines.append(
            f"| {r['num']} | {r['name']} | {r['n_methods']} | "
            f"{r['default']} | {r['best']} | {r['worst']} | "
            f"{r['delta']} | {r['complexity']} |"
        )

    lines.append("")
    lines.append("> `*` indicates counter-intuitive result where declared slower complexity runs faster on small test data.")
    lines.append("> This demonstrates that complexity != actual time for small inputs.")

    return "\n".join(lines)


def get_descriptive_method_name(problem, method):
    """Map method names to descriptive algorithm names."""
    # Problem-specific mappings for clarity
    mappings = {
        "0010_regular_expression_matching": {
            "recursive": "Top-down Memo",
            "default": "Bottom-up DP",
        },
        "0044_wildcard_matching": {
            "greedy": "Greedy Backtrack",
            "default": "2D DP Table",
        },
        "0011_container_with_most_water": {
            "optimized": "Two Pointers",
            "bruteforce": "Nested Loops",
        },
        "0016_3sum_closest": {
            "optimized": "Two Ptr+Prune",
            "default": "Two Ptr Basic",
        },
        "0001_two_sum": {
            "hash_map": "Hash Map",
            "bruteforce": "Nested Loops",
        },
        "0055_jump_game": {
            "default": "Greedy",
            "dp": "DP Array",
        },
        "0042_trapping_rain_water": {
            "twopointer": "Two Pointers",
            "dp": "Prefix Arrays",
        },
        "0023_merge_k_sorted_lists": {
            "default": "Heap Merge",
            "greedy": "Sequential",
        },
        "0033_search_in_rotated_sorted_array": {
            "binary_search": "Binary Search",
            "linear_scan": "Linear Scan",
        },
    }
    if problem in mappings and method in mappings[problem]:
        return mappings[problem][method]
    # Fallback: capitalize and clean up
    return method.replace("_", " ").title()[:15]


def format_time_human(ms):
    """Format milliseconds to human-readable time."""
    if ms < 1:
        return f"{ms:.2f}ms"
    elif ms < 1000:
        return f"{ms:.1f}ms"
    elif ms < 60000:
        return f"{ms/1000:.1f}s"
    else:
        return f"{ms/60000:.1f}min"


def format_speedup_human(ratio):
    """Format speedup ratio with human-readable comparison."""
    if ratio >= 10000:
        return f"**{ratio/1000:.0f},000x** faster"
    elif ratio >= 1000:
        return f"**{ratio:.0f}x** faster"
    else:
        return f"**{ratio:.0f}x** faster"


def format_spotlight_markdown(spotlight):
    """Format spotlight table as markdown."""
    lines = [
        "## Large N Spotlight (n=5000)",
        "",
        "When input size grows, algorithm choice becomes critical:",
        "",
        "| # | Problem | Fast | Slow | Speedup |",
        "|--:|---------|------|------|--------:|"
    ]

    for s in spotlight:
        short_name = s["problem"].split("_", 1)[1].replace("_", " ").title()[:22]
        fast_name = get_descriptive_method_name(s["problem"], s["fastest_method"])
        slow_name = get_descriptive_method_name(s["problem"], s["slowest_method"])
        fast_time = format_time_human(s["fastest_time"])
        slow_time = format_time_human(s["slowest_time"])
        speedup = format_speedup_human(s["ratio"])
        lines.append(
            f"| {s['problem'].split('_')[0]} | {short_name} | "
            f"{fast_name} ({fast_time}) | "
            f"{slow_name} ({slow_time}) | "
            f"{speedup} |"
        )

    # Add interpretation
    lines.append("")
    lines.append("> At n=5000, the wrong algorithm choice turns **milliseconds into minutes**.")
    lines.append("> Regular Expression Matching: Memoization finishes while you blink; 2D DP takes a coffee break.")

    return "\n".join(lines)


def get_complexity_from_benchmark(benchmark_data, problem, method):
    """Get time and space complexity from benchmark data."""
    if problem not in benchmark_data:
        return "?", "?"
    methods = benchmark_data[problem].get("benchmark", {}).get("methods", [])
    for m in methods:
        if m["method"] == method:
            # Parse "O(n) time, O(1) space       4.6MB"
            complexity = m.get("complexity", "")
            time_match = complexity.split(" time")[0] if " time" in complexity else "?"
            space_part = complexity.split("time,")[1] if "time," in complexity else ""
            space_match = space_part.split(" space")[0].strip() if " space" in space_part else "?"
            # Clean up complexity strings
            time_match = time_match.replace("*", "").strip()
            space_match = space_match.replace("extra", "").strip()
            return time_match, space_match
    return "?", "?"


def get_short_problem_name(problem):
    """Get shortened problem name for display."""
    name_map = {
        "0010_regular_expression_matching": "Regex Matching",
        "0044_wildcard_matching": "Wildcard Match",
        "0011_container_with_most_water": "Container Water",
        "0016_3sum_closest": "3Sum Closest",
        "0001_two_sum": "Two Sum",
        "0055_jump_game": "Jump Game",
        "0042_trapping_rain_water": "Trapping Rain",
        "0023_merge_k_sorted_lists": "Merge K Lists",
        "0033_search_in_rotated_sorted_array": "Search Rotated",
    }
    if problem in name_map:
        return name_map[problem]
    return problem.split("_", 1)[1].replace("_", " ").title()[:16]


def format_ascii_box_table(large_n_data, benchmark_data, top_n=10):
    """Generate ASCII box table for README using tabulate."""
    # Collect data
    table_data = []
    for problem, data in large_n_data.items():
        methods = data.get("estimate", {}).get("methods", [])
        if len(methods) < 2:
            continue

        fastest = min(methods, key=lambda x: x["time_n5000_ms"])
        slowest = max(methods, key=lambda x: x["time_n5000_ms"])

        if fastest["time_n5000_ms"] > 0:
            ratio = slowest["time_n5000_ms"] / fastest["time_n5000_ms"]
            if ratio >= 2:  # Only include 2x+ speedups
                fast_time_c, fast_space_c = get_complexity_from_benchmark(
                    benchmark_data, problem, fastest["method"])
                slow_time_c, slow_space_c = get_complexity_from_benchmark(
                    benchmark_data, problem, slowest["method"])

                # Format problem name
                prob_num = problem.split("_")[0]
                prob_name = get_short_problem_name(problem)

                # Format method names with times
                fast_name = get_descriptive_method_name(problem, fastest["method"])
                slow_name = get_descriptive_method_name(problem, slowest["method"])
                fast_time = format_time_human(fastest["time_n5000_ms"])
                slow_time = format_time_human(slowest["time_n5000_ms"])

                # Format speedup
                if ratio >= 1000:
                    speedup = f"{ratio/1000:.0f},000×"
                else:
                    speedup = f"{ratio:.0f}×"

                # Skip if missing complexity data
                if fast_time_c == "?" or slow_time_c == "?":
                    continue

                # Format complexity (simplify verbose strings)
                def simplify_complexity(c):
                    # Take first part before " worst" or " average"
                    if " worst" in c:
                        c = c.split(" worst")[0]
                    if " average" in c:
                        c = c.split(" average")[0]
                    return c.strip()

                time_c = f"{simplify_complexity(fast_time_c)} vs {simplify_complexity(slow_time_c)}"
                space_c = f"{fast_space_c} vs {slow_space_c}"

                table_data.append({
                    "ratio": ratio,
                    "row": [
                        f"{prob_num} {prob_name}",
                        f"{fast_name} {fast_time}",
                        f"{slow_name} {slow_time}",
                        speedup,
                        time_c,
                        space_c,
                    ]
                })

    # Sort by ratio descending
    table_data.sort(key=lambda x: x["ratio"], reverse=True)
    table_data = table_data[:top_n]

    # Extract rows for tabulate
    rows = [item["row"] for item in table_data]
    headers = ["Problem", "Fast", "Slow", "Speedup", "Time Complexity", "Space Complexity"]

    # Generate table with tabulate (simple_grid uses thin unicode box-drawing chars)
    table = tabulate(rows, headers=headers, tablefmt="simple_grid")

    return f"Benchmark Results (n = 5,000)\n{table}"


def format_appendix_markdown(appendix):
    """Format appendix as markdown."""
    lines = [
        "## Appendix: Full Solution Details",
        ""
    ]

    for entry in appendix:
        lines.append(f"### {entry['problem']} ({entry['method_count']} solutions)")
        lines.append("")
        lines.append("| Method | Time | Complexity | Notes |")
        lines.append("|--------|------|------------|-------|")

        for m in entry["methods"]:
            notes = ", ".join(m["notes"]) if m["notes"] else ""
            lines.append(f"| {m['method']} | {m['time']} | {m['complexity']} | {notes} |")

        lines.append("")

    return "\n".join(lines)


def main():
    print("Loading data...")
    benchmark_data = load_benchmark_data()
    large_n_data = load_large_n_data()

    print(f"Benchmark data: {len(benchmark_data)} problems")
    print(f"Large n data: {len(large_n_data)} problems")

    # Generate tables
    print("\nGenerating main table...")
    main_rows = generate_main_table(benchmark_data)
    main_md = format_main_table_markdown(main_rows)

    print("Generating spotlight...")
    spotlight = generate_large_n_spotlight(large_n_data, top_n=15)
    spotlight_md = format_spotlight_markdown(spotlight) if spotlight else "No large n data available yet."

    print("Generating appendix...")
    appendix = generate_appendix(benchmark_data)
    appendix_md = format_appendix_markdown(appendix)

    # Generate ASCII box table for README
    print("Generating ASCII table for README...")
    ascii_table = format_ascii_box_table(large_n_data, benchmark_data, top_n=10)
    ascii_path = PROJECT_ROOT / "docs" / "benchmark_ascii_table.txt"
    ascii_path.write_text(ascii_table, encoding="utf-8")
    print(f"ASCII table saved to {ascii_path}")

    # Combine into final document
    doc = f"""# Benchmark Results

This document contains benchmark data for all multi-solution problems in the NeetCode Practice Framework.

{spotlight_md}

---

{main_md}

---

{appendix_md}

---

## Methodology

- **Small test data**: Runs actual test cases from `tests/` directory
- **Large n data**: Uses `generate_for_complexity(n)` with n=5000
- **Times**: Median of 5 runs for large n, average for small tests
- **Environment**: Python 3.11

To reproduce:
```bash
python runner/test_runner.py <problem> --all --benchmark
python runner/test_runner.py <problem> --all --estimate
```
"""

    # Save
    output_path = PROJECT_ROOT / "docs" / "benchmarks.md"
    output_path.write_text(doc, encoding="utf-8")
    print(f"\n[DONE] Saved to {output_path}")


if __name__ == "__main__":
    main()
