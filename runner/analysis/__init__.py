# runner/analysis/__init__.py
"""
Analysis modules for complexity and memory profiling.

Provides:
- Complexity estimation (Big-O analysis)
- Memory profiling (RSS measurement)
- Input scale estimation
- Input shape inference (PyTorch-style)
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
from runner.analysis.input_shape import (
    InputShape,
    infer_shape,
    infer_shapes_from_signature,
    compute_aggregate_shape,
    shape_of,
    format_shape,
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
    # input_shape (PyTorch-style)
    'InputShape',
    'infer_shape',
    'infer_shapes_from_signature',
    'compute_aggregate_shape',
    'shape_of',
    'format_shape',
]

