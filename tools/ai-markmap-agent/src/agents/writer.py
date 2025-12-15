# =============================================================================
# Writer Agent
# =============================================================================
# Refinement Mode: Applies expert-approved improvements to baseline Markmap.
# This is the ONLY agent that produces the final Markdown output.
# =============================================================================

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base_agent import BaseAgent
from ..consensus import Suggestion, format_improvements_for_writer


class WriterAgent(BaseAgent):
    """
    Markmap Writer agent in refinement mode.
    
    Responsibilities:
    1. Load the baseline Markmap
    2. Receive list of adopted improvements
    3. Apply improvements surgically
    4. Verify links and formatting
    5. Produce the refined Markmap
    
    This is the ONLY agent that produces Markdown.
    """
    
    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialize the Writer agent.
        
        Args:
            config: Full configuration dict
        """
        from ..config_loader import ConfigLoader
        
        config = config or ConfigLoader.get_config()
        model_config = config.get("writer", config.get("models", {}).get("writer", {}))
        
        super().__init__(
            agent_id="writer",
            model_config=model_config,
            config=config,
        )
        
        # Load format guide
        self.format_guide = self._load_format_guide(model_config)
        
        # URL templates
        urls_config = config.get("urls", {})
        self.github_template = urls_config.get("github", {}).get(
            "solution_template",
            "https://github.com/lufftw/neetcode/blob/main/{solution_file}"
        )
    
    def _load_format_guide(self, model_config: dict) -> str:
        """Load the Markmap format guide."""
        format_guide_path = model_config.get(
            "format_guide",
            "prompts/writer/markmap_format_guide.md"
        )
        
        base_dir = Path(__file__).parent.parent.parent
        full_path = base_dir / format_guide_path
        
        if full_path.exists():
            return full_path.read_text(encoding="utf-8")
        
        return "Use standard Markmap markdown formatting."
    
    def _build_problems_lookup(self, problems: dict[str, Any]) -> dict[str, dict]:
        """Build a lookup dictionary for problems by ID."""
        lookup = {}
        
        for key, value in problems.items():
            if isinstance(value, dict):
                problem_id = value.get("id", key)
                # Normalize ID to 4 digits
                if isinstance(problem_id, str) and problem_id.isdigit():
                    problem_id = problem_id.zfill(4)
                lookup[problem_id] = value
                # Also store without leading zeros for flexibility
                lookup[str(int(problem_id))] = value
        
        return lookup
    
    def _format_problems_for_prompt(
        self,
        problems_lookup: dict[str, dict],
    ) -> str:
        """Format problems for the writer prompt."""
        if not problems_lookup:
            return "No problem data available."
        
        lines = ["| ID | Title | Slug | Has Solution |", "|---|---|---|---|"]
        
        seen = set()
        for pid, problem in list(problems_lookup.items())[:100]:
            if pid in seen:
                continue
            seen.add(pid)
            
            title = problem.get("title", "Unknown")[:50]
            slug = problem.get("slug", "")
            has_solution = "Yes" if problem.get("solution_file") else "No"
            lines.append(f"| {pid} | {title} | {slug} | {has_solution} |")
        
        return "\n".join(lines)
    
    def _format_ontology(self, ontology: dict[str, Any]) -> str:
        """Format ontology for prompt."""
        if not ontology:
            return "No ontology data available."
        
        lines = []
        for category, data in list(ontology.items())[:10]:
            lines.append(f"**{category}**:")
            if isinstance(data, dict):
                for key, value in list(data.items())[:5]:
                    lines.append(f"  - {key}: {value}")
            lines.append("")
        
        return "\n".join(lines)
    
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Generate the refined Markmap from baseline + improvements.
        
        Args:
            state: Workflow state containing:
                - baseline_markmap: The original Markmap to refine
                - adopted_suggestions: List of approved Suggestion objects
                - problems: Problem metadata for link generation
                - ontology: Ontology reference
                
        Returns:
            Updated state with final_markmap
        """
        # Get baseline
        baseline_markmap = state.get("baseline_markmap", "")
        if not baseline_markmap:
            print("    ⚠ No baseline markmap found")
            state["final_markmap"] = ""
            return state
        
        # Get adopted suggestions
        adopted_suggestions: list[Suggestion] = state.get("adopted_suggestions", [])
        
        # Format improvements for writer
        brief_list, detailed_descriptions = format_improvements_for_writer(adopted_suggestions)
        
        # Get problem metadata
        problems = state.get("problems", {})
        problems_lookup = self._build_problems_lookup(problems)
        
        # Get ontology
        ontology = state.get("ontology", {})
        
        # Build the prompt
        prompt = self.behavior_prompt.format(
            baseline_markmap=baseline_markmap,
            adopted_improvements=brief_list,
            improvement_details=detailed_descriptions,
            problem_data=self._format_problems_for_prompt(problems_lookup),
            github_template=self.github_template,
            ontology_summary=self._format_ontology(ontology),
        )
        
        messages = self._build_messages(prompt)
        
        # Save LLM input
        self._save_llm_call_input(messages, "write")
        
        response = self.llm.invoke(messages)
        
        # Save LLM output
        self._save_llm_call_output(response.content, "write")
        
        # Extract markdown from response (in case it's wrapped in code blocks)
        final_markmap = self._extract_markdown(response.content)
        
        state["final_markmap"] = final_markmap
        return state
    
    def _extract_markdown(self, response: str) -> str:
        """
        Extract markdown from response, removing any wrapping code blocks.
        
        Args:
            response: LLM response text
            
        Returns:
            Clean markdown content
        """
        import re
        
        # Check if response is wrapped in markdown code block
        code_block_pattern = r'^```(?:markdown|md)?\s*\n(.*?)```\s*$'
        match = re.match(code_block_pattern, response, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        # If not wrapped, return as-is (but strip leading/trailing whitespace)
        return response.strip()


def create_writer(config: dict[str, Any] | None = None) -> WriterAgent:
    """
    Create a Writer agent.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        WriterAgent instance
    """
    return WriterAgent(config)
