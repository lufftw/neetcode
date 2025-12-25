# runner/analysis/input_scale.py
"""
Input Scale Estimation - Derive problem scale from method signatures.

Per Input_Scale_Metrics.md:
- Input Scale (n, m, V, E): Structural size of the problem
- Signature Payload (MB): Memory footprint of input objects
- Input Bytes (MB): Raw size of stdin data

No conversion is performed between these values.
"""
import sys
from typing import Optional, Dict, Any


def estimate_input_scale(signature_args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Estimate input scale from method signature arguments.
    
    Standard mappings (from Input_Scale_Metrics.md):
    - List[int], str -> n = len(...)
    - Two lists -> n = len(a), m = len(b)
    - Matrix -> rows, cols, n = rows * cols
    - Linked list -> nodes
    - Tree -> nodes
    - Graph edges -> E, V
    
    Returns:
        Dict with scale metrics (e.g., {'n': 1000, 'm': 500})
        or None if signature unavailable
    """
    if not signature_args:
        return None
    
    scale: Dict[str, Any] = {}
    
    for name, value in signature_args.items():
        if value is None:
            continue
        
        # String
        if isinstance(value, str):
            if 'n' not in scale:
                scale['n'] = len(value)
            continue
        
        # List or Tuple (check for matrix first)
        if isinstance(value, (list, tuple)):
            if value and isinstance(value[0], (list, tuple)):
                # Matrix / Grid
                rows = len(value)
                cols = len(value[0]) if value else 0
                scale['rows'] = rows
                scale['cols'] = cols
                scale['n'] = rows * cols
            else:
                # 1D array/tuple
                if 'n' not in scale:
                    scale['n'] = len(value)
                elif 'm' not in scale:
                    scale['m'] = len(value)
            continue
        
        # Dict (frequency map or adjacency list)
        if isinstance(value, dict):
            scale['u'] = len(value)  # unique keys
            # Check if it's an adjacency list
            if value and all(isinstance(v, (list, tuple)) for v in value.values()):
                scale['V'] = len(value)
                scale['E'] = sum(len(adj) for adj in value.values())
            continue
    
    return scale if scale else None


def compute_input_bytes(input_data: str) -> int:
    """Compute raw size of input data in bytes."""
    return len(input_data.encode('utf-8'))


def compute_signature_payload(obj: Any) -> Optional[int]:
    """
    Estimate deep memory footprint of an object.
    
    Note: This is a best-effort estimation.
    Returns None if measurement fails.
    """
    try:
        return _deep_sizeof(obj, seen=set())
    except Exception:
        return None


def _deep_sizeof(obj: Any, seen: set) -> int:
    """Recursively compute deep size of an object."""
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    
    size = sys.getsizeof(obj)
    
    if isinstance(obj, dict):
        size += sum(_deep_sizeof(k, seen) + _deep_sizeof(v, seen) 
                   for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(_deep_sizeof(item, seen) for item in obj)
    elif hasattr(obj, '__dict__'):
        size += _deep_sizeof(obj.__dict__, seen)
    
    return size


def format_input_scale(scale: Optional[Dict[str, Any]]) -> str:
    """
    Format input scale as shape string.
    
    Format:
        [a]       = 1D length
        [a,b]     = 2D shape (rows×cols)
        [a,b,c]   = 3D shape
        n=X       = total elements (always shown)
    
    Examples:
        {'s': {'shape': [8]}}
        → "s:[8] n=8"
        
        {'matrix': {'shape': [3, 4]}}
        → "matrix:[3,4] n=12"
        
        {'lists': {'shape': [3], 'total': 8}}
        → "lists:[3] n=8"
    """
    if not scale:
        return "N/A"
    
    parts = []
    
    for key, value in scale.items():
        # New auto_shape format: {'shape': [...], 'total': N, ...}
        if isinstance(value, dict):
            shape = value.get('shape')
            total = value.get('total')
            
            if shape is not None:
                if len(shape) == 0:
                    # Scalar - skip (doesn't contribute to "scale")
                    continue
                
                # Format as [d1,d2,...]
                shape_str = f"[{','.join(str(d) for d in shape)}]"
                
                # Calculate n (total elements)
                if total is not None:
                    n = total
                else:
                    # For uniform shapes, n = product of dimensions
                    n = 1
                    for d in shape:
                        n *= d
                
                parts.append(f"{key}:{shape_str} n={n}")
            else:
                parts.append(f"{key}:{value}")
        
        # Legacy format: direct values
        elif isinstance(value, (list, tuple)) and len(value) == 2:
            dims, total = value
            if isinstance(dims, list):
                shape_str = f"[{','.join(str(d) for d in dims)}]"
                parts.append(f"{key}:{shape_str} n={total}")
        elif isinstance(value, list):
            shape_str = f"[{','.join(str(d) for d in value)}]"
            n = 1
            for d in value:
                n *= d
            parts.append(f"{key}:{shape_str} n={n}")
        elif isinstance(value, int):
            parts.append(f"{key}={value}")
        else:
            parts.append(f"{key}={value}")
    
    return ' '.join(parts) if parts else "N/A"


def get_input_scale_legend() -> str:
    """
    Return legend text explaining the Input Scale format.
    
    Returns:
        Multi-line string with format explanation.
    """
    return """Input Scale Legend:
  [a]     = 1D length
  [a,b]   = 2D shape (rows×cols)
  [a,b,c] = 3D shape
  n       = total elements"""


__all__ = [
    'estimate_input_scale',
    'compute_input_bytes',
    'compute_signature_payload',
    'format_input_scale',
    'get_input_scale_legend',
]

