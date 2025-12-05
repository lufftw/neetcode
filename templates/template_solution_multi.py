# solutions/xxxx_problem_name.py
"""
題目: [Problem Name]
連結: https://leetcode.com/problems/xxx/

多解法模板 - 支援 --all 和 --method 參數測試
"""
from typing import List, Optional
import os

# ============================================
# SOLUTIONS 定義（必須）
# 告訴 test_runner 有哪些解法可以測試
# ============================================
SOLUTIONS = {
    "default": {
        "method": "solve_optimal",      # 對應下方的方法名稱
        "complexity": "O(n)",           # 時間複雜度
        "description": "Optimal solution using hash map"
    },
    "bruteforce": {
        "method": "solve_bruteforce",
        "complexity": "O(n²)",
        "description": "Brute force approach"
    },
    # 可繼續新增更多解法...
}


class Solution:
    # ============================================
    # 解法一：最佳解
    # ============================================
    def solve_optimal(self, *args):
        """
        TODO: 實作最佳解法
        Time: O(n), Space: O(n)
        """
        pass
    
    # ============================================
    # 解法二：暴力解
    # ============================================
    def solve_bruteforce(self, *args):
        """
        TODO: 實作暴力解法
        Time: O(n²), Space: O(1)
        """
        pass


def solve():
    """
    從 stdin 讀取輸入，根據 SOLUTION_METHOD 環境變數選擇解法。
    """
    import sys
    
    # 讀取環境變數，決定要用哪個解法
    method_name = os.environ.get('SOLUTION_METHOD', 'default')
    
    # 取得對應的方法名稱
    method_info = SOLUTIONS.get(method_name, SOLUTIONS.get('default'))
    method_func_name = method_info['method']
    
    # 解析輸入
    data = sys.stdin.read().strip().split('\n')
    # TODO: 根據題目格式解析輸入
    
    sol = Solution()
    
    # 動態呼叫對應的解法
    method_func = getattr(sol, method_func_name)
    result = method_func()  # TODO: 傳入解析後的參數
    
    # 輸出答案
    print(result)


if __name__ == "__main__":
    solve()

