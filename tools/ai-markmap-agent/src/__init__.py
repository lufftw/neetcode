"""
AI Markmap Agent - Multi-Agent Collaborative System for Markmap Generation.

This package provides a LangGraph-based pipeline that coordinates multiple
AI agents to generate high-quality Markmaps from NeetCode metadata.

Main components:
- agents: Generator, Optimizer, Summarizer, and Judge agents
- memory: Short-term (STM) and Long-term (LTM) memory systems
- compression: Content compression for token management
- output: HTML converter for final output generation
- graph: LangGraph workflow orchestration
"""

from .config_loader import ConfigLoader, load_config, get_api_key
from .data_sources import DataSourcesLoader, load_data_sources
from .graph import build_markmap_graph, run_pipeline, run_pipeline_async

__version__ = "0.1.0"

__all__ = [
    "ConfigLoader",
    "load_config",
    "get_api_key",
    "DataSourcesLoader",
    "load_data_sources",
    "build_markmap_graph",
    "run_pipeline",
    "run_pipeline_async",
]
