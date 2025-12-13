"""
Agent modules for AI Markmap generation and optimization.

V2 Agents:
- GeneratorAgent: Generalist/Specialist Markmap generators
- OptimizerAgent: Optimization and debate agents
- SummarizerAgent: Round summarization
- JudgeAgent: Final evaluation and voting

V3 Agents (Structure Specification based):
- PlannerAgent: Structure Specification generators
- StrategistAgent: Content strategy optimization
- IntegratorAgent: Suggestion integration
- EvaluatorAgent: Structure evaluation
- WriterAgentV3: Final Markmap rendering
"""

from .base_agent import BaseAgent

# V2 Agents
from .generator import GeneralistAgent, SpecialistAgent, create_generators
from .optimizer import OptimizerAgent, create_optimizers
from .summarizer import SummarizerAgent
from .judge import JudgeAgent, create_judges, aggregate_votes
from .writer import WriterAgent, create_writer

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
from .writer_v3 import WriterAgentV3, create_writer_v3

__all__ = [
    # Base
    "BaseAgent",
    # V2 Agents
    "GeneralistAgent",
    "SpecialistAgent",
    "create_generators",
    "OptimizerAgent",
    "create_optimizers",
    "SummarizerAgent",
    "JudgeAgent",
    "create_judges",
    "aggregate_votes",
    "WriterAgent",
    "create_writer",
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
    "WriterAgentV3",
    "create_writer_v3",
]

