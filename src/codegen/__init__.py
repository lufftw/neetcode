"""
CodeGen - LeetCode solution skeleton generator.

This package provides:
    - Reference skeleton generation (solutions/)
    - Practice skeleton generation (practices/)
    - Reusable components: solution_header, helpers, stub_parser

Usage:
    from codegen import (
        generate_reference_skeleton,
        generate_practice_skeleton,
        render_solution_header,
    )
    
    # Generate reference skeleton
    generate_reference_skeleton(1)  # Two Sum
    
    # Generate practice skeleton  
    generate_practice_skeleton(1)
    
    # Render header only
    header = render_solution_header(problem_meta)
"""

from .core.solution_header import render_solution_header
from .core.stub_parser import parse_code_stub, StubInfo
from .core.assemble import assemble_module
from .core.config import CodeGenConfig, load_config
from .core.helpers import detect_required_helpers, emit_helpers, HELPER_CATALOG
from .reference.generator import generate_reference_skeleton
from .practice.generator import generate_practice_skeleton

__all__ = [
    # Main generators
    "generate_reference_skeleton",
    "generate_practice_skeleton",
    # Components
    "render_solution_header",
    "parse_code_stub",
    "StubInfo",
    "assemble_module",
    # Config
    "CodeGenConfig",
    "load_config",
    # Helpers
    "detect_required_helpers",
    "emit_helpers",
    "HELPER_CATALOG",
]

