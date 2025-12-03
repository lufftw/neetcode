# solutions/xxxx_problem_name.py
"""
題目: [Problem Name]
連結: https://leetcode.com/problems/xxx/
"""
from typing import List, Optional


class Solution:
    def solve(self, *args):
        """
        TODO: 實作你的解法
        """
        pass


def solve():
    """
    從 stdin 讀取輸入，呼叫 Solution，輸出答案。
    Parse input from stdin, call Solution, print output.
    """
    import sys
    data = sys.stdin.read().strip().split('\n')
    
    # TODO: 根據題目格式解析輸入
    # Example for Two Sum:
    # nums = list(map(int, data[0].strip('[]').split(',')))
    # target = int(data[1])
    
    sol = Solution()
    # result = sol.solve(...)
    
    # TODO: 輸出答案
    # print(result)


if __name__ == "__main__":
    solve()

