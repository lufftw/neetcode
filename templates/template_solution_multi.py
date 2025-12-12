# solutions/xxxx_problem_name.py
"""
Problem: [Problem Name]
Link: https://leetcode.com/problems/xxx/

Multi-solution template using polymorphic architecture.
- Multiple classes, each implementing the SAME method name
- Supports --all and --method parameters for testing
"""
from typing import List, Optional
from _runner import get_solver


# ============================================
# SOLUTIONS metadata (REQUIRED)
# Each entry MUST have 'class' and 'method' fields
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionOptimal",
        "method": "solve",              # TODO: Use LeetCode method name
        "complexity": "O(n)",
        "description": "Optimal solution using hash map",
    },
    "bruteforce": {
        "class": "SolutionBruteforce",
        "method": "solve",              # Same method name (polymorphism)
        "complexity": "O(n²)",
        "description": "Brute force approach",
    },
    # Add more solutions as needed...
}


# ============================================
# Solution 1: Optimal
# Time: O(n), Space: O(n)
# ============================================
class SolutionOptimal:
    def solve(self, *args):
        """
        TODO: Implement optimal solution
        
        Rename this method to match the LeetCode method name.
        """
        pass


# ============================================
# Solution 2: Brute Force
# Time: O(n²), Space: O(1)
# ============================================
class SolutionBruteforce:
    def solve(self, *args):
        """
        TODO: Implement brute force solution
        
        Use the SAME method name as SolutionOptimal (polymorphism).
        """
        pass


def solve():
    """
    Parse input from stdin, select solution based on SOLUTION_METHOD env var.
    """
    import sys
    data = sys.stdin.read().strip().split('\n')
    
    # TODO: Parse input according to problem format
    # Example:
    # nums = list(map(int, data[0].split(',')))
    # target = int(data[1])
    
    # Get solver instance (auto-selects based on SOLUTION_METHOD env var)
    solver = get_solver(SOLUTIONS)
    
    # Call method naturally - all classes use the same method name
    # result = solver.solve(...)  # TODO: Change to actual method name
    
    # TODO: Print the result
    # print(result)


if __name__ == "__main__":
    solve()
