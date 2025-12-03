# runner/test_runner.py
import subprocess
import glob
import os
import sys
from typing import Optional

PYTHON_EXE = sys.executable  # 用目前這個 Python 來跑

def normalize_output(s: str) -> str:
    """
    簡單正規化輸出，避免多餘空白/換行造成比對失敗。
    Simple normalization to avoid whitespace issues.
    """
    lines = s.strip().splitlines()
    lines = [line.rstrip() for line in lines]
    return "\n".join(lines)

def run_one_case(problem: str, input_path: str, output_path: str) -> bool:
    # 讀 input
    with open(input_path, "r", encoding="utf-8") as f:
        input_data = f.read()

    # 讀 expected
    with open(output_path, "r", encoding="utf-8") as f:
        expected = f.read()

    # 執行對應的 solution 檔案
    solution_path = os.path.join("solutions", f"{problem}.py")
    if not os.path.exists(solution_path):
        print(f"❌ 找不到解答檔案: {solution_path}")
        return False

    result = subprocess.run(
        [PYTHON_EXE, solution_path],
        input=input_data,
        text=True,
        capture_output=True
    )

    actual = result.stdout

    exp_norm = normalize_output(expected)
    act_norm = normalize_output(actual)

    case_name = os.path.basename(input_path)
    ok = (exp_norm == act_norm)

    print(f"=== {case_name} ===")
    if ok:
        print("✅ PASS")
    else:
        print("❌ WRONG ANSWER")
        print("--- Expected ---")
        print(exp_norm)
        print("--- Actual   ---")
        print(act_norm)
        if result.stderr:
            print("--- STDERR   ---")
            print(result.stderr.strip())
    print()
    return ok

def main(argv: list[str]) -> None:
    """
    用法 / Usage:
      python runner/test_runner.py 0001_two_sum
    或指定 tests 目錄（預設 tests/）:
      python runner/test_runner.py 0001_two_sum tests_alt
    """
    if len(argv) < 2:
        print("用法: python runner/test_runner.py <problem_name> [tests_dir]")
        print("Example: python runner/test_runner.py 0001_two_sum")
        sys.exit(1)

    problem = argv[1]
    tests_dir: str = argv[2] if len(argv) >= 3 else "tests"

    pattern = os.path.join(tests_dir, f"{problem}_*.in")
    input_files = sorted(glob.glob(pattern))
    if not input_files:
        print(f"⚠️ 找不到測資檔案 (no test inputs): {pattern}")
        sys.exit(1)

    total = len(input_files)
    passed = 0

    for in_path in input_files:
        out_path = in_path.replace(".in", ".out")
        if not os.path.exists(out_path):
            print(f"⚠️ 找不到對應的 output 檔: {out_path}")
            continue
        if run_one_case(problem, in_path, out_path):
            passed += 1

    print(f"測試結果 / Summary: {passed} / {total} cases passed.")

if __name__ == "__main__":
    main(sys.argv)