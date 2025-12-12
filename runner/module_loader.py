# runner/module_loader.py
"""
Module Loader - Load solution and generator modules dynamically.

Validates SOLUTIONS dictionary format per ARCHITECTURE_MIGRATION.md:
- SOLUTIONS dictionary is required
- Each entry must have 'class' and 'method' fields
- 'default' key is required
"""
import os
import importlib.util
from typing import Optional, Tuple, Any


def validate_solutions_meta(solutions_meta: Optional[dict], problem: str) -> bool:
    """
    Validate SOLUTIONS format per polymorphic architecture.
    
    Required format:
        SOLUTIONS = {
            "default": {"class": "SolutionName", "method": "methodName", ...},
            ...
        }
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not solutions_meta:
        print(f"⚠️ [{problem}] SOLUTIONS dictionary not found (legacy mode)")
        return True  # Allow legacy mode for backward compatibility
    
    if 'default' not in solutions_meta:
        print(f"❌ [{problem}] SOLUTIONS must have 'default' key")
        return False
    
    errors = []
    for key, info in solutions_meta.items():
        if 'class' not in info:
            errors.append(f"SOLUTIONS['{key}'] missing 'class' field")
        if 'method' not in info:
            errors.append(f"SOLUTIONS['{key}'] missing 'method' field")
    
    if errors:
        print(f"❌ [{problem}] Invalid SOLUTIONS format:")
        for error in errors:
            print(f"   - {error}")
        print(f"\n   Expected format:")
        print(f"   SOLUTIONS = {{")
        print(f'       "default": {{"class": "Solution", "method": "twoSum", ...}},')
        print(f"   }}")
        return False
    
    return True


def load_solution_module(problem: str) -> Tuple[Optional[Any], Optional[dict], str]:
    """
    Dynamically load solution module to get SOLUTIONS metadata and COMPARE_MODE.
    
    Validates SOLUTIONS format per polymorphic architecture.
    
    Returns:
        tuple: (module, solutions_meta, compare_mode)
            - module: Loaded module object
            - solutions_meta: SOLUTIONS dictionary (if exists and valid)
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
    
    # Validate SOLUTIONS format
    if solutions_meta and not validate_solutions_meta(solutions_meta, problem):
        # Return None for invalid SOLUTIONS to trigger error handling
        return module, None, "exact"
    
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

