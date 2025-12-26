# runner/analysis/input_shape.py
"""
Input Shape Analysis - PyTorch/TensorFlow-style shape description for LeetCode inputs.

Inspired by:
- PyTorch: tensor.shape → torch.Size([batch, channels, H, W])
- TensorFlow: tf.TensorSpec(shape=[None, 224, 224, 3])

For LeetCode problems, we describe input structure as named dimensions:
- List[int]           → Shape(n=1000)
- List[List[int]]     → Shape(k=3, n=8) or Shape(rows=10, cols=20)
- TreeNode            → Shape(nodes=15, height=4)
- Graph edges         → Shape(V=100, E=500)
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union, get_type_hints, get_origin, get_args
import inspect


@dataclass
class InputShape:
    """
    Named shape descriptor for algorithm inputs.
    
    Similar to torch.Size but with semantic names for algorithm analysis.
    
    Examples:
        InputShape(n=1000)                    # 1D array
        InputShape(n=100, m=200)              # Two arrays
        InputShape(rows=10, cols=20, n=200)   # Matrix
        InputShape(k=3, n=8)                  # k lists, n total elements
        InputShape(V=100, E=500)              # Graph
        InputShape(nodes=15, height=4)        # Tree
    """
    # Primary dimensions
    n: Optional[int] = None          # Main size (array length, total elements)
    m: Optional[int] = None          # Secondary size
    
    # Matrix/Grid
    rows: Optional[int] = None
    cols: Optional[int] = None
    
    # Graph
    V: Optional[int] = None          # Vertices
    E: Optional[int] = None          # Edges
    
    # Tree
    nodes: Optional[int] = None
    height: Optional[int] = None
    
    # Collection of collections
    k: Optional[int] = None          # Number of sub-collections
    
    # Additional dimensions
    d: Optional[int] = None          # Dimensionality (for points)
    u: Optional[int] = None          # Unique keys (for dicts)
    
    # Raw info
    dtype: Optional[str] = None      # Element type hint
    
    def __repr__(self) -> str:
        """Format like PyTorch: Shape(n=1000, m=200)"""
        parts = []
        for name in ['n', 'm', 'k', 'rows', 'cols', 'V', 'E', 'nodes', 'height', 'd', 'u']:
            val = getattr(self, name)
            if val is not None:
                parts.append(f"{name}={val}")
        return f"Shape({', '.join(parts)})" if parts else "Shape()"
    
    def to_dict(self) -> Dict[str, int]:
        """Convert to dict for storage/display."""
        return {k: v for k, v in self.__dict__.items() 
                if v is not None and k != 'dtype'}
    
    def format(self) -> str:
        """Format for CLI display: 'n=1000, m=200'"""
        d = self.to_dict()
        if not d:
            return "N/A"
        # Priority order
        order = ['n', 'm', 'k', 'rows', 'cols', 'V', 'E', 'nodes', 'height', 'd', 'u']
        parts = [f"{k}={d[k]}" for k in order if k in d]
        return ', '.join(parts)


# ============================================================================
# Shape Inference from Values
# ============================================================================

def infer_shape(value: Any, type_hint: Optional[type] = None) -> InputShape:
    """
    Infer InputShape from a Python value.
    
    Like calling tensor.shape in PyTorch, but for algorithm inputs.
    
    Args:
        value: The actual input value
        type_hint: Optional type annotation for better inference
        
    Returns:
        InputShape with appropriate dimensions filled
        
    Examples:
        >>> infer_shape([1, 2, 3, 4, 5])
        Shape(n=5)
        
        >>> infer_shape([[1,2], [3,4], [5,6]])
        Shape(rows=3, cols=2, n=6)
        
        >>> infer_shape({'a': [1,2], 'b': [3]})  # adjacency list
        Shape(V=2, E=3)
    """
    shape = InputShape()
    
    if value is None:
        return shape
    
    # String
    if isinstance(value, str):
        shape.n = len(value)
        shape.dtype = 'str'
        return shape
    
    # List or Tuple
    if isinstance(value, (list, tuple)):
        if not value:
            shape.n = 0
            return shape
        
        first = value[0]
        
        # List[List[...]] - could be matrix, k-lists, intervals, points
        if isinstance(first, (list, tuple)):
            outer_len = len(value)
            
            # Check if it's a uniform matrix (all rows same length)
            inner_lens = [len(x) for x in value if isinstance(x, (list, tuple))]
            if inner_lens and all(l == inner_lens[0] for l in inner_lens):
                # Uniform matrix/grid
                shape.rows = outer_len
                shape.cols = inner_lens[0]
                shape.n = outer_len * inner_lens[0]
            else:
                # Variable-length sublists (k lists)
                shape.k = outer_len
                shape.n = sum(inner_lens)
            
            return shape
        
        # List[int/float/str] - simple 1D array
        shape.n = len(value)
        return shape
    
    # Dict - could be adjacency list or frequency map
    if isinstance(value, dict):
        shape.u = len(value)  # unique keys
        
        # Check if adjacency list pattern
        if value and all(isinstance(v, (list, tuple)) for v in value.values()):
            shape.V = len(value)
            shape.E = sum(len(adj) for adj in value.values())
        
        return shape
    
    # Set
    if isinstance(value, (set, frozenset)):
        shape.u = len(value)
        return shape
    
    # Linked List node (duck typing)
    if hasattr(value, 'next'):
        count = 0
        node = value
        while node:
            count += 1
            node = getattr(node, 'next', None)
        shape.nodes = count
        shape.n = count
        return shape
    
    # Tree node (duck typing)
    if hasattr(value, 'left') or hasattr(value, 'right') or hasattr(value, 'children'):
        nodes, height = _count_tree(value)
        shape.nodes = nodes
        shape.height = height
        shape.n = nodes
        return shape
    
    return shape


def _count_tree(root: Any) -> Tuple[int, int]:
    """Count nodes and height of a tree."""
    if root is None:
        return 0, 0
    
    # Binary tree
    if hasattr(root, 'left') and hasattr(root, 'right'):
        left_nodes, left_height = _count_tree(getattr(root, 'left', None))
        right_nodes, right_height = _count_tree(getattr(root, 'right', None))
        return 1 + left_nodes + right_nodes, 1 + max(left_height, right_height)
    
    # N-ary tree
    if hasattr(root, 'children'):
        children = getattr(root, 'children', []) or []
        if not children:
            return 1, 1
        child_results = [_count_tree(c) for c in children]
        total_nodes = 1 + sum(r[0] for r in child_results)
        max_height = 1 + max(r[1] for r in child_results)
        return total_nodes, max_height
    
    return 1, 1


# ============================================================================
# Shape Inference from Method Signature
# ============================================================================

def infer_shapes_from_signature(
    method: callable,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any] = None
) -> Dict[str, InputShape]:
    """
    Infer InputShape for each parameter from method signature + actual values.
    
    Like introspecting a PyTorch model's input shapes.
    
    Args:
        method: The method to analyze
        args: Positional arguments passed to method
        kwargs: Keyword arguments passed to method
        
    Returns:
        Dict mapping parameter name to its InputShape
        
    Example:
        >>> def solve(nums: List[int], k: int): pass
        >>> infer_shapes_from_signature(solve, ([1,2,3,4,5], 3))
        {'nums': Shape(n=5), 'k': Shape()}
    """
    kwargs = kwargs or {}
    sig = inspect.signature(method)
    params = list(sig.parameters.values())
    
    # Skip 'self' if present
    if params and params[0].name == 'self':
        params = params[1:]
    
    # Get type hints
    try:
        hints = get_type_hints(method)
    except Exception:
        hints = {}
    
    result = {}
    
    # Map args to parameters
    for i, param in enumerate(params):
        name = param.name
        
        # Get value
        if name in kwargs:
            value = kwargs[name]
        elif i < len(args):
            value = args[i]
        elif param.default is not inspect.Parameter.empty:
            value = param.default
        else:
            continue
        
        # Get type hint
        type_hint = hints.get(name)
        
        # Infer shape
        result[name] = infer_shape(value, type_hint)
    
    return result


def compute_aggregate_shape(shapes: Dict[str, InputShape]) -> InputShape:
    """
    Compute aggregate InputShape from multiple parameter shapes.
    
    Combines shapes into a single summary shape.
    
    Example:
        >>> shapes = {
        ...     'lists': Shape(k=3, n=8),
        ...     'target': Shape()
        ... }
        >>> compute_aggregate_shape(shapes)
        Shape(k=3, n=8)
    """
    result = InputShape()
    
    for name, shape in shapes.items():
        # Take first non-None for each dimension
        for dim in ['n', 'm', 'k', 'rows', 'cols', 'V', 'E', 'nodes', 'height', 'd', 'u']:
            if getattr(result, dim) is None:
                val = getattr(shape, dim)
                if val is not None:
                    setattr(result, dim, val)
    
    return result


# ============================================================================
# Convenience Functions
# ============================================================================

def shape_of(value: Any) -> InputShape:
    """
    Quick shape inference, like PyTorch's tensor.shape.
    
    Examples:
        >>> shape_of([1, 2, 3])
        Shape(n=3)
        
        >>> shape_of([[1,2], [3,4], [5,6]])
        Shape(rows=3, cols=2, n=6)
    """
    return infer_shape(value)


def format_shape(value: Any) -> str:
    """
    Get formatted shape string for display.
    
    Examples:
        >>> format_shape([1, 2, 3, 4, 5])
        'n=5'
        
        >>> format_shape([[1,2,3], [4,5,6]])
        'rows=2, cols=3, n=6'
    """
    return infer_shape(value).format()


__all__ = [
    'InputShape',
    'infer_shape',
    'infer_shapes_from_signature',
    'compute_aggregate_shape',
    'shape_of',
    'format_shape',
]

