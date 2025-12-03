# runner/case_runner.py
import subprocess
import os
import sys
from typing import Optional

PYTHON_EXE = sys.executable

def main(argv: list[str]) -> None:
    """
    用法 / Usage:
      python runner/case_runner.py 0001_two_sum 1
    會跑:
      solutions/0001_two_sum.py
    並把:
      tests/0001_two_sum_1.in
    當 stdin 餵進去，輸出顯示在終端機上（不比對）。
    """

    if len(argv) < 3:
        print("用法: python runner/case_runner.py <problem_name> <case_index>")
        print("Example: python runner/case_runner.py 0001_two_sum 1")
        sys.exit(1)

    problem = argv[1]
    case_idx = argv[2]

    tests_dir = "tests"
    in_path = os.path.join(tests_dir, f"{problem}_{case_idx}.in")

    if not os.path.exists(in_path):
        print(f"❌ 找不到測資檔案: {in_path}")
        sys.exit(1)

    solution_path = os.path.join("solutions", f"{problem}.py")
    if not os.path.exists(solution_path):
        print(f"❌ 找不到解答檔案: {solution_path}")
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
        capture_output=False  # 直接顯示在 terminal
    )

if __name__ == "__main__":
    main(sys.argv)