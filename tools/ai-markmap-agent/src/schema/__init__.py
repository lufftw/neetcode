# =============================================================================
# Schema Module - V3 Structure Specification
# =============================================================================
# This module defines the Structure Specification schema and validation
# for the V3 multi-agent Markmap generation system.
# =============================================================================

from .structure_spec import (
    StructureSpec,
    Metadata,
    Organization,
    Section,
    ProblemRef,
    Subcategory,
    LearningPath,
    ProgressSummary,
    FormatHints,
    validate_structure_spec,
    validate_final_output,
    parse_structure_spec,
    dump_structure_spec,
    extract_yaml_from_response,
)

__all__ = [
    "StructureSpec",
    "Metadata",
    "Organization",
    "Section",
    "ProblemRef",
    "Subcategory",
    "LearningPath",
    "ProgressSummary",
    "FormatHints",
    "validate_structure_spec",
    "validate_final_output",
    "parse_structure_spec",
    "dump_structure_spec",
    "extract_yaml_from_response",
]

