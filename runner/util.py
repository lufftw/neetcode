# runner/util.py
"""
共用工具函式 (Common Utilities)
"""
import os
import sys
from typing import Optional

# 專案根目錄
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 預設目錄
SOLUTIONS_DIR = os.path.join(PROJECT_ROOT, "solutions")
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "templates")


def normalize_output(s: str) -> str:
    """
    正規化輸出，移除多餘空白與換行。
    Normalize output by removing trailing whitespace and extra newlines.
    """
    lines = s.strip().splitlines()
    lines = [line.rstrip() for line in lines]
    return "\n".join(lines)


def get_solution_path(problem: str) -> str:
    """取得解答檔案路徑"""
    return os.path.join(SOLUTIONS_DIR, f"{problem}.py")


def get_test_input_path(problem: str, case_idx: int | str, tests_dir: Optional[str] = None) -> str:
    """取得測資輸入檔案路徑"""
    base_dir = tests_dir or TESTS_DIR
    return os.path.join(base_dir, f"{problem}_{case_idx}.in")


def get_test_output_path(problem: str, case_idx: int | str, tests_dir: Optional[str] = None) -> str:
    """取得測資輸出檔案路徑"""
    base_dir = tests_dir or TESTS_DIR
    return os.path.join(base_dir, f"{problem}_{case_idx}.out")


def read_file(path: str) -> str:
    """讀取檔案內容"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    """寫入檔案內容"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def file_exists(path: str) -> bool:
    """檢查檔案是否存在"""
    return os.path.exists(path)


def compare_outputs(expected: str, actual: str) -> bool:
    """
    比較兩個輸出是否相同（正規化後）。
    Compare two outputs after normalization.
    """
    return normalize_output(expected) == normalize_output(actual)


def print_diff(expected: str, actual: str) -> None:
    """印出 expected vs actual 的差異"""
    exp_norm = normalize_output(expected)
    act_norm = normalize_output(actual)
    
    print("--- Expected ---")
    print(exp_norm)
    print("--- Actual   ---")
    print(act_norm)


def get_python_exe() -> str:
    """取得目前使用的 Python 執行檔路徑"""
    return sys.executable

