# solutions/_runner.py
"""
Runner utilities for solution files.

Usage:
    from _runner import get_solver, auto_shape
    
    def solve():
        # Parse input
        nums = [1, 2, 3, 4, 5]
        target = 9
        
        # Automatically report shapes of all local variables (PyTorch-style)
        auto_shape()  # → "nums: [5], target: scalar"
        
        # Run solver
        solver = get_solver(SOLUTIONS)
        result = solver.twoSum(nums, target)

This module handles path setup automatically, so you don't need to
worry about sys.path manipulation in your solution files.
"""
import sys
import os
import inspect
import json
from typing import Any, Dict, List, Optional, get_type_hints

# Auto-setup project root path
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# Shape protocol markers
_SHAPE_START = "__SHAPE__:"
_SHAPE_END = "__END_SHAPE__"

# Only emit shape data if runner is listening (reduces terminal noise)
_SHAPE_ENABLED = os.environ.get('NEETCODE_SHAPE_REPORT', '0') == '1'


def _compute_shape(value: Any, name: str = "") -> Dict[str, Any]:
    """
    Compute PyTorch-style shape of a value.
    
    Returns dict with shape info like:
    - {'shape': [5]} for list of 5 elements
    - {'shape': [3, 4]} for 3x4 matrix
    - {'shape': [3], 'total': 8} for 3 lists with 8 total elements
    - {'value': 42} for scalar
    """
    if value is None:
        return {'shape': None}
    
    # Scalar types - shape is () like PyTorch 0-dim tensor
    if isinstance(value, (int, float, bool)):
        return {'shape': [], 'dtype': type(value).__name__}  # [] = scalar
    
    # String
    if isinstance(value, str):
        return {'shape': [len(value)], 'dtype': 'str'}
    
    # List or Tuple
    if isinstance(value, (list, tuple)):
        if not value:
            return {'shape': [0]}
        
        first = value[0]
        
        # Nested list (matrix or k-lists)
        if isinstance(first, (list, tuple)):
            outer_len = len(value)
            inner_lens = [len(x) for x in value if isinstance(x, (list, tuple))]
            total = sum(inner_lens)
            
            # Uniform matrix (all same length AND length > 0)
            # If inner length is 0, treat as k-lists with empty sublists
            if inner_lens and inner_lens[0] > 0 and all(l == inner_lens[0] for l in inner_lens):
                return {'shape': [outer_len, inner_lens[0]]}
            else:
                # Variable-length sublists OR empty sublists (k-lists pattern)
                return {'shape': [outer_len], 'total': total}
        
        # Simple 1D list
        return {'shape': [len(value)]}
    
    # Dict
    if isinstance(value, dict):
        # Check if adjacency list pattern
        if value and all(isinstance(v, (list, tuple)) for v in value.values()):
            E = sum(len(adj) for adj in value.values())
            return {'shape': [len(value)], 'edges': E, 'dtype': 'adj_list'}
        return {'shape': [len(value)], 'dtype': 'dict'}
    
    # Set
    if isinstance(value, (set, frozenset)):
        return {'shape': [len(value)], 'dtype': 'set'}
    
    # Linked List (duck typing)
    if hasattr(value, 'next') and hasattr(value, 'val'):
        count = 0
        node = value
        while node:
            count += 1
            node = getattr(node, 'next', None)
        return {'shape': [count], 'dtype': 'LinkedList'}
    
    # Tree (duck typing)
    if hasattr(value, 'left') or hasattr(value, 'right'):
        nodes, height = _count_tree(value)
        return {'shape': [nodes], 'height': height, 'dtype': 'Tree'}
    
    # Unknown - try to get length
    try:
        return {'shape': [len(value)]}
    except TypeError:
        return {'type': type(value).__name__}


def _count_tree(root) -> tuple:
    """Count nodes and height of a tree."""
    if root is None:
        return 0, 0
    left_n, left_h = _count_tree(getattr(root, 'left', None))
    right_n, right_h = _count_tree(getattr(root, 'right', None))
    return 1 + left_n + right_n, 1 + max(left_h, right_h)


def auto_shape(*args, **named_values) -> None:
    """
    Automatically compute and report shapes of variables (PyTorch-style).
    
    Call this after parsing input. It inspects caller's local variables
    and reports their shapes automatically.
    
    Usage:
        nums = [1, 2, 3, 4, 5]
        target = 9
        auto_shape()  # Reports shapes of nums and target
        
        # Or explicitly specify which variables:
        auto_shape(nums, target)
        
        # Or with names:
        auto_shape(nums=nums, target=target)
    
    Output (to stderr):
        __SHAPE__:{"nums":{"shape":[5]},"target":{"value":9}}__END_SHAPE__
    """
    shapes = {}
    
    # If explicit values provided
    if named_values:
        for name, value in named_values.items():
            shapes[name] = _compute_shape(value, name)
    elif args:
        # Try to get variable names from caller's frame
        frame = inspect.currentframe().f_back
        local_vars = frame.f_locals
        
        for arg in args:
            # Find the variable name
            found_name = None
            for name, val in local_vars.items():
                if val is arg and not name.startswith('_'):
                    found_name = name
                    break
            
            if found_name:
                shapes[found_name] = _compute_shape(arg, found_name)
            else:
                shapes[f'arg{len(shapes)}'] = _compute_shape(arg)
    else:
        # Auto-detect from caller's local variables
        frame = inspect.currentframe().f_back
        local_vars = frame.f_locals
        
        # Filter out internal variables and modules
        for name, value in local_vars.items():
            if name.startswith('_'):
                continue
            if inspect.ismodule(value) or inspect.isfunction(value) or inspect.isclass(value):
                continue
            if name in ('sys', 'os', 'lines', 'i', 'k'):  # Skip common loop vars
                continue
            
            shapes[name] = _compute_shape(value, name)
    
    if shapes and _SHAPE_ENABLED:
        json_str = json.dumps(shapes, separators=(',', ':'))
        print(f"{_SHAPE_START}{json_str}{_SHAPE_END}", file=sys.stderr, flush=True)


def report_shape(shapes: dict = None, **kwargs) -> None:
    """
    Report input shapes manually (for backward compatibility).
    
    Prefer auto_shape() for automatic detection.
    """
    if shapes is None and kwargs:
        shapes = kwargs
    
    if not shapes or not _SHAPE_ENABLED:
        return
    
    json_str = json.dumps(shapes, separators=(',', ':'))
    print(f"{_SHAPE_START}{json_str}{_SHAPE_END}", file=sys.stderr, flush=True)


def shape(*dims, total: int = None) -> dict:
    """
    Helper to create shape dict (like torch.Size).
    
    Example:
        report_shape({
            'lists': shape(3, total=8),    # {'shape': [3], 'total': 8}
            'grid': shape(10, 20),          # {'shape': [10, 20]}
        })
    """
    result = {'shape': list(dims)}
    if total is not None:
        result['total'] = total
    return result


def get_solver(solutions_meta: dict, auto_report_shape: bool = True):
    """
    Get the solver instance for the currently selected solution method.
    
    Automatically reads SOLUTION_METHOD from environment and returns
    the appropriate class instance. Also automatically reports shapes
    of method parameters by matching local variable names to signature.
    
    Args:
        solutions_meta: The SOLUTIONS dictionary from the solution file
        auto_report_shape: If True, automatically report shapes of method parameters
    
    Returns:
        An instance of the selected solution class
    
    Example:
        # Shapes are automatically captured by matching signature params!
        nums1 = [1, 2, 3]
        nums2 = [4, 5, 6, 7]
        solver = get_solver(SOLUTIONS)  # ← Auto-reports: nums1:[3], nums2:[4]
        result = solver.findMedianSortedArrays(nums1, nums2)
    """
    # Get caller's frame for both globals and locals
    caller_frame = inspect.currentframe().f_back
    caller_globals = caller_frame.f_globals
    caller_locals = caller_frame.f_locals
    
    method_key = os.environ.get('SOLUTION_METHOD', 'default')
    info = solutions_meta.get(method_key, solutions_meta['default'])
    
    # Get solver class and method
    solver_class = caller_globals[info['class']]
    method_name = info['method']
    
    # Auto-report shapes by matching signature parameter names
    if auto_report_shape:
        _auto_report_shapes_from_signature(solver_class, method_name, caller_locals)
    
    return solver_class()


def _auto_report_shapes_from_signature(solver_class, method_name: str, local_vars: dict) -> None:
    """
    Automatically compute and report shapes by matching method signature parameters.
    
    Uses actual value inspection (like PyTorch tensor.shape) to detect:
    - 1D arrays: [n]
    - 2D matrices: [m, n]  
    - K-lists (variable sublists): [k] with total=sum
    """
    # Get the method
    method = getattr(solver_class, method_name, None)
    if method is None:
        return
    
    # Get parameter names from signature (this is reliable)
    try:
        sig = inspect.signature(method)
        param_names = [p for p in sig.parameters.keys() if p != 'self']
    except (ValueError, TypeError):
        return
    
    if not param_names:
        return
    
    # Match local variables to parameter names
    # Use _compute_shape which properly detects nested list structure
    shapes = {}
    for param_name in param_names:
        if param_name not in local_vars:
            continue
        
        value = local_vars[param_name]
        
        # Always use value-based shape detection (most reliable)
        shape_info = _compute_shape(value, param_name)
        
        # Only include non-scalar shapes
        shape = shape_info.get('shape')
        if shape is not None and len(shape) > 0:
            shapes[param_name] = shape_info
    
    # Report if we found any shapes (only if runner is listening)
    if shapes and _SHAPE_ENABLED:
        json_str = json.dumps(shapes, separators=(',', ':'))
        print(f"{_SHAPE_START}{json_str}{_SHAPE_END}", file=sys.stderr, flush=True)


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


__all__ = ['get_solver', 'get_solution_info', 'auto_shape', 'report_shape', 'shape']

