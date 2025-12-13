"""
Agent modules for AI Markmap generation and refinement.

Refinement Mode Agents:
- ExpertAgent: Domain-specific experts (Architect, Professor, Engineer)
- WriterAgent: Applies improvements to baseline Markmap
- TranslatorAgent: Language translation
"""

from .base_agent import BaseAgent

# Expert Agents (Refinement Mode)
from .expert import (
    ExpertAgent,
    ArchitectExpert,
    ProfessorExpert,
    EngineerExpert,
    Suggestion,
    Vote,
    AdoptionList,
    create_experts,
)

# Writer and Translator
from .writer import WriterAgent, create_writer
from .translator import TranslatorAgent, create_translators

__all__ = [
    # Base
    "BaseAgent",
    # Expert Agents
    "ExpertAgent",
    "ArchitectExpert",
    "ProfessorExpert",
    "EngineerExpert",
    "Suggestion",
    "Vote",
    "AdoptionList",
    "create_experts",
    # Writer and Translator
    "WriterAgent",
    "create_writer",
    "TranslatorAgent",
    "create_translators",
]
