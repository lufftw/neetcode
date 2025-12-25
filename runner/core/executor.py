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
from typing import Dict
from runner.utils.compare import compare_result
from runner.analysis.memory_profiler import HAS_PSUTIL
from runner.analysis.input_scale import compute_input_bytes, estimate_input_scale

PYTHON_EXE = sys.executable


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
    Try to estimate input scale from raw input string.
    
    Attempts to parse input as Python literals and derive scale metrics.
    Returns dict like {'n': 100, 'm': 50} or None if estimation fails.
    """
    if not input_data.strip():
        return None
    
    lines = input_data.strip().split('\n')
    parsed_args: Dict[str, Any] = {}
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        try:
            # Try to parse as Python literal
            obj = ast.literal_eval(line)
            parsed_args[f'arg{i}'] = obj
        except (ValueError, SyntaxError):
            # Try to parse as simple number
            try:
                if '.' in line:
                    parsed_args[f'arg{i}'] = float(line)
                else:
                    parsed_args[f'arg{i}'] = int(line)
            except ValueError:
                # Store as string (for length calculation)
                parsed_args[f'arg{i}'] = line
    
    if not parsed_args:
        return None
    
    # Use estimate_input_scale to derive metrics
    return estimate_input_scale(parsed_args)


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
    
    # Memory profiling setup
    rss_samples: List[int] = []
    stop_event: Optional[threading.Event] = None
    sampler_thread: Optional[threading.Thread] = None
    peak_rss_bytes: Optional[int] = None
    
    start_time = time.perf_counter()
    
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
        stdout, stderr = proc.communicate(input=input_data)
        
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

