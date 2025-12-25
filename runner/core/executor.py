# runner/core/executor.py
"""
Test Case Executor - Run individual test cases with optional memory profiling.
"""
import subprocess
import os
import sys
import time
import threading
from typing import Optional, Any, Tuple, List

import ast
import re
import json
from typing import Dict
from runner.utils.compare import compare_result
from runner.analysis.memory_profiler import HAS_PSUTIL
from runner.analysis.input_scale import compute_input_bytes
from runner.analysis.input_shape import shape_of, InputShape

PYTHON_EXE = sys.executable

# Shape protocol for subprocess communication
_SHAPE_START = "__SHAPE__:"
_SHAPE_END = "__END_SHAPE__"
_SHAPE_PATTERN = re.compile(rf'{re.escape(_SHAPE_START)}(.+?){re.escape(_SHAPE_END)}')


def _sample_subprocess_rss(pid: int, interval: float, 
                           samples: List[int], stop_event: threading.Event) -> None:
    """
    Sample subprocess RSS at regular intervals.
    
    Runs in a separate thread to collect memory samples during execution.
    """
    if not HAS_PSUTIL:
        return
    
    import psutil
    
    try:
        proc = psutil.Process(pid)
        while not stop_event.is_set():
            try:
                rss = proc.memory_info().rss
                samples.append(rss)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                break
            stop_event.wait(interval)
    except Exception:
        pass


def _estimate_input_scale_from_string(input_data: str) -> Optional[Dict[str, Any]]:
    """
    Estimate input scale from raw input string using PyTorch-style shape inference.
    
    Parses input into Python objects, then uses shape_of() to compute
    semantic dimensions (n, m, k, rows, cols, V, E, etc.)
    
    Returns dict like {'n': 100, 'k': 3} or None if estimation fails.
    """
    if not input_data.strip():
        return None
    
    lines = input_data.strip().split('\n')
    parsed_objects: List[Any] = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        obj = _parse_input_line(line)
        if obj is not None:
            parsed_objects.append(obj)
    
    if not parsed_objects:
        return None
    
    # Use shape_of() for PyTorch-style shape inference
    return _compute_aggregate_shape(parsed_objects)


def _compute_aggregate_shape(objects: List[Any]) -> Optional[Dict[str, Any]]:
    """
    Compute aggregate shape from multiple parsed input objects.
    
    Smart aggregation:
    - If multiple lists of similar type → treat as k-lists
    - If single list of lists → use its shape directly
    - Otherwise combine individual shapes
    """
    if not objects:
        return None
    
    # Check if first object is an integer count followed by that many lists
    # Pattern: k\n list1\n list2\n ... (common for k-way merge problems)
    if (len(objects) >= 2 and 
        isinstance(objects[0], int) and 
        all(isinstance(o, (list, tuple)) for o in objects[1:])):
        
        k = objects[0]
        lists = objects[1:]
        
        # Verify k matches number of lists (or close)
        if abs(k - len(lists)) <= 1:  # Allow off-by-one
            total_elements = sum(len(lst) for lst in lists)
            return {'k': len(lists), 'n': total_elements}
    
    # Single object - use its shape directly
    if len(objects) == 1:
        shape = shape_of(objects[0])
        result = shape.to_dict()
        return result if result else None
    
    # Multiple objects - try to find the most meaningful shape
    # Priority: list of lists > single list > scalar
    best_shape = None
    best_priority = -1
    
    for obj in objects:
        shape = shape_of(obj)
        priority = _shape_priority(shape)
        
        if priority > best_priority:
            best_priority = priority
            best_shape = shape
    
    if best_shape:
        result = best_shape.to_dict()
        return result if result else None
    
    return None


def _shape_priority(shape: InputShape) -> int:
    """Determine priority of a shape (higher = more informative)."""
    if shape.k is not None or shape.V is not None:
        return 4  # k-lists or graph
    if shape.rows is not None:
        return 3  # matrix
    if shape.n is not None and shape.n > 0:
        return 2  # array/string
    if shape.u is not None:
        return 1  # dict
    return 0


def _parse_input_line(line: str) -> Optional[Any]:
    """
    Parse a single line of input into a Python object.
    
    Handles:
    - Python literals: [1,2,3], {"a": 1}, (1, 2)
    - Comma-separated values: 1,4,5 -> [1, 4, 5]
    - Space-separated values: 1 4 5 -> [1, 4, 5]
    - Single numbers: 42, 3.14
    - Strings (fallback)
    """
    line = line.strip()
    if not line:
        return None
    
    # 1. Try Python literal first
    try:
        return ast.literal_eval(line)
    except (ValueError, SyntaxError):
        pass
    
    # 2. Try comma-separated values (e.g., "1,4,5")
    if ',' in line:
        parts = [p.strip() for p in line.split(',')]
        if len(parts) > 1:
            parsed_list = _try_parse_list(parts)
            if parsed_list is not None:
                return parsed_list
    
    # 3. Try space-separated values (e.g., "1 4 5")
    if ' ' in line:
        parts = line.split()
        if len(parts) > 1:
            parsed_list = _try_parse_list(parts)
            if parsed_list is not None:
                return parsed_list
    
    # 4. Try single number
    try:
        if '.' in line:
            return float(line)
        return int(line)
    except ValueError:
        pass
    
    # 5. Return as string (for length calculation)
    return line


def _try_parse_list(parts: List[str]) -> Optional[List[Any]]:
    """Try to parse list of string parts into typed list."""
    result = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        try:
            # Try int first
            result.append(int(p))
        except ValueError:
            try:
                # Try float
                result.append(float(p))
            except ValueError:
                # Keep as string
                result.append(p)
    return result if result else None


def _parse_shape_from_stderr(stderr: str) -> Optional[Dict[str, Any]]:
    """
    Parse shape information reported by subprocess via stderr.
    
    Solutions can call report_shape() to emit shape info.
    This is the authoritative source since subprocess has actual parsed objects.
    
    Returns:
        Shape dict if found, None otherwise
    """
    if not stderr:
        return None
    
    match = _SHAPE_PATTERN.search(stderr)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
    return None


def run_one_case(problem: str, input_path: str, output_path: str, 
                 method: Optional[str] = None, benchmark: bool = False,
                 compare_mode: str = "exact", module: Any = None,
                 profile_memory: bool = False) -> Tuple[Optional[bool], float, str, Optional[str], str, Optional[int], int, Optional[Dict[str, Any]]]:
    """
    Run a single test case with optional memory profiling.
    
    Args:
        problem: Problem name
        input_path: Input file path
        output_path: Expected output file path
        method: Solution method name (optional)
        benchmark: Whether to measure time
        compare_mode: Comparison mode ("exact" | "sorted" | "set")
        module: Loaded solution module (for JUDGE_FUNC)
        profile_memory: Whether to capture RSS measurements
    
    Returns: 
        tuple: (passed, elapsed_ms, actual, expected, validation_mode, peak_rss_bytes, input_bytes, input_scale)
            - passed: bool or None (None = skipped)
            - elapsed_ms: float
            - actual: str
            - expected: str or None
            - validation_mode: "judge" | "judge-only" | "exact" | "sorted" | "set" | "skip"
            - peak_rss_bytes: int or None (peak RSS of subprocess)
            - input_bytes: int (raw input size)
            - input_scale: dict or None (e.g., {'n': 100, 'm': 50})
    """
    # Check if .out file exists
    has_out_file = os.path.exists(output_path)
    judge_func = getattr(module, 'JUDGE_FUNC', None) if module else None
    
    # Read input
    with open(input_path, "r", encoding="utf-8") as f:
        input_data = f.read()
    
    input_bytes = compute_input_bytes(input_data)
    
    # Try to estimate input scale from input data
    input_scale_str = _estimate_input_scale_from_string(input_data)
    
    # Read expected output (if exists)
    if has_out_file:
        with open(output_path, "r", encoding="utf-8") as f:
            expected = f.read()
    else:
        expected = None
    
    # Handle missing .out file
    if not has_out_file and not judge_func:
        # No .out and no JUDGE_FUNC -> skip
        return None, 0.0, "", None, "skip", None, input_bytes, input_scale_str
    
    solution_path = os.path.join("solutions", f"{problem}.py")
    if not os.path.exists(solution_path):
        print(f"❌ Solution file not found: {solution_path}")
        return False, 0.0, "", expected, "error", None, input_bytes, input_scale_str
    
    # Prepare environment variables to pass method parameter
    env = os.environ.copy()
    if method:
        env['SOLUTION_METHOD'] = method
    
    # Enable shape reporting from solution subprocess
    env['NEETCODE_SHAPE_REPORT'] = '1'
    
    # Memory profiling setup
    rss_samples: List[int] = []
    stop_event: Optional[threading.Event] = None
    sampler_thread: Optional[threading.Thread] = None
    peak_rss_bytes: Optional[int] = None
    
    start_time = time.perf_counter()
    
    stderr_output = ""
    
    # Use Popen for memory profiling to get PID
    if profile_memory and HAS_PSUTIL:
        proc = subprocess.Popen(
            [PYTHON_EXE, solution_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        
        # Start RSS sampling thread
        stop_event = threading.Event()
        sampler_thread = threading.Thread(
            target=_sample_subprocess_rss,
            args=(proc.pid, 0.01, rss_samples, stop_event)  # 10ms interval
        )
        sampler_thread.start()
        
        # Communicate with process
        stdout, stderr_output = proc.communicate(input=input_data)
        
        # Stop sampling
        stop_event.set()
        sampler_thread.join(timeout=0.1)
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        actual = stdout
        
        # Calculate peak RSS from samples
        if rss_samples:
            peak_rss_bytes = max(rss_samples)
    else:
        # Standard execution without memory profiling
        result = subprocess.run(
            [PYTHON_EXE, solution_path],
            input=input_data,
            text=True,
            capture_output=True,
            env=env
        )
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        actual = result.stdout
        stderr_output = result.stderr
    
    # Parse shape from subprocess stderr (if reported by solution)
    # This is the authoritative source - solution has actual parsed objects
    reported_shape = _parse_shape_from_stderr(stderr_output)
    if reported_shape:
        input_scale_str = reported_shape  # Prefer subprocess-reported shape
    
    # Determine validation mode and run comparison
    if judge_func:
        # JUDGE_FUNC mode
        ok = compare_result(actual, expected, input_data, module, compare_mode)
        validation_mode = "judge" if has_out_file else "judge-only"
    else:
        # COMPARE_MODE (requires .out file)
        ok = compare_result(actual, expected, input_data, module, compare_mode)
        validation_mode = compare_mode  # "exact" / "sorted" / "set"
    
    return ok, elapsed_ms, actual, expected, validation_mode, peak_rss_bytes, input_bytes, input_scale_str


def run_generated_case(problem: str, input_data: str, case_name: str,
                       method: Optional[str], benchmark: bool,
                       compare_mode: str, module: Any,
                       profile_memory: bool = False) -> Tuple[Optional[bool], float, str, str, Optional[int], int, Optional[Dict[str, Any]]]:
    """
    Run a single generated test case with optional memory profiling.
    
    Returns:
        tuple: (passed, elapsed_ms, actual, input_data, peak_rss_bytes, input_bytes, input_scale)
    """
    judge_func = getattr(module, 'JUDGE_FUNC', None) if module else None
    input_bytes = compute_input_bytes(input_data)
    input_scale_str = _estimate_input_scale_from_string(input_data)
    
    if not judge_func:
        # Generated cases require JUDGE_FUNC
        return None, 0.0, "", input_data, None, input_bytes, input_scale_str
    
    solution_path = os.path.join("solutions", f"{problem}.py")
    if not os.path.exists(solution_path):
        return False, 0.0, "", input_data, None, input_bytes, input_scale_str
    
    # Prepare environment variables
    env = os.environ.copy()
    if method:
        env['SOLUTION_METHOD'] = method
    
    # Enable shape reporting from solution subprocess
    env['NEETCODE_SHAPE_REPORT'] = '1'
    
    # Memory profiling setup
    rss_samples: List[int] = []
    peak_rss_bytes: Optional[int] = None
    
    start_time = time.perf_counter()
    
    if profile_memory and HAS_PSUTIL:
        proc = subprocess.Popen(
            [PYTHON_EXE, solution_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        
        # Start RSS sampling thread
        stop_event = threading.Event()
        sampler_thread = threading.Thread(
            target=_sample_subprocess_rss,
            args=(proc.pid, 0.01, rss_samples, stop_event)
        )
        sampler_thread.start()
        
        # Communicate with process
        stdout, stderr = proc.communicate(input=input_data)
        
        # Stop sampling
        stop_event.set()
        sampler_thread.join(timeout=0.1)
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        actual = stdout
        
        if rss_samples:
            peak_rss_bytes = max(rss_samples)
    else:
        result = subprocess.run(
            [PYTHON_EXE, solution_path],
            input=input_data,
            text=True,
            capture_output=True,
            env=env
        )
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        actual = result.stdout
    
    # Validate using JUDGE_FUNC (expected is None for generated cases)
    ok = compare_result(actual, None, input_data, module, compare_mode)
    
    return ok, elapsed_ms, actual, input_data, peak_rss_bytes, input_bytes, input_scale_str


__all__ = [
    'PYTHON_EXE',
    'run_one_case',
    'run_generated_case',
]

