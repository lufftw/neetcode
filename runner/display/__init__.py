# runner/display/__init__.py
"""
Display modules for test runner output.

Provides formatting and display functions for:
- Core reporting (pass/fail, validation labels)
- Benchmark visualization (bar charts, tables)
- Memory profiling output (traces, comparisons)
"""
from runner.display.reporter import (
    supports_unicode,
    get_box_chars,
    truncate_input,
    format_validation_label,
    save_failed_case,
)
from runner.display.benchmark import (
    print_visual_benchmark,
    print_benchmark_summary,
)
from runner.display.memory import (
    print_memory_trace,
    print_memory_per_case,
    print_trace_compare,
)

__all__ = [
    # reporter
    'supports_unicode',
    'get_box_chars',
    'truncate_input',
    'format_validation_label',
    'save_failed_case',
    # benchmark
    'print_visual_benchmark',
    'print_benchmark_summary',
    # memory
    'print_memory_trace',
    'print_memory_per_case',
    'print_trace_compare',
]

