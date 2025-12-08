# runner/module_loader.py
"""
Module Loader - Load solution and generator modules dynamically.
"""
import os
import importlib.util
from typing import Optional, Tuple, Any


def load_solution_module(problem: str) -> Tuple[Optional[Any], Optional[dict], str]:
    """
    Dynamically load solution module to get SOLUTIONS metadata and COMPARE_MODE.
    
    Returns:
        tuple: (module, solutions_meta, compare_mode)
            - module: Loaded module object
            - solutions_meta: SOLUTIONS dictionary (if exists)
            - compare_mode: Comparison mode ("exact" | "sorted" | "set")
    """
    solution_path = os.path.join("solutions", f"{problem}.py")
    if not os.path.exists(solution_path):
        return None, None, "exact"
    
    spec = importlib.util.spec_from_file_location(f"solution_{problem}", solution_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"⚠️ Error loading module: {e}")
        return None, None, "exact"
    
    # Get SOLUTIONS metadata (if exists)
    solutions_meta = getattr(module, 'SOLUTIONS', None)
    
    # Get COMPARE_MODE (default: "exact")
    compare_mode = getattr(module, 'COMPARE_MODE', 'exact')
    
    return module, solutions_meta, compare_mode


def load_generator_module(problem: str) -> Optional[Any]:
    """
    Load generator module for a problem.
    
    Returns:
        module or None if generator doesn't exist
    """
    generator_path = os.path.join("generators", f"{problem}.py")
    if not os.path.exists(generator_path):
        return None
    
    spec = importlib.util.spec_from_file_location(f"generator_{problem}", generator_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"⚠️ Error loading generator: {e}")
        return None
    
    # Check if generate function exists
    if not hasattr(module, 'generate'):
        print(f"⚠️ Generator missing 'generate' function: {generator_path}")
        return None
    
    return module

