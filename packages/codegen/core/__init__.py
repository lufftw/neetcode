"""
CodeGen core components.

Shared modules used by both reference and practice generators.
"""

from .solution_header import render_solution_header
from .stub_parser import parse_code_stub, StubInfo
from .assemble import assemble_module
from .config import CodeGenConfig, load_config

__all__ = [
    "render_solution_header",
    "parse_code_stub",
    "StubInfo",
    "assemble_module",
    "CodeGenConfig",
    "load_config",
]

