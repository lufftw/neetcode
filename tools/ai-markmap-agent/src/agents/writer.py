# =============================================================================
# Writer Agent
# =============================================================================
# Reads Structure Specification and generates final Markmap Markdown.
# This is the ONLY agent that produces Markdown output.
# =============================================================================

from __future__ import annotations

import yaml
from pathlib import Path
from typing import Any

from .base_agent import BaseAgent
from ..schema import StructureSpec, dump_structure_spec


class WriterAgent(BaseAgent):
    """
    Markmap Writer agent.
    
    Responsibilities:
    1. Read Structure Specification (YAML)
    2. Apply evaluator feedback and suggestions
    3. Look up full problem metadata by ID
    4. Generate proper links (GitHub/LeetCode)
    5. Apply Markmap formatting (checkboxes, KaTeX, fold, etc.)
    6. Produce complete Markmap Markdown output
    
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
        model_config = config["models"]["writer"]
        
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
        self.leetcode_template = urls_config.get("leetcode", {}).get(
            "problem_template",
            "https://leetcode.com/problems/{slug}/"
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
        
        return "# Markmap Format Guide\n\nUse standard markdown formatting."
    
    def _build_problems_lookup(self, problems: dict[str, Any]) -> dict[str, dict]:
        """Build a lookup dictionary for problems by ID."""
        lookup = {}
        
        for key, value in problems.items():
            if isinstance(value, dict):
                problem_id = value.get("id", key)
                # Normalize ID to 4 digits
                if problem_id.isdigit():
                    problem_id = problem_id.zfill(4)
                lookup[problem_id] = value
        
        return lookup
    
    def _format_spec_for_prompt(self, spec: StructureSpec) -> str:
        """Format Structure Specification for the prompt."""
        return dump_structure_spec(spec)
    
    def _format_problems_for_prompt(
        self,
        spec: StructureSpec,
        problems_lookup: dict[str, dict],
    ) -> str:
        """Format relevant problems with full metadata for the prompt."""
        # Get all problem IDs from spec
        problem_ids = spec.get_all_problem_ids()
        
        if not problem_ids:
            return "No problems referenced in the structure specification."
        
        lines = ["```json", "["]
        
        for i, pid in enumerate(sorted(problem_ids)):
            problem = problems_lookup.get(pid, {})
            if not problem:
                # Try without leading zeros
                problem = problems_lookup.get(pid.lstrip("0"), {})
            
            entry = {
                "id": pid,
                "title": problem.get("title", f"Problem {pid}"),
                "slug": problem.get("slug", ""),
                "difficulty": problem.get("difficulty", ""),
                "patterns": problem.get("patterns", []),
                "solution_file": problem.get("solution_file", ""),
                "has_solution": bool(problem.get("solution_file", "")),
                "time_complexity": problem.get("time_complexity", ""),
                "space_complexity": problem.get("space_complexity", ""),
            }
            
            comma = "," if i < len(problem_ids) - 1 else ""
            lines.append(f"  {entry}{comma}")
        
        lines.append("]")
        lines.append("```")
        
        return "\n".join(lines)
    
    def _format_evaluator_feedback(
        self,
        evaluator_results: dict[str, dict],
        evaluator_suggestions: list[str],
    ) -> str:
        """Format evaluator feedback for the prompt."""
        lines = []
        
        if evaluator_results:
            lines.append("### Evaluator Assessments\n")
            for eval_id, result in evaluator_results.items():
                name = result.get("evaluator_name", eval_id)
                score = result.get("overall_score", 0)
                approved = result.get("approved", False)
                
                status = "✓ Approved" if approved else "⚠ Needs Improvement"
                lines.append(f"**{name}** (Score: {score}/10) - {status}")
                
                strengths = result.get("strengths", [])
                if strengths:
                    lines.append("- Strengths:")
                    for s in strengths:
                        lines.append(f"  - {s}")
                
                improvements = result.get("improvements", [])
                if improvements:
                    lines.append("- Improvements:")
                    for imp in improvements:
                        lines.append(f"  - {imp}")
                
                lines.append("")
        
        if evaluator_suggestions:
            lines.append("### Suggestions to Apply\n")
            for i, suggestion in enumerate(evaluator_suggestions, 1):
                lines.append(f"{i}. {suggestion}")
        
        if not lines:
            return "No specific feedback. Apply standard formatting."
        
        return "\n".join(lines)
    
    def _format_pattern_docs(self, patterns: dict[str, Any]) -> str:
        """Format pattern docs for correct naming and structure."""
        if not patterns:
            return "No pattern documentation available."
        
        lines = []
        for pattern_name, pattern_data in patterns.items():
            lines.append(f"## {pattern_name}")
            
            if isinstance(pattern_data, dict):
                sub_patterns = pattern_data.get("sub_patterns", [])
                if sub_patterns:
                    lines.append("Sub-patterns:")
                    for sp in sub_patterns:
                        if isinstance(sp, dict):
                            sp_name = sp.get("name", "Unknown")
                            sp_desc = sp.get("description", "")
                            lines.append(f"  - **{sp_name}**: {sp_desc}")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Generate the final Markmap from Structure Specification.
        
        Args:
            state: Workflow state containing:
                - current_structure_spec: The final Structure Specification
                - evaluator_results: Evaluator assessments
                - problems: Full problem metadata
                - patterns: Pattern documentation
                
        Returns:
            Updated state with final_markmap
        """
        # Get Structure Specification
        spec = state.get("current_structure_spec")
        if not isinstance(spec, StructureSpec):
            if isinstance(spec, dict):
                spec = StructureSpec.from_dict(spec)
            else:
                print("    ⚠ No valid Structure Specification found")
                state["final_markmap"] = ""
                return state
        
        # Get problem metadata
        problems = state.get("problems", {})
        problems_lookup = self._build_problems_lookup(problems)
        
        # Get evaluator feedback
        evaluator_results = state.get("evaluator_results", {})
        evaluator_suggestions = state.get("evaluator_suggestions", [])
        
        # Get pattern docs for correct naming
        patterns = state.get("patterns", {})
        
        # Format inputs
        spec_yaml = self._format_spec_for_prompt(spec)
        problems_json = self._format_problems_for_prompt(spec, problems_lookup)
        feedback = self._format_evaluator_feedback(evaluator_results, evaluator_suggestions)
        pattern_docs = self._format_pattern_docs(patterns)
        
        # Build the prompt
        prompt = f"""You are the Markmap Writer. Your job is to transform a Structure Specification (YAML) into final Markmap Markdown.

## Structure Specification

This defines WHAT to include and HOW to organize it:

```yaml
{spec_yaml}
```

## Problem Metadata

Use this to generate correct links and details:

{problems_json}

## Evaluator Feedback

Apply these improvements:

{feedback}

## Pattern Documentation

Use correct naming from here:

{pattern_docs}

## Markmap Format Guide

{self.format_guide}

## URL Templates

- For problems WITH solution_file: `{self.github_template}`
- For problems WITHOUT solution_file: `{self.leetcode_template}`

## Your Task

Transform the Structure Specification into final Markmap Markdown:

1. **Parse the Structure Spec**
   - Follow the `organization` settings
   - Create sections from `sections` array
   - Include `learning_paths` if enabled
   - Include `progress_summary` if enabled

2. **Generate Problem Entries**
   - Look up each problem ID in the metadata
   - Use correct title, difficulty, complexity from metadata
   - Generate checkbox: `[x]` if has_solution, `[ ]` otherwise
   - Generate status icon: ✓ if solved, ○ otherwise
   - Generate correct URL based on solution_file presence

3. **Apply Format Hints**
   - `should_fold: true` → add `<!-- markmap: fold -->` comment
   - `highlight_level: emphasized` → use **bold** for section name
   - `use_table: true` → render as table

4. **Apply Evaluator Suggestions**
   - Make all suggested improvements

5. **Final Formatting**
   - Add YAML frontmatter with title and markmap settings
   - Use KaTeX for complexity: `$O(n)$`
   - Use proper heading levels
   - Use "LeetCode" not "LC"
   - DO NOT include any process artifacts (_internal, _decisions, etc.)

## Output

Produce ONLY the final Markmap markdown. No explanations, no YAML, just the finished Markdown document."""

        messages = self._build_messages(prompt)
        
        # Save LLM input
        self._save_llm_call_input(messages, "write")
        
        response = self.llm.invoke(messages)
        
        # Save LLM output
        self._save_llm_call_output(response.content, "write")
        
        state["final_markmap"] = response.content
        return state


def create_writer(config: dict[str, Any] | None = None) -> WriterAgent:
    """
    Create a Writer agent.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        WriterAgent instance
    """
    return WriterAgent(config)

