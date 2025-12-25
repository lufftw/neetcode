# runner/__init__.py
"""
NeetCode Practice Test Runner Package.

This is the main entry point for the runner package. It provides backward-compatible
imports from the new subpackage structure.

Subpackages:
    runner.utils       - Utility modules (loader, compare, parser, paths)
    runner.display     - Display modules (reporter, benchmark, memory)
    runner.analysis    - Analysis modules (complexity, memory_profiler, input_scale)
    runner.core        - Core execution modules (executor, method_runner)

Example Usage:
    from runner import load_solution_module, run_one_case
    from runner.display import print_benchmark_summary
    from runner.analysis import ComplexityEstimator
"""

# Re-export from utils
from runner.utils.loader import (
    load_solution_module,
    load_generator_module,
)
from runner.utils.compare import (
    compare_result,
    normalize_output,
)
from runner.utils.parser import (
    parse_class_headers,
    get_approach_info,
    build_method_mapping,
)
from runner.utils.paths import (
    PROJECT_ROOT,
    SOLUTIONS_DIR,
    TESTS_DIR,
    get_solution_path,
)

# Re-export from display
from runner.display.reporter import (
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

# Re-export from analysis
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

# Re-export from core
from runner.core.executor import (
    PYTHON_EXE,
    run_one_case,
    run_generated_case,
)
from runner.core.method_runner import (
    run_method_tests,
    run_legacy_tests,
)

__all__ = [
    # utils.loader
    'load_solution_module',
    'load_generator_module',
    # utils.compare
    'compare_result',
    'normalize_output',
    # utils.parser
    'parse_class_headers',
    'get_approach_info',
    'build_method_mapping',
    # utils.paths
    'PROJECT_ROOT',
    'SOLUTIONS_DIR',
    'TESTS_DIR',
    'get_solution_path',
    # display.reporter
    'truncate_input',
    'format_validation_label',
    'save_failed_case',
    # display.benchmark
    'print_visual_benchmark',
    'print_benchmark_summary',
    # display.memory
    'print_memory_trace',
    'print_memory_per_case',
    'print_trace_compare',
    # analysis.complexity
    'HAS_BIG_O',
    'ComplexityEstimator',
    'ComplexityResult',
    'format_complexity_result',
    # analysis.memory_profiler
    'HAS_PSUTIL',
    'MemoryProfiler',
    'CaseMemoryMetrics',
    'MethodMemoryMetrics',
    'format_bytes',
    'generate_memory_trace',
    # analysis.input_scale
    'estimate_input_scale',
    'compute_input_bytes',
    'compute_signature_payload',
    'format_input_scale',
    # core.executor
    'PYTHON_EXE',
    'run_one_case',
    'run_generated_case',
    # core.method_runner
    'run_method_tests',
    'run_legacy_tests',
]

