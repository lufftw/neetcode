#!/usr/bin/env python3
"""
Collect benchmark data from all multi-solution problems.
Outputs JSON for further processing.
"""
import subprocess
import json
import re
import sys
import os
from pathlib import Path

# Fix Windows encoding issues
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"

PROJECT_ROOT = Path(__file__).parent.parent
SOLUTIONS_DIR = PROJECT_ROOT / "solutions"

def find_multi_solution_problems():
    """Find all solution files with multiple methods."""
    problems = []
    for sol_file in sorted(SOLUTIONS_DIR.glob("*.py")):
        if sol_file.name.startswith("_"):
            continue
        content = sol_file.read_text(encoding="utf-8")
        # Count "class": occurrences in SOLUTIONS dict
        class_count = len(re.findall(r'"class":', content))
        if class_count >= 2:
            problem_name = sol_file.stem
            problems.append((problem_name, class_count))
    return problems

def run_benchmark(problem_name):
    """Run benchmark and parse results."""
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "runner" / "test_runner.py"),
        problem_name,
        "--all",
        "--benchmark"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(PROJECT_ROOT),
            encoding="utf-8",
            errors="replace"
        )
        return parse_benchmark_output(result.stdout)
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except Exception as e:
        return {"error": str(e)}

def parse_benchmark_output(output):
    """Parse benchmark output to extract method data."""
    methods = []

    # Pattern for performance table rows
    # Method          Avg Time   Pass Rate  Complexity    Peak RSS
    table_pattern = r"^(\w+)\s+(\d+\.?\d*)\s*ms\s+(\d+/\d+)\s+(.+?)(?:\s+\d+\.?\d*MB)?\s*$"

    for line in output.split("\n"):
        line = line.strip()
        match = re.match(table_pattern, line)
        if match:
            method_name = match.group(1)
            avg_time = float(match.group(2))
            pass_rate = match.group(3)
            complexity = match.group(4).strip()

            methods.append({
                "method": method_name,
                "avg_time_ms": avg_time,
                "pass_rate": pass_rate,
                "complexity": complexity
            })

    return {"methods": methods} if methods else {"error": "no data parsed", "raw": output[:500]}

def main():
    print("Finding multi-solution problems...")
    problems = find_multi_solution_problems()
    print(f"Found {len(problems)} problems with multiple solutions\n")

    results = {}

    for i, (problem_name, method_count) in enumerate(problems):
        print(f"[{i+1}/{len(problems)}] {problem_name} ({method_count} methods)...", end=" ", flush=True)

        data = run_benchmark(problem_name)

        if "error" in data:
            print(f"[ERROR] {data['error']}")
        else:
            methods = data.get("methods", [])
            if methods:
                times = [m["avg_time_ms"] for m in methods]
                fastest = min(methods, key=lambda x: x["avg_time_ms"])
                slowest = max(methods, key=lambda x: x["avg_time_ms"])
                print(f"[OK] {len(methods)} methods, {fastest['method']}={fastest['avg_time_ms']:.1f}ms (fastest)")
            else:
                print("[WARN] no methods parsed")

        results[problem_name] = {
            "method_count": method_count,
            "benchmark": data
        }

    # Save results
    output_file = PROJECT_ROOT / "docs" / "benchmark_data.json"
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n[DONE] Results saved to {output_file}")

if __name__ == "__main__":
    main()
