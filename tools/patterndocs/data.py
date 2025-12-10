# tools/patterndocs/data.py
"""Data classes for pattern documentation."""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class APIKernel:
    """Represents an API Kernel from ontology."""
    id: str
    summary: str


@dataclass
class Pattern:
    """Represents a Pattern from ontology."""
    id: str
    api_kernel: str
    summary: str


@dataclass
class PatternDocConfig:
    """Configuration for generating a pattern document."""
    kernel_id: str
    kernel_summary: str
    source_dir: Path
    output_file: Path
    patterns: list[Pattern] = field(default_factory=list)

