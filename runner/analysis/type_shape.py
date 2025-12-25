# runner/analysis/type_shape.py
"""
Type-based Shape Inference - Infer shape structure from Python type hints.

Uses typing module's get_origin() and get_args() to understand type structure.
Combined with actual values, can compute precise shapes.

Example:
    nums: List[int]           → structure: [?]      (1D array)
    matrix: List[List[int]]   → structure: [?, ?]   (2D matrix)
    graph: Dict[int, List]    → structure: {V: ?, E: ?} (graph)
"""
from typing import (
    Any, Dict, List, Optional, Tuple, Union,
    get_type_hints, get_origin, get_args
)
import inspect


def infer_shape_from_type(type_hint) -> Dict[str, Any]:
    """
    Infer shape structure from a type hint.
    
    Returns a dict describing the expected structure:
    - 'dims': number of dimensions (0=scalar, 1=array, 2=matrix, etc.)
    - 'structure': description like '[?]', '[?, ?]', 'scalar'
    - 'element_type': inner element type name
    
    Examples:
        int → {'dims': 0, 'structure': 'scalar', 'element_type': 'int'}
        List[int] → {'dims': 1, 'structure': '[n]', 'element_type': 'int'}
        List[List[int]] → {'dims': 2, 'structure': '[m, n]', 'element_type': 'int'}
    """
    origin = get_origin(type_hint)
    args = get_args(type_hint)
    
    # Handle Optional[X] → extract X
    if origin is Union:
        # Filter out NoneType
        non_none_args = [a for a in args if a is not type(None)]
        if len(non_none_args) == 1:
            return infer_shape_from_type(non_none_args[0])
    
    # Scalar types
    if origin is None:
        type_name = getattr(type_hint, '__name__', str(type_hint))
        if type_name in ('int', 'float', 'bool', 'str'):
            if type_name == 'str':
                # String is like 1D array of chars
                return {'dims': 1, 'structure': '[n]', 'element_type': 'char'}
            return {'dims': 0, 'structure': 'scalar', 'element_type': type_name}
        # Unknown type - treat as opaque
        return {'dims': 0, 'structure': type_name, 'element_type': type_name}
    
    # List[X]
    if origin is list:
        if not args:
            return {'dims': 1, 'structure': '[n]', 'element_type': 'any'}
        
        inner = args[0]
        inner_info = infer_shape_from_type(inner)
        
        # List[List[...]] → 2D
        if inner_info['dims'] >= 1 and inner_info['structure'].startswith('['):
            return {
                'dims': inner_info['dims'] + 1,
                'structure': f"[k, {inner_info['structure'][1:]}",  # [k, n] or [k, m, n]
                'element_type': inner_info['element_type']
            }
        
        # List[scalar] → 1D
        return {
            'dims': 1,
            'structure': '[n]',
            'element_type': inner_info['element_type']
        }
    
    # Dict[K, V]
    if origin is dict:
        return {'dims': 1, 'structure': '{keys}', 'element_type': 'dict'}
    
    # Tuple[...]
    if origin is tuple:
        return {'dims': 1, 'structure': f'({len(args)})', 'element_type': 'tuple'}
    
    # Unknown generic
    return {'dims': 0, 'structure': str(type_hint), 'element_type': 'unknown'}


def get_method_param_shapes(method) -> Dict[str, Dict[str, Any]]:
    """
    Get shape structure for each parameter of a method from its type hints.
    
    Example:
        def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        
        Returns:
        {
            'nums1': {'dims': 1, 'structure': '[n]', 'element_type': 'int'},
            'nums2': {'dims': 1, 'structure': '[n]', 'element_type': 'int'}
        }
    """
    try:
        hints = get_type_hints(method)
    except Exception:
        # Can't get type hints - return empty
        return {}
    
    result = {}
    for param, type_hint in hints.items():
        if param == 'return':
            continue
        result[param] = infer_shape_from_type(type_hint)
    
    return result


def compute_shape_with_type(value: Any, type_hint) -> Dict[str, Any]:
    """
    Compute actual shape using both value and type hint.
    
    Type hint tells us the STRUCTURE, value tells us the DIMENSIONS.
    
    Example:
        value = [[1,2,3], [4,5,6]]
        type_hint = List[List[int]]
        → {'shape': [2, 3], 'structure': '[k, n]', 'total': 6}
    """
    type_info = infer_shape_from_type(type_hint)
    
    if value is None:
        return {'shape': None, 'structure': type_info['structure']}
    
    # Scalar
    if type_info['dims'] == 0:
        return {'shape': [], 'dtype': type_info['element_type']}
    
    # 1D: List[X] or str
    if type_info['dims'] == 1:
        if isinstance(value, (list, tuple, str)):
            return {
                'shape': [len(value)],
                'structure': type_info['structure'],
                'dtype': type_info['element_type']
            }
    
    # 2D: List[List[X]]
    if type_info['dims'] == 2:
        if isinstance(value, (list, tuple)) and value:
            outer_len = len(value)
            if isinstance(value[0], (list, tuple)):
                inner_lens = [len(x) for x in value if isinstance(x, (list, tuple))]
                total = sum(inner_lens)
                
                # Uniform (matrix) or variable (k-lists)?
                if inner_lens and all(l == inner_lens[0] for l in inner_lens) and inner_lens[0] > 0:
                    return {
                        'shape': [outer_len, inner_lens[0]],
                        'structure': type_info['structure'],
                        'dtype': type_info['element_type']
                    }
                else:
                    return {
                        'shape': [outer_len],
                        'total': total,
                        'structure': type_info['structure'],
                        'dtype': type_info['element_type']
                    }
    
    # Fallback: just report length
    try:
        return {'shape': [len(value)], 'structure': type_info['structure']}
    except TypeError:
        return {'shape': [], 'structure': type_info['structure']}


def format_typed_shape(shape_info: Dict[str, Any], param_name: str) -> str:
    """
    Format shape info for display.
    
    Example:
        {'shape': [3], 'structure': '[n]', 'dtype': 'int'}
        → 'nums:[3]'
        
        {'shape': [2, 3], 'structure': '[k, n]'}
        → 'matrix:[2x3]'
        
        {'shape': [3], 'total': 8, 'structure': '[k, n]'}
        → 'lists:[3]->n=8'
    """
    shape = shape_info.get('shape')
    total = shape_info.get('total')
    
    if shape is None:
        return f"{param_name}:None"
    
    if len(shape) == 0:
        # Scalar - skip
        return ""
    
    dim_str = 'x'.join(str(d) for d in shape)
    
    if total is not None:
        return f"{param_name}:[{dim_str}]->n={total}"
    
    return f"{param_name}:[{dim_str}]"


__all__ = [
    'infer_shape_from_type',
    'get_method_param_shapes',
    'compute_shape_with_type',
    'format_typed_shape',
]

