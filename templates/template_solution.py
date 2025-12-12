# solutions/xxxx_problem_name.py
"""
Problem: [Problem Name]
Link: https://leetcode.com/problems/xxx/

Single-solution template with polymorphic architecture.
"""
from typing import List, Optional
from _runner import get_solver


# ============================================
# SOLUTIONS metadata (REQUIRED)
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "solve",              # TODO: Use LeetCode method name (e.g., twoSum)
        "complexity": "O(?)",
        "description": "TODO: Brief description",
    },
}


class Solution:
    def solve(self, *args):
        """
        TODO: Implement your solution
        
        Rename this method to match the LeetCode method name.
        Update the 'method' field in SOLUTIONS accordingly.
        """
        pass


def solve():
    """
    Parse input from stdin, call Solution, print output.
    """
    import sys
    data = sys.stdin.read().strip().split('\n')
    
    # TODO: Parse input according to problem format
    # Example for Two Sum:
    # nums = list(map(int, data[0].split(',')))
    # target = int(data[1])
    
    # Get solver instance (auto-selects based on SOLUTION_METHOD env var)
    solver = get_solver(SOLUTIONS)
    
    # Call method naturally - use the LeetCode method name
    # result = solver.solve(...)  # TODO: Change to actual method name
    
    # TODO: Print the result
    # print(result)


if __name__ == "__main__":
    solve()
