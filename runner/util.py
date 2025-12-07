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


def compare_outputs(actual: str, expected: str, compare_mode: str = "exact") -> bool:
    """
    比較兩個輸出是否相同，支援多種比較模式。
    Compare two outputs with different comparison modes.
    
    Args:
        actual: 實際輸出
        expected: 預期輸出
        compare_mode: 比較模式
            - "exact": 精確比對（預設）
            - "sorted": 排序後比對（適用於 "return in any order" 題目）
            - "set": 集合比對（適用於不重複元素、順序無關）
    
    Returns:
        bool: 是否相符
    
    Examples:
        # N-Queens: order doesn't matter
        >>> compare_outputs("[['.Q..'], ['..Q.']]", "[['..Q.'], ['.Q..']]", "sorted")
        True
        
        # Two Sum: exact match required
        >>> compare_outputs("[0, 1]", "[1, 0]", "exact")
        False
    """
    import ast
    
    actual_norm = normalize_output(actual)
    expected_norm = normalize_output(expected)
    
    # 精確比對
    if compare_mode == "exact":
        return actual_norm == expected_norm
    
    # 嘗試解析為 Python 物件進行進階比對
    try:
        actual_obj = ast.literal_eval(actual_norm)
        expected_obj = ast.literal_eval(expected_norm)
        
        if compare_mode == "sorted":
            return _compare_sorted(actual_obj, expected_obj)
        
        elif compare_mode == "set":
            return _compare_set(actual_obj, expected_obj)
    
    except (ValueError, SyntaxError):
        # 無法解析時，退回精確比對
        pass
    
    return actual_norm == expected_norm


def _compare_sorted(actual: any, expected: any) -> bool:
    """
    排序後比對，支援巢狀 list。
    Sort and compare, supporting nested lists.
    
    Handles:
        - List[List[str]]: N-Queens, Permutations
        - List[List[int]]: Combination Sum, Subsets
        - List[int/str]: Simple lists
    """
    if not isinstance(actual, list) or not isinstance(expected, list):
        return actual == expected
    
    if len(actual) != len(expected):
        return False
    
    # 空 list
    if not actual:
        return True
    
    # 巢狀 list (e.g., N-Queens: List[List[str]])
    if isinstance(actual[0], list):
        # 將內層 list 轉為 tuple 以便排序
        try:
            actual_sorted = sorted(tuple(x) for x in actual)
            expected_sorted = sorted(tuple(x) for x in expected)
            return actual_sorted == expected_sorted
        except TypeError:
            # 無法排序時，退回直接比對
            return actual == expected
    
    # 單層 list
    try:
        return sorted(actual) == sorted(expected)
    except TypeError:
        return actual == expected


def _compare_set(actual: any, expected: any) -> bool:
    """
    集合比對，忽略重複與順序。
    Set comparison, ignoring duplicates and order.
    """
    if not isinstance(actual, list) or not isinstance(expected, list):
        return actual == expected
    
    # 巢狀 list - 轉為 frozenset of tuples
    if actual and isinstance(actual[0], list):
        try:
            actual_set = set(tuple(x) for x in actual)
            expected_set = set(tuple(x) for x in expected)
            return actual_set == expected_set
        except TypeError:
            return actual == expected
    
    # 單層 list
    try:
        return set(actual) == set(expected)
    except TypeError:
        return actual == expected


def compare_result(actual_str: str, expected_str: str, input_str: str,
                   module, compare_mode: str = "exact") -> bool:
    """
    整合比對邏輯，支援 JUDGE_FUNC 和 COMPARE_MODE。
    Integrated comparison logic supporting JUDGE_FUNC and COMPARE_MODE.
    
    優先級 / Priority:
        1. JUDGE_FUNC（使用者自訂驗證函式）
        2. COMPARE_MODE（框架提供：exact/sorted/set）
    
    Args:
        actual_str: 程式實際輸出（原始字串）
        expected_str: 預期輸出（原始字串）
        input_str: 輸入資料（原始字串）
        module: 載入的 solution 模組
        compare_mode: 比較模式 ("exact" | "sorted" | "set")
    
    Returns:
        bool: 是否正確
    
    JUDGE_FUNC 簽名 / Signature:
        def judge(actual, expected, input_data) -> bool
        
        - 若 actual/expected 可被 ast.literal_eval 解析，則傳入解析後的物件
        - 若無法解析，則傳入原始字串
        - input_data 永遠是原始字串
    
    Examples:
        # Decision Problem 驗證（物件模式）
        def judge(actual: list, expected: list, input_data: str) -> bool:
            n = int(input_data)
            return is_valid_solution(actual, n)
        
        # 自訂格式比對（字串模式）
        def judge(actual: str, expected: str, input_data: str) -> bool:
            return parse_linked_list(actual) == parse_linked_list(expected)
    """
    import ast
    
    actual_norm = normalize_output(actual_str)
    expected_norm = normalize_output(expected_str)
    
    # ========== 優先：JUDGE_FUNC ==========
    judge_func = getattr(module, 'JUDGE_FUNC', None) if module else None
    
    if judge_func:
        # 嘗試解析為 Python 物件
        try:
            actual_obj = ast.literal_eval(actual_norm)
            expected_obj = ast.literal_eval(expected_norm)
            # 成功解析 → 傳物件
            return judge_func(actual_obj, expected_obj, input_str)
        except (ValueError, SyntaxError):
            # 無法解析 → 傳原始字串
            return judge_func(actual_norm, expected_norm, input_str)
    
    # ========== 其次：COMPARE_MODE ==========
    return compare_outputs(actual_norm, expected_norm, compare_mode)


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

