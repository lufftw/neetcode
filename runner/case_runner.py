# runner/case_runner.py
"""
Single Case Runner - Run a single test case for debugging.
"""
import subprocess
import os
import sys
from typing import Optional

PYTHON_EXE = sys.executable

def main(argv: list[str]) -> None:
    """
    Run a single test case without comparison (for debugging).
    
    Usage:
        python runner/case_runner.py 0001_two_sum 1
    
    This will run:
        solutions/0001_two_sum.py
    With stdin from:
        tests/0001_two_sum_1.in
    Output is displayed directly in terminal (no comparison).
    """

    if len(argv) < 3:
        print("Usage: python runner/case_runner.py <problem_name> <case_index>")
        print("Example: python runner/case_runner.py 0001_two_sum 1")
        sys.exit(1)

    problem = argv[1]
    case_idx = argv[2]

    tests_dir = "tests"
    in_path = os.path.join(tests_dir, f"{problem}_{case_idx}.in")

    if not os.path.exists(in_path):
        print(f"❌ Test input file not found: {in_path}")
        sys.exit(1)

    solution_path = os.path.join("solutions", f"{problem}.py")
    if not os.path.exists(solution_path):
        print(f"❌ Solution file not found: {solution_path}")
        sys.exit(1)

    with open(in_path, "r", encoding="utf-8") as f:
        input_data = f.read()

    print(f"=== Running {problem}, case #{case_idx} ===")
    print(f"Input file: {in_path}")
    print()

    result = subprocess.run(
        [PYTHON_EXE, solution_path],
        input=input_data,
        text=True,
        capture_output=False  # Display output directly in terminal
    )

if __name__ == "__main__":
    main(sys.argv)