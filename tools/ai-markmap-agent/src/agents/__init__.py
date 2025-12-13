"""
Agent modules for AI Markmap generation and optimization.

V3 Agents (Structure Specification based):
- PlannerAgent: Structure Specification generators
- StrategistAgent: Content strategy optimization
- IntegratorAgent: Suggestion integration
- EvaluatorAgent: Structure evaluation
- WriterAgentV3: Final Markmap rendering
- TranslatorAgent: Language translation
"""

from .base_agent import BaseAgent

# V3 Agents
from .planner import (
    StructurePlannerAgent,
    GeneralistPlannerAgent,
    SpecialistPlannerAgent,
    create_planners,
)
from .strategist import (
    ContentStrategistAgent,
    ArchitectStrategist,
    ProfessorStrategist,
    UXStrategist,
    create_strategists,
)
from .integrator import (
    IntegratorAgent,
    create_integrator,
    calculate_consensus,
)
from .evaluator import (
    EvaluatorAgent,
    StructureEvaluator,
    ContentEvaluator,
    create_evaluators,
    aggregate_evaluations,
)
from .writer import WriterAgent, create_writer
from .translator import TranslatorAgent, create_translators

__all__ = [
    # Base
    "BaseAgent",
    # V3 Agents
    "StructurePlannerAgent",
    "GeneralistPlannerAgent",
    "SpecialistPlannerAgent",
    "create_planners",
    "ContentStrategistAgent",
    "ArchitectStrategist",
    "ProfessorStrategist",
    "UXStrategist",
    "create_strategists",
    "IntegratorAgent",
    "create_integrator",
    "calculate_consensus",
    "EvaluatorAgent",
    "StructureEvaluator",
    "ContentEvaluator",
    "create_evaluators",
    "aggregate_evaluations",
    "WriterAgent",
    "create_writer",
    "TranslatorAgent",
    "create_translators",
]
