# =============================================================================
# Writer Agent
# =============================================================================
# Final Markmap Writer responsible for producing polished output.
# Applies judge feedback, generates links, and uses proper formatting.
# =============================================================================

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base_agent import BaseAgent


class WriterAgent(BaseAgent):
    """
    Final Markmap Writer agent.
    
    Responsibilities:
    1. Apply judge feedback and suggestions
    2. Generate proper links (GitHub/LeetCode)
    3. Apply Markmap formatting (checkboxes, KaTeX, fold, etc.)
    4. Produce polished final output
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
    
    def generate_link(self, problem: dict) -> tuple[str, str, bool]:
        """
        Generate appropriate link for a problem.
        
        Args:
            problem: Problem metadata dict
            
        Returns:
            Tuple of (url, display_text, is_solved)
        """
        problem_id = problem.get("id", "")
        title = problem.get("title", "Unknown")
        slug = problem.get("slug", "")
        solution_file = problem.get("solution_file", "")
        
        # Format display text: "LeetCode {id} {title}"
        display_text = f"LeetCode {problem_id} {title}"
        
        if solution_file:
            # Has solution - use GitHub link
            url = self.github_template.format(solution_file=solution_file)
            return url, display_text, True
        else:
            # No solution - use LeetCode link
            url = self.leetcode_template.format(slug=slug)
            return url, display_text, False
    
    def build_problem_entry(self, problem: dict) -> str:
        """
        Build a formatted problem entry.
        
        Args:
            problem: Problem metadata dict
            
        Returns:
            Formatted markdown string
        """
        url, display_text, is_solved = self.generate_link(problem)
        
        # Checkbox and status icon
        checkbox = "[x]" if is_solved else "[ ]"
        status_icon = "✓" if is_solved else "○"
        
        # Difficulty
        difficulty = problem.get("difficulty", "")
        difficulty_str = f"**{difficulty}**" if difficulty else ""
        
        # Complexity
        time_complexity = problem.get("time_complexity", "")
        space_complexity = problem.get("space_complexity", "")
        
        complexity_parts = []
        if time_complexity:
            complexity_parts.append(f"${time_complexity}$ time")
        if space_complexity:
            complexity_parts.append(f"${space_complexity}$ space")
        complexity_str = " | ".join(complexity_parts)
        
        # Build entry
        entry = f"- {checkbox} [{display_text}]({url}) {status_icon}"
        
        # Add details line if we have any
        details = []
        if difficulty_str:
            details.append(difficulty_str)
        if complexity_str:
            details.append(complexity_str)
        
        if details:
            entry += f"\n  - {' | '.join(details)}"
        
        return entry
    
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Generate the final polished Markmap.
        
        Args:
            state: Workflow state containing:
                - selected_markmap: The judge-selected draft
                - judge_feedback: Feedback from judges
                - consensus_suggestions: Agreed improvements
                - problems: Full problem metadata
                
        Returns:
            Updated state with final_markmap
        """
        selected_markmap = state.get("selected_markmap", "")
        judge_feedback = state.get("judge_feedback", [])
        consensus_suggestions = state.get("consensus_suggestions", [])
        problems = state.get("problems", {})
        
        # Prepare problems lookup
        problems_list = []
        if isinstance(problems, dict):
            for key, value in problems.items():
                if isinstance(value, dict):
                    problems_list.append(value)
        
        # Build problems reference for the prompt
        problems_json = self._format_problems_for_prompt(problems_list)
        
        # Build feedback summary
        feedback_summary = self._format_feedback(judge_feedback, consensus_suggestions)
        
        # Build the prompt
        prompt = f"""You are tasked with producing the final, polished Markmap.

## Selected Markmap (Draft)

{selected_markmap}

## Judge Feedback and Suggestions

{feedback_summary}

## Problem Metadata (for generating links)

{problems_json}

## Markmap Format Guide

{self.format_guide}

## Your Task

1. Start with the selected markmap structure
2. Apply ALL judge suggestions (do not skip any)
3. For each problem reference, generate the correct link:
   - If `solution_file` exists → use GitHub: {self.github_template}
   - Otherwise → use LeetCode: {self.leetcode_template}
4. Use proper Markmap formatting:
   - YAML frontmatter with title and markmap settings
   - Checkboxes: `[x]` for solved (has solution_file), `[ ]` for unsolved
   - Status icons: ✓ for solved, ○ for unsolved
   - KaTeX for complexity: `$O(n)$`
   - Fold for dense sections: `<!-- markmap: fold -->`
5. Use "LeetCode" not "LC" for problem names

## Output

Produce ONLY the final Markmap markdown. No explanations."""

        messages = [{"role": "user", "content": prompt}]
        final_markmap = self._call_llm(messages)
        
        state["final_markmap"] = final_markmap
        return state
    
    def _format_problems_for_prompt(self, problems: list[dict]) -> str:
        """Format problems list for the prompt."""
        if not problems:
            return "No problem metadata available."
        
        lines = ["```json", "["]
        for i, p in enumerate(problems[:50]):  # Limit to 50 for token efficiency
            entry = {
                "id": p.get("id", ""),
                "title": p.get("title", ""),
                "slug": p.get("slug", ""),
                "difficulty": p.get("difficulty", ""),
                "patterns": p.get("patterns", []),
                "solution_file": p.get("solution_file", ""),
                "time_complexity": p.get("time_complexity", ""),
                "space_complexity": p.get("space_complexity", ""),
            }
            comma = "," if i < len(problems) - 1 and i < 49 else ""
            lines.append(f"  {entry}{comma}")
        
        if len(problems) > 50:
            lines.append(f"  // ... and {len(problems) - 50} more problems")
        
        lines.append("]")
        lines.append("```")
        return "\n".join(lines)
    
    def _format_feedback(
        self,
        judge_feedback: list[dict],
        consensus_suggestions: list[str],
    ) -> str:
        """Format judge feedback for the prompt."""
        lines = []
        
        if judge_feedback:
            lines.append("### Individual Judge Feedback\n")
            for fb in judge_feedback:
                judge_id = fb.get("judge_id", "Unknown")
                score = fb.get("score", "N/A")
                lines.append(f"**{judge_id}** (Score: {score}/100)")
                
                strengths = fb.get("strengths", [])
                if strengths:
                    lines.append("- Strengths:")
                    for s in strengths:
                        lines.append(f"  - {s}")
                
                improvements = fb.get("improvements", [])
                if improvements:
                    lines.append("- Improvements needed:")
                    for imp in improvements:
                        lines.append(f"  - {imp}")
                
                lines.append("")
        
        if consensus_suggestions:
            lines.append("### Consensus Suggestions (MUST apply all)\n")
            for i, suggestion in enumerate(consensus_suggestions, 1):
                lines.append(f"{i}. {suggestion}")
        
        if not lines:
            return "No specific feedback. Focus on applying proper formatting and links."
        
        return "\n".join(lines)


def create_writer(config: dict[str, Any] | None = None) -> WriterAgent:
    """
    Create a Writer agent.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        WriterAgent instance
    """
    return WriterAgent(config)

