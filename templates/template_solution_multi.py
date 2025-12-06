# solutions/xxxx_problem_name.py
"""
Problem: [Problem Name]
Link: https://leetcode.com/problems/xxx/

Multi-solution template - Supports --all and --method parameters
"""
from typing import List, Optional
import os

# ============================================
# SOLUTIONS Definition (Required)
# Tells test_runner which solutions are available
# ============================================
SOLUTIONS = {
    "default": {
        "method": "solve_optimal",      # Corresponding method name below
        "complexity": "O(n)",           # Time complexity
        "description": "Optimal solution using hash map"
    },
    "bruteforce": {
        "method": "solve_bruteforce",
        "complexity": "O(n²)",
        "description": "Brute force approach"
    },
    # Add more solutions as needed...
}


class Solution:
    # ============================================
    # Solution 1: Optimal
    # ============================================
    def solve_optimal(self, *args):
        """
        TODO: Implement optimal solution
        Time: O(n), Space: O(n)
        """
        pass
    
    # ============================================
    # Solution 2: Brute Force
    # ============================================
    def solve_bruteforce(self, *args):
        """
        TODO: Implement brute force solution
        Time: O(n²), Space: O(1)
        """
        pass


def solve():
    """
    Parse input from stdin, select solution based on SOLUTION_METHOD env var.
    """
    import sys
    
    # Read environment variable to determine which solution to use
    method_name = os.environ.get('SOLUTION_METHOD', 'default')
    
    # Get the corresponding method name
    method_info = SOLUTIONS.get(method_name, SOLUTIONS.get('default'))
    method_func_name = method_info['method']
    
    # Parse input
    data = sys.stdin.read().strip().split('\n')
    # TODO: Parse input according to problem format
    
    sol = Solution()
    
    # Dynamically call the corresponding solution
    method_func = getattr(sol, method_func_name)
    result = method_func()  # TODO: Pass parsed parameters
    
    # Print the result
    print(result)


if __name__ == "__main__":
    solve()
