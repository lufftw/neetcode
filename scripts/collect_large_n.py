#!/usr/bin/env python3
"""
Collect large-n complexity estimation data from problems with generators.
Only runs problems that have generate_for_complexity function.
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
GENERATORS_DIR = PROJECT_ROOT / "generators"

def find_problems_with_complexity_generator():
    """Find problems that have generate_for_complexity in their generator."""
    problems = []

    for gen_file in sorted(GENERATORS_DIR.glob("*.py")):
        if gen_file.name.startswith("_"):
            continue

        content = gen_file.read_text(encoding="utf-8")
        if "generate_for_complexity" in content:
            problem_name = gen_file.stem

            # Check if solution has multiple methods
            sol_file = SOLUTIONS_DIR / f"{problem_name}.py"
            if sol_file.exists():
                sol_content = sol_file.read_text(encoding="utf-8")
                class_count = len(re.findall(r'"class":', sol_content))
                if class_count >= 2:
                    problems.append((problem_name, class_count))

    return problems

def run_estimate(problem_name):
    """Run complexity estimation and parse results."""
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "runner" / "test_runner.py"),
        problem_name,
        "--all",
        "--estimate"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,  # 10 minutes max per problem
            cwd=str(PROJECT_ROOT),
            encoding="utf-8",
            errors="replace"
        )
        return parse_estimate_output(result.stdout)
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except Exception as e:
        return {"error": str(e)}

def parse_estimate_output(output):
    """Parse estimation output to extract method data."""
    methods = []
    current_method = None

    lines = output.split("\n")
    for i, line in enumerate(lines):
        # Match: 📌 Estimating: method_name
        if "Estimating:" in line:
            match = re.search(r"Estimating:\s+(\w+)", line)
            if match:
                current_method = match.group(1)

        # Match: n= 5000: 123.456ms
        if current_method and "n= 5000:" in line or "n=5000:" in line:
            match = re.search(r"n=\s*5000:\s+([\d.]+)ms", line)
            if match:
                time_ms = float(match.group(1))

                # Look for estimated complexity in next few lines
                estimated = None
                for j in range(i, min(i+5, len(lines))):
                    if "Estimated:" in lines[j]:
                        est_match = re.search(r"Estimated:\s+(O\([^)]+\))", lines[j])
                        if est_match:
                            estimated = est_match.group(1)
                        break

                methods.append({
                    "method": current_method,
                    "time_n5000_ms": time_ms,
                    "estimated_complexity": estimated
                })
                current_method = None

    return {"methods": methods} if methods else {"error": "no data parsed"}

def main():
    print("Finding problems with generate_for_complexity...")
    problems = find_problems_with_complexity_generator()
    print(f"Found {len(problems)} problems with complexity generators\n")

    results = {}

    for i, (problem_name, method_count) in enumerate(problems):
        print(f"[{i+1}/{len(problems)}] {problem_name} ({method_count} methods)...", flush=True)

        data = run_estimate(problem_name)

        if "error" in data:
            print(f"  [ERROR] {data['error']}")
        else:
            methods = data.get("methods", [])
            if methods:
                fastest = min(methods, key=lambda x: x["time_n5000_ms"])
                slowest = max(methods, key=lambda x: x["time_n5000_ms"])
                ratio = slowest["time_n5000_ms"] / fastest["time_n5000_ms"] if fastest["time_n5000_ms"] > 0 else 0
                print(f"  [OK] fastest: {fastest['method']}={fastest['time_n5000_ms']:.2f}ms")
                print(f"       slowest: {slowest['method']}={slowest['time_n5000_ms']:.2f}ms")
                print(f"       ratio: {ratio:.1f}x")
            else:
                print("  [WARN] no methods parsed")

        results[problem_name] = {
            "method_count": method_count,
            "estimate": data
        }

    # Save results
    output_file = PROJECT_ROOT / "docs" / "large_n_data.json"
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n[DONE] Results saved to {output_file}")

    # Print summary of most dramatic differences
    print("\n" + "="*60)
    print("TOP 10 MOST DRAMATIC SPEEDUPS (n=5000)")
    print("="*60)

    dramatic = []
    for problem, data in results.items():
        methods = data.get("estimate", {}).get("methods", [])
        if len(methods) >= 2:
            fastest = min(methods, key=lambda x: x["time_n5000_ms"])
            slowest = max(methods, key=lambda x: x["time_n5000_ms"])
            if fastest["time_n5000_ms"] > 0:
                ratio = slowest["time_n5000_ms"] / fastest["time_n5000_ms"]
                dramatic.append((problem, fastest, slowest, ratio))

    dramatic.sort(key=lambda x: x[3], reverse=True)

    for problem, fastest, slowest, ratio in dramatic[:10]:
        print(f"{problem}")
        print(f"  {fastest['method']}: {fastest['time_n5000_ms']:.2f}ms → {slowest['method']}: {slowest['time_n5000_ms']:.2f}ms = {ratio:.0f}x")

if __name__ == "__main__":
    main()
