# runner/analysis/__init__.py
"""
Analysis modules for complexity and memory profiling.

Provides:
- Complexity estimation (Big-O analysis)
- Memory profiling (RSS measurement)
- Input scale estimation
"""
from runner.analysis.complexity import (
    HAS_BIG_O,
    ComplexityEstimator,
    ComplexityResult,
    format_complexity_result,
)
from runner.analysis.memory_profiler import (
    HAS_PSUTIL,
    MemoryProfiler,
    CaseMemoryMetrics,
    MethodMemoryMetrics,
    format_bytes,
    generate_memory_trace,
)
from runner.analysis.input_scale import (
    estimate_input_scale,
    compute_input_bytes,
    compute_signature_payload,
    format_input_scale,
)

__all__ = [
    # complexity
    'HAS_BIG_O',
    'ComplexityEstimator',
    'ComplexityResult',
    'format_complexity_result',
    # memory_profiler
    'HAS_PSUTIL',
    'MemoryProfiler',
    'CaseMemoryMetrics',
    'MethodMemoryMetrics',
    'format_bytes',
    'generate_memory_trace',
    # input_scale
    'estimate_input_scale',
    'compute_input_bytes',
    'compute_signature_payload',
    'format_input_scale',
]

