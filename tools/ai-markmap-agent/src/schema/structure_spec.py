# =============================================================================
# Structure Specification Schema V1
# =============================================================================
# This is the core data structure for V3 - what agents discuss,
# NOT the final Markdown output.
# =============================================================================

from __future__ import annotations

import re
import yaml
from dataclasses import dataclass, field
from typing import Any, Literal
from enum import Enum


class Importance(str, Enum):
    """Section importance level."""
    CORE = "core"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    OPTIONAL = "optional"


class ProblemRole(str, Enum):
    """Problem role in learning progression."""
    FOUNDATION = "foundation"
    PRACTICE = "practice"
    CHALLENGE = "challenge"


class HighlightLevel(str, Enum):
    """Visual emphasis level."""
    NORMAL = "normal"
    EMPHASIZED = "emphasized"
    DE_EMPHASIZED = "de-emphasized"


class GroupingType(str, Enum):
    """Content grouping strategy."""
    PATTERN = "pattern"
    DIFFICULTY = "difficulty"
    TOPIC = "topic"
    PROGRESS = "progress"
    CUSTOM = "custom"


@dataclass
class ProblemRef:
    """
    Reference to a problem by ID only.
    Full metadata is looked up by Writer.
    """
    id: str
    role: ProblemRole = ProblemRole.PRACTICE
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role.value,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any] | str) -> "ProblemRef":
        if isinstance(data, str):
            return cls(id=data)
        return cls(
            id=data.get("id", ""),
            role=ProblemRole(data.get("role", "practice")),
        )


@dataclass
class Subcategory:
    """Sub-category within a section."""
    name: str
    problems: list[str] = field(default_factory=list)
    description: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        d = {
            "name": self.name,
            "problems": self.problems,
        }
        if self.description:
            d["description"] = self.description
        return d
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Subcategory":
        return cls(
            name=data.get("name", ""),
            problems=data.get("problems", []),
            description=data.get("description", ""),
        )


@dataclass
class FormatHints:
    """
    Optional format hints for the Writer.
    Only used when specific formatting is needed.
    """
    should_fold: bool = False
    use_table: bool = False
    highlight_level: HighlightLevel = HighlightLevel.NORMAL
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "should_fold": self.should_fold,
            "use_table": self.use_table,
            "highlight_level": self.highlight_level.value,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FormatHints":
        return cls(
            should_fold=data.get("should_fold", False),
            use_table=data.get("use_table", False),
            highlight_level=HighlightLevel(data.get("highlight_level", "normal")),
        )


@dataclass
class SectionContent:
    """Content within a section."""
    problems: list[ProblemRef] = field(default_factory=list)
    learning_order: list[str] = field(default_factory=list)
    subcategories: list[Subcategory] = field(default_factory=list)
    
    def to_dict(self) -> dict[str, Any]:
        d = {
            "problems": [p.to_dict() for p in self.problems],
        }
        if self.learning_order:
            d["learning_order"] = self.learning_order
        if self.subcategories:
            d["subcategories"] = [s.to_dict() for s in self.subcategories]
        return d
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SectionContent":
        return cls(
            problems=[ProblemRef.from_dict(p) for p in data.get("problems", [])],
            learning_order=data.get("learning_order", []),
            subcategories=[
                Subcategory.from_dict(s) for s in data.get("subcategories", [])
            ],
        )


@dataclass
class Section:
    """A section in the Markmap structure."""
    id: str
    name: str
    importance: Importance = Importance.CORE
    content: SectionContent = field(default_factory=SectionContent)
    format_hints: FormatHints = field(default_factory=FormatHints)
    _decisions: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict[str, Any]:
        d = {
            "id": self.id,
            "name": self.name,
            "importance": self.importance.value,
            "content": self.content.to_dict(),
        }
        if self.format_hints:
            d["format_hints"] = self.format_hints.to_dict()
        if self._decisions:
            d["_decisions"] = self._decisions
        return d
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Section":
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            importance=Importance(data.get("importance", "core")),
            content=SectionContent.from_dict(data.get("content", {})),
            format_hints=FormatHints.from_dict(data.get("format_hints", {})),
            _decisions=data.get("_decisions", []),
        )


@dataclass
class LearningPathStep:
    """A step in a learning path."""
    section: str
    problems: list[str] = field(default_factory=list)
    milestone: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        d = {
            "section": self.section,
            "problems": self.problems,
        }
        if self.milestone:
            d["milestone"] = self.milestone
        return d
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LearningPathStep":
        return cls(
            section=data.get("section", ""),
            problems=data.get("problems", []),
            milestone=data.get("milestone", ""),
        )


@dataclass
class LearningPath:
    """A learning path through the content."""
    id: str
    name: str
    description: str = ""
    estimated_time: str = ""
    prerequisite: str = ""
    steps: list[LearningPathStep] = field(default_factory=list)
    
    def to_dict(self) -> dict[str, Any]:
        d = {
            "id": self.id,
            "name": self.name,
        }
        if self.description:
            d["description"] = self.description
        if self.estimated_time:
            d["estimated_time"] = self.estimated_time
        if self.prerequisite:
            d["prerequisite"] = self.prerequisite
        d["steps"] = [s.to_dict() for s in self.steps]
        return d
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LearningPath":
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            estimated_time=data.get("estimated_time", ""),
            prerequisite=data.get("prerequisite", ""),
            steps=[LearningPathStep.from_dict(s) for s in data.get("steps", [])],
        )


@dataclass
class DisplayOptions:
    """Display options for the Markmap."""
    show_complexity: bool = True
    show_difficulty: bool = True
    show_progress: bool = True
    show_topics: bool = False
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "show_complexity": self.show_complexity,
            "show_difficulty": self.show_difficulty,
            "show_progress": self.show_progress,
            "show_topics": self.show_topics,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DisplayOptions":
        return cls(
            show_complexity=data.get("show_complexity", True),
            show_difficulty=data.get("show_difficulty", True),
            show_progress=data.get("show_progress", True),
            show_topics=data.get("show_topics", False),
        )


@dataclass
class IncludeSections:
    """Which optional sections to include."""
    learning_paths: bool = True
    progress_summary: bool = True
    quick_reference: bool = False
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "learning_paths": self.learning_paths,
            "progress_summary": self.progress_summary,
            "quick_reference": self.quick_reference,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "IncludeSections":
        return cls(
            learning_paths=data.get("learning_paths", True),
            progress_summary=data.get("progress_summary", True),
            quick_reference=data.get("quick_reference", False),
        )


@dataclass
class Organization:
    """Organization strategy for the Markmap."""
    primary_grouping: GroupingType = GroupingType.PATTERN
    secondary_grouping: GroupingType | None = None
    display_options: DisplayOptions = field(default_factory=DisplayOptions)
    include_sections: IncludeSections = field(default_factory=IncludeSections)
    
    def to_dict(self) -> dict[str, Any]:
        d = {
            "primary_grouping": self.primary_grouping.value,
            "display_options": self.display_options.to_dict(),
            "include_sections": self.include_sections.to_dict(),
        }
        if self.secondary_grouping:
            d["secondary_grouping"] = self.secondary_grouping.value
        return d
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Organization":
        secondary = data.get("secondary_grouping")
        return cls(
            primary_grouping=GroupingType(data.get("primary_grouping", "pattern")),
            secondary_grouping=GroupingType(secondary) if secondary else None,
            display_options=DisplayOptions.from_dict(data.get("display_options", {})),
            include_sections=IncludeSections.from_dict(data.get("include_sections", {})),
        )


@dataclass
class ProgressSummary:
    """Progress summary configuration."""
    enabled: bool = True
    group_by: str = "section"
    show_percentage: bool = True
    show_count: bool = True
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "group_by": self.group_by,
            "show_percentage": self.show_percentage,
            "show_count": self.show_count,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProgressSummary":
        return cls(
            enabled=data.get("enabled", True),
            group_by=data.get("group_by", "section"),
            show_percentage=data.get("show_percentage", True),
            show_count=data.get("show_count", True),
        )


@dataclass
class Metadata:
    """Metadata about the Structure Specification."""
    title: str = "NeetCode Algorithm Patterns"
    description: str = ""
    version: str = "1.0"
    generated_by: str = "generalist"
    language: str = "en"
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "version": self.version,
            "generated_by": self.generated_by,
            "language": self.language,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Metadata":
        return cls(
            title=data.get("title", "NeetCode Algorithm Patterns"),
            description=data.get("description", ""),
            version=data.get("version", "1.0"),
            generated_by=data.get("generated_by", "generalist"),
            language=data.get("language", "en"),
        )


@dataclass
class DecisionLogEntry:
    """A decision log entry for internal tracking."""
    round: int
    decision: str
    rationale: str
    source: str
    agreed_by: list[str] = field(default_factory=list)
    timestamp: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        d = {
            "round": self.round,
            "decision": self.decision,
            "rationale": self.rationale,
            "source": self.source,
        }
        if self.agreed_by:
            d["agreed_by"] = self.agreed_by
        if self.timestamp:
            d["timestamp"] = self.timestamp
        return d
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DecisionLogEntry":
        return cls(
            round=data.get("round", 1),
            decision=data.get("decision", ""),
            rationale=data.get("rationale", ""),
            source=data.get("source", ""),
            agreed_by=data.get("agreed_by", []),
            timestamp=data.get("timestamp", ""),
        )


@dataclass
class Internal:
    """Internal metadata (not shown in final output)."""
    decision_log: list[DecisionLogEntry] = field(default_factory=list)
    rejected_suggestions: list[dict[str, Any]] = field(default_factory=list)
    version_history: list[dict[str, Any]] = field(default_factory=list)
    statistics: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_log": [d.to_dict() for d in self.decision_log],
            "rejected_suggestions": self.rejected_suggestions,
            "version_history": self.version_history,
            "statistics": self.statistics,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Internal":
        return cls(
            decision_log=[
                DecisionLogEntry.from_dict(d) for d in data.get("decision_log", [])
            ],
            rejected_suggestions=data.get("rejected_suggestions", []),
            version_history=data.get("version_history", []),
            statistics=data.get("statistics", {}),
        )


@dataclass
class StructureSpec:
    """
    The main Structure Specification document.
    
    This is what agents discuss in V3 - a YAML-based intermediate
    representation that describes WHAT to include, not HOW to format.
    """
    metadata: Metadata = field(default_factory=Metadata)
    organization: Organization = field(default_factory=Organization)
    sections: list[Section] = field(default_factory=list)
    learning_paths: list[LearningPath] = field(default_factory=list)
    progress_summary: ProgressSummary = field(default_factory=ProgressSummary)
    _internal: Internal = field(default_factory=Internal)
    
    def to_dict(self) -> dict[str, Any]:
        d = {
            "metadata": self.metadata.to_dict(),
            "organization": self.organization.to_dict(),
            "sections": [s.to_dict() for s in self.sections],
        }
        if self.learning_paths:
            d["learning_paths"] = [p.to_dict() for p in self.learning_paths]
        if self.progress_summary.enabled:
            d["progress_summary"] = self.progress_summary.to_dict()
        if (
            self._internal.decision_log
            or self._internal.rejected_suggestions
            or self._internal.version_history
        ):
            d["_internal"] = self._internal.to_dict()
        return d
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StructureSpec":
        return cls(
            metadata=Metadata.from_dict(data.get("metadata", {})),
            organization=Organization.from_dict(data.get("organization", {})),
            sections=[Section.from_dict(s) for s in data.get("sections", [])],
            learning_paths=[
                LearningPath.from_dict(p) for p in data.get("learning_paths", [])
            ],
            progress_summary=ProgressSummary.from_dict(
                data.get("progress_summary", {})
            ),
            _internal=Internal.from_dict(data.get("_internal", {})),
        )
    
    def get_all_problem_ids(self) -> set[str]:
        """Get all problem IDs referenced in this specification."""
        ids = set()
        for section in self.sections:
            for problem in section.content.problems:
                ids.add(problem.id)
            for subcat in section.content.subcategories:
                ids.update(subcat.problems)
        for path in self.learning_paths:
            for step in path.steps:
                ids.update(step.problems)
        return ids
    
    def get_section_by_id(self, section_id: str) -> Section | None:
        """Get a section by its ID."""
        for section in self.sections:
            if section.id == section_id:
                return section
        return None


# =============================================================================
# Validation Functions
# =============================================================================

class ValidationError(Exception):
    """Raised when Structure Spec validation fails."""
    pass


def validate_structure_spec(spec: dict[str, Any]) -> tuple[bool, list[str]]:
    """
    Validate a Structure Specification dictionary.
    
    Args:
        spec: Dictionary to validate
        
    Returns:
        Tuple of (is_valid, list of error messages)
    """
    errors = []
    
    # Required top-level keys
    required_keys = ["metadata", "organization", "sections"]
    for key in required_keys:
        if key not in spec:
            errors.append(f"Missing required key: {key}")
    
    # Check for Markdown (should not be present)
    spec_str = yaml.dump(spec)
    markdown_patterns = [
        (r"```", "Code block (```) found - should not contain Markdown"),
        (r"- \[[ x]\]", "Checkbox (- [x] or - [ ]) found"),
        (r"\*\*[^*]+\*\*", "Bold (**text**) found"),
        (r"__[^_]+__", "Bold (__text__) found"),
        (r"#{1,6}\s", "Heading (# text) found"),
    ]
    for pattern, msg in markdown_patterns:
        if re.search(pattern, spec_str):
            errors.append(f"Markdown detected: {msg}")
    
    # Check for URLs (should not be present)
    url_patterns = [
        r"https?://",
        r"www\.",
        r"github\.com",
        r"leetcode\.com",
    ]
    for pattern in url_patterns:
        if re.search(pattern, spec_str, re.IGNORECASE):
            errors.append(f"URL detected (pattern: {pattern})")
    
    # Validate sections structure
    if "sections" in spec:
        for i, section in enumerate(spec["sections"]):
            if not isinstance(section, dict):
                errors.append(f"Section {i} is not a dictionary")
                continue
            
            if "id" not in section:
                errors.append(f"Section {i} missing 'id'")
            if "name" not in section:
                errors.append(f"Section {i} missing 'name'")
            
            # Validate content
            content = section.get("content", {})
            problems = content.get("problems", [])
            for j, problem in enumerate(problems):
                if isinstance(problem, dict):
                    if "id" not in problem:
                        errors.append(f"Section {i}, problem {j} missing 'id'")
                elif not isinstance(problem, str):
                    errors.append(f"Section {i}, problem {j} has invalid type")
    
    is_valid = len(errors) == 0
    return is_valid, errors


def validate_final_output(output: str) -> tuple[bool, list[str]]:
    """
    Validate that final Markmap output has no process artifacts.
    
    Args:
        output: Final Markmap markdown string
        
    Returns:
        Tuple of (is_valid, list of error messages)
    """
    errors = []
    
    # Patterns that should NOT appear in final output
    forbidden_patterns = [
        (r"Round \d+ Summary", "Round summary header found"),
        (r"Optimizer Suggestions", "Optimizer suggestions found"),
        (r"Consensus Adopted", "Consensus section found"),
        (r"Conflicts Resolved", "Conflicts section found"),
        (r"Change Log", "Change log found"),
        (r"_internal", "Internal metadata found"),
        (r"_decisions", "Decision metadata found"),
        (r"strategist_response:", "Strategist response YAML found"),
        (r"conflict_responses:", "Conflict response YAML found"),
    ]
    
    for pattern, msg in forbidden_patterns:
        if re.search(pattern, output, re.IGNORECASE):
            errors.append(msg)
    
    is_valid = len(errors) == 0
    return is_valid, errors


# =============================================================================
# Parsing Functions
# =============================================================================

def parse_structure_spec(yaml_str: str) -> StructureSpec:
    """
    Parse a YAML string into a StructureSpec object.
    
    Args:
        yaml_str: YAML string to parse
        
    Returns:
        Parsed StructureSpec object
        
    Raises:
        ValidationError: If the YAML is invalid
    """
    try:
        data = yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML: {e}")
    
    if not isinstance(data, dict):
        raise ValidationError("YAML must be a dictionary at root level")
    
    is_valid, errors = validate_structure_spec(data)
    if not is_valid:
        raise ValidationError(f"Validation failed: {'; '.join(errors)}")
    
    return StructureSpec.from_dict(data)


def dump_structure_spec(spec: StructureSpec) -> str:
    """
    Dump a StructureSpec to YAML string.
    
    Args:
        spec: StructureSpec to dump
        
    Returns:
        YAML string representation
    """
    return yaml.dump(
        spec.to_dict(),
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
    )


def extract_yaml_from_response(response: str) -> str:
    """
    Extract YAML content from LLM response.
    
    Handles both:
    - Pure YAML responses
    - YAML wrapped in ```yaml ... ``` code blocks
    
    Args:
        response: LLM response string
        
    Returns:
        Extracted YAML string
    """
    # Try to extract from code block first
    code_block_pattern = r"```(?:yaml)?\s*(.*?)```"
    matches = re.findall(code_block_pattern, response, re.DOTALL)
    
    if matches:
        # Return the longest match (likely the main YAML content)
        return max(matches, key=len).strip()
    
    # If no code block, assume the entire response is YAML
    return response.strip()

