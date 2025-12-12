# solutions/_runner.py
"""
Runner utilities for solution files.

Usage:
    from _runner import get_solver
    
    def solve():
        solver = get_solver(SOLUTIONS)
        result = solver.twoSum(nums, target)  # Natural LeetCode-style call

This module handles path setup automatically, so you don't need to
worry about sys.path manipulation in your solution files.
"""
import sys
import os
import inspect

# Auto-setup project root path
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


def get_solver(solutions_meta: dict):
    """
    Get the solver instance for the currently selected solution method.
    
    Automatically reads SOLUTION_METHOD from environment and returns
    the appropriate class instance. No need to pass globals().
    
    Args:
        solutions_meta: The SOLUTIONS dictionary from the solution file
    
    Returns:
        An instance of the selected solution class
    
    Example:
        solver = get_solver(SOLUTIONS)
        result = solver.twoSum(nums, target)  # Natural method call
    """
    # Auto-capture caller's globals (no need to pass explicitly)
    caller_globals = inspect.currentframe().f_back.f_globals
    
    method_key = os.environ.get('SOLUTION_METHOD', 'default')
    info = solutions_meta.get(method_key, solutions_meta['default'])
    
    return caller_globals[info['class']]()


def get_solution_info(solutions_meta: dict) -> dict:
    """
    Get the solution info dict for the currently selected method.
    
    Useful for logging or debugging which solution is running.
    
    Args:
        solutions_meta: The SOLUTIONS dictionary from the solution file
    
    Returns:
        The info dict (contains 'class', 'method', 'complexity', etc.)
    """
    method_key = os.environ.get('SOLUTION_METHOD', 'default')
    return solutions_meta.get(method_key, solutions_meta['default'])


__all__ = ['get_solver', 'get_solution_info']

