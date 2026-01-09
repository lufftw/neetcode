# =============================================================================
# Expert Agents
# =============================================================================
# Domain-specific experts who review and suggest improvements to Markmaps.
# Each expert brings a unique perspective: architecture, pedagogy, or practice.
# =============================================================================

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from .base_agent import BaseAgent


@dataclass
class Suggestion:
    """A single improvement suggestion from an expert."""
    id: str                     # e.g., "A1", "P2", "E3"
    expert_id: str              # Which expert made this suggestion
    type: str                   # add, modify, remove, reorder, clarify
    location: str               # Where in the Markmap
    what: str                   # What to change
    why: str                    # Rationale
    raw_text: str = ""          # Original text from LLM
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "expert_id": self.expert_id,
            "type": self.type,
            "location": self.location,
            "what": self.what,
            "why": self.why,
        }


@dataclass
class Vote:
    """An expert's vote on a suggestion."""
    suggestion_id: str
    voter_id: str
    vote: str                   # "agree", "modify", "disagree"
    rationale: str = ""
    modification: str = ""      # Only if vote is "modify"


@dataclass 
class AdoptionList:
    """An expert's final list of suggestions they endorse."""
    expert_id: str
    adopted_ids: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "expert_id": self.expert_id,
            "adopted_ids": self.adopted_ids,
        }


def parse_suggestions_from_response(response: str, expert_id: str) -> list[Suggestion]:
    """
    Parse suggestions from LLM response (standalone function for resume).
    
    Args:
        response: Raw LLM response text
        expert_id: Expert identifier (e.g., "architect", "professor")
        
    Returns:
        List of parsed Suggestion objects
    """
    suggestions = []
    
    # Pattern to match suggestion blocks
    # Looking for patterns like: ### A1: Title or ## A1 - Title
    suggestion_pattern = r'#{2,3}\s*([A-Z]\d+)[:\s-]+(.+?)(?=#{2,3}\s*[A-Z]\d+|$)'
    matches = re.findall(suggestion_pattern, response, re.DOTALL)
    
    for match in matches:
        suggestion_id = match[0]
        content = match[1].strip()
        
        # Extract fields
        type_match = re.search(r'\*\*Type\*\*:\s*(\w+)', content, re.IGNORECASE)
        location_match = re.search(r'\*\*Location\*\*:\s*(.+?)(?=\n\*\*|\n-|\n#|$)', content, re.IGNORECASE | re.DOTALL)
        what_match = re.search(r'\*\*What\*\*:\s*(.+?)(?=\n\*\*|\n-|\n#|$)', content, re.IGNORECASE | re.DOTALL)
        why_match = re.search(r'\*\*Why\*\*:\s*(.+?)(?=\n\*\*|\n-|\n#|$)', content, re.IGNORECASE | re.DOTALL)
        
        suggestions.append(Suggestion(
            id=suggestion_id,
            expert_id=expert_id,
            type=type_match.group(1).strip().lower() if type_match else "modify",
            location=location_match.group(1).strip() if location_match else "",
            what=what_match.group(1).strip() if what_match else content[:200],
            why=why_match.group(1).strip() if why_match else "",
            raw_text=content,
        ))
    
    return suggestions


def parse_adoption_list_from_response(response: str) -> list[str]:
    """
    Parse adoption list from discussion response (standalone function for resume).
    
    Args:
        response: Raw LLM discussion response text
        
    Returns:
        List of adopted suggestion IDs (e.g., ["A1", "P2", "E3"])
    """
    adopted_ids = []
    
    # Strategy 1: Look for explicit adoption section
    adoption_patterns = [
        r'(?:^|\n)#+\s*(?:My\s+)?Final\s+Adoption\s+List.*',
        r'I\s+recommend\s+adopting\s+(?:these\s+)?suggestions?:?\s*\n.*',
        r'(?:^|\n)#+\s*Part\s*2\s*:?\s*Final\s+Adoption.*',
    ]
    
    section_text = ""
    for pattern in adoption_patterns:
        match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
        if match:
            section_text = response[match.start():]
            break
    
    # Strategy 2: If no explicit section found, look for all ✅ Agree votes
    if not section_text:
        agree_pattern = r'\*\*Vote\*\*:\s*✅\s*Agree.*?(?:^|\n)#+\s*([APE]\d+)'
        agrees = re.findall(agree_pattern, response, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        if agrees:
            adopted_ids = list(dict.fromkeys(agrees))
    
    # Extract IDs from section text
    if section_text:
        ids = re.findall(r'\b([APE]\d+)\b', section_text)
        adopted_ids = list(dict.fromkeys(ids))
    
    return adopted_ids


class ExpertAgent(BaseAgent):
    """
    Base class for Expert agents.
    
    Experts review a baseline Markmap and suggest domain-specific improvements.
    Each expert has a unique focus area and evaluation criteria.
    """
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        emoji: str,
        focus: str,
        focus_areas: list[str],
        model_config: dict[str, Any],
        config: dict[str, Any] | None = None,
    ):
        super().__init__(agent_id, model_config, config)
        self.name = name
        self.emoji = emoji
        self.focus = focus
        self.focus_areas = focus_areas
        self.suggestion_prefix = agent_id[0].upper()  # A for architect, P for professor, etc.
    
    def _get_phase_instructions(self, phase: str, round_number: int) -> str:
        """
        Get phase-specific instructions.

        Note: These are intentionally concise. Detailed instructions are in
        the behavior prompts (architect-behavior.md, etc.). Phase instructions
        only emphasize key constraints to avoid redundancy and save tokens.
        """
        if phase == "review":
            # Key constraint: independent assessment (no cross-expert influence)
            return """**Independent Review** — Do NOT consider other experts' opinions.
Identify concrete improvements from your expertise. Be thorough but practical."""

        elif phase == "discussion":
            # Discussion template (discussion-behavior.md) already contains full instructions.
            # Only add minimal context here.
            return """**Group Discussion** — Review all suggestions, vote, and create your adoption list."""

        return ""
    
    def _prepare_review_input(
        self,
        state: dict[str, Any],
    ) -> dict[str, Any]:
        """Prepare input for the review phase (Round 1)."""
        baseline_markmap = state.get("baseline_markmap", "")
        ontology = state.get("ontology", {})
        problems = state.get("problems", {})
        
        # Get suggestion limits from config
        experts_config = self.config.get("experts", {})
        suggestions_config = experts_config.get("suggestions", {})
        min_suggestions = suggestions_config.get("min_per_expert", 5)
        max_suggestions = suggestions_config.get("max_per_expert", 10)
        
        return {
            "phase": "Independent Review",
            "round_number": 1,
            "phase_instructions": self._get_phase_instructions("review", 1),
            "baseline_markmap": baseline_markmap,
            "ontology_summary": self._format_ontology(ontology),
            "problem_data": self._format_problems(problems, baseline_markmap),
            "min_suggestions": min_suggestions,
            "max_suggestions": max_suggestions,
        }
    
    def _parse_baseline_sections(self, baseline: str) -> list[dict[str, Any]]:
        """
        Parse baseline markmap into sections based on ## headings.

        Returns list of sections:
        [{"heading": "Kernel 1: SubstringSlidingWindow", "content": "...", "line_start": 28, "line_end": 63}]
        """
        import re
        lines = baseline.split('\n')
        sections = []
        current_section = None

        for i, line in enumerate(lines):
            # Match ## headings (not # or ###)
            if re.match(r'^##\s+[^#]', line):
                # Save previous section
                if current_section:
                    current_section["line_end"] = i - 1
                    current_section["content"] = '\n'.join(
                        lines[current_section["line_start"]:i]
                    )
                    sections.append(current_section)

                # Start new section
                heading = re.sub(r'^##\s+', '', line).strip()
                current_section = {
                    "heading": heading,
                    "line_start": i,
                    "line_end": None,
                    "content": "",
                }

        # Don't forget the last section
        if current_section:
            current_section["line_end"] = len(lines) - 1
            current_section["content"] = '\n'.join(
                lines[current_section["line_start"]:]
            )
            sections.append(current_section)

        return sections

    def _extract_keywords_from_suggestions(
        self,
        suggestions: dict[str, list["Suggestion"]],
    ) -> set[str]:
        """
        Extract location keywords from all suggestions.

        Extracts:
        - Quoted strings: "Sliding Window"
        - Kernel references: Kernel 1, Kernel 2
        - Pattern names: sliding_window_unique
        - Section indicators: Two Pointers, Backtracking
        """
        import re
        keywords = set()

        for expert_suggestions in suggestions.values():
            for s in expert_suggestions:
                location = s.location.lower() if s.location else ""

                # Extract quoted strings
                quoted = re.findall(r'"([^"]+)"', s.location)
                keywords.update(q.lower() for q in quoted)

                # Extract Kernel references
                kernels = re.findall(r'kernel\s*(\d+)', location, re.IGNORECASE)
                keywords.update(f"kernel {k}" for k in kernels)

                # Extract pattern names (snake_case)
                patterns = re.findall(r'\b([a-z]+_[a-z_]+)\b', location)
                keywords.update(patterns)

                # Extract common section names
                common_sections = [
                    "sliding window", "two pointer", "backtracking",
                    "binary search", "dynamic programming", "dp",
                    "graph", "tree", "linked list", "heap", "stack",
                    "superhighway", "universe"
                ]
                for section in common_sections:
                    if section in location:
                        keywords.add(section)

        return keywords

    def _match_sections_to_keywords(
        self,
        sections: list[dict],
        keywords: set[str],
    ) -> list[dict]:
        """
        Match sections to keywords using fuzzy matching.

        Returns sections that match any keyword.
        Uses multiple matching strategies:
        1. Direct substring match
        2. Word-based match (ignoring case/spacing)
        3. Content pattern match
        """
        import re

        def normalize(text: str) -> str:
            """Normalize text for matching: lowercase, remove special chars."""
            return re.sub(r'[^a-z0-9]', '', text.lower())

        def words(text: str) -> set[str]:
            """Extract words from text."""
            return set(re.findall(r'[a-z]+', text.lower()))

        matched = []
        for section in sections:
            heading_lower = section["heading"].lower()
            heading_normalized = normalize(section["heading"])
            heading_words = words(section["heading"])
            content_lower = section["content"].lower()

            for kw in keywords:
                kw_normalized = normalize(kw)
                kw_words = words(kw)

                # Strategy 1: Direct substring match
                if kw in heading_lower or heading_lower in kw:
                    matched.append(section)
                    break

                # Strategy 2: Normalized match (ignore spaces, special chars)
                if kw_normalized in heading_normalized:
                    matched.append(section)
                    break

                # Strategy 3: Word overlap (e.g., "two pointer" matches "TwoPointersTraversal")
                if kw_words and kw_words.issubset(heading_words):
                    matched.append(section)
                    break

                # Strategy 4: Content pattern match (for snake_case patterns)
                if '_' in kw and kw in content_lower:
                    matched.append(section)
                    break

        return matched

    def _extract_relevant_baseline(
        self,
        baseline: str,
        suggestions: dict[str, list["Suggestion"]],
        min_sections: int = 2,
        fallback_ratio: float = 0.3,
    ) -> tuple[str, bool]:
        """
        Extract only the baseline sections relevant to the suggestions.

        Args:
            baseline: Full baseline markmap
            suggestions: All expert suggestions
            min_sections: Minimum sections to extract (safety threshold)
            fallback_ratio: If matched sections < this ratio of total, use full baseline

        Returns:
            Tuple of (extracted_content, is_full_baseline)
        """
        sections = self._parse_baseline_sections(baseline)

        if not sections:
            return baseline, True

        keywords = self._extract_keywords_from_suggestions(suggestions)

        if not keywords:
            return baseline, True

        matched = self._match_sections_to_keywords(sections, keywords)

        # Safety checks: fall back to full baseline if matching is too sparse
        if len(matched) < min_sections:
            return baseline, True

        if len(matched) / len(sections) < fallback_ratio:
            # Less than 30% matched - might miss important context
            return baseline, True

        # Build extracted content with section indicators
        lines = [
            f"*Showing {len(matched)}/{len(sections)} sections relevant to suggestions*",
            f"*Keywords matched: {', '.join(sorted(keywords)[:10])}*",
            "",
        ]

        for section in matched:
            lines.append(f"--- Section: {section['heading']} (lines {section['line_start']}-{section['line_end']}) ---")
            lines.append(section["content"])
            lines.append("")

        return '\n'.join(lines), False

    def _prepare_discussion_input(
        self,
        state: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Prepare input for the discussion phase (Round 2).

        Token optimization: Only includes baseline sections relevant to
        the suggestions, unless matching is too sparse (then falls back
        to full baseline for safety).
        """
        from pathlib import Path

        baseline_markmap = state.get("baseline_markmap", "")
        all_suggestions = state.get("expert_suggestions", {})

        # Token optimization: Extract only relevant baseline sections
        relevant_baseline, is_full = self._extract_relevant_baseline(
            baseline_markmap, all_suggestions
        )

        # Get own suggestions
        own_suggestions = all_suggestions.get(self.agent_id, [])
        own_suggestions_text = self._format_suggestions_list(own_suggestions)

        # Get other experts' suggestions
        architect_suggestions = self._format_suggestions_list(
            all_suggestions.get("architect", [])
        ) if self.agent_id != "architect" else "(Your own suggestions)"

        professor_suggestions = self._format_suggestions_list(
            all_suggestions.get("professor", [])
        ) if self.agent_id != "professor" else "(Your own suggestions)"

        engineer_suggestions = self._format_suggestions_list(
            all_suggestions.get("engineer", [])
        ) if self.agent_id != "engineer" else "(Your own suggestions)"

        # Load discussion behavior prompt
        base_dir = Path(__file__).parent.parent.parent
        discussion_prompt_path = base_dir / "prompts/experts/discussion-behavior.md"

        if discussion_prompt_path.exists():
            discussion_template = discussion_prompt_path.read_text(encoding="utf-8")
        else:
            discussion_template = self.behavior_prompt

        # Prepare focus reminder based on expert type
        focus_reminder = f"Focus areas: {', '.join(self.focus_areas)}"

        return {
            "phase": "Full Discussion",
            "round_number": 2,
            "own_suggestions": own_suggestions_text,
            "architect_suggestions": architect_suggestions,
            "professor_suggestions": professor_suggestions,
            "engineer_suggestions": engineer_suggestions,
            "baseline_markmap": relevant_baseline,
            "expert_name": self.name,
            "expert_focus_reminder": focus_reminder,
            "_discussion_template": discussion_template,
            "_baseline_is_full": is_full,  # For debugging/logging
        }
    
    def _format_ontology(self, ontology: dict[str, Any]) -> str:
        """Format ontology for prompt."""
        if not ontology:
            return "No ontology data available."
        
        lines = []
        for category, data in ontology.items():
            lines.append(f"**{category}**:")
            if isinstance(data, dict):
                for key, value in list(data.items())[:10]:  # Limit for tokens
                    if isinstance(value, list):
                        lines.append(f"  - {key}: {', '.join(str(v) for v in value[:5])}")
                    else:
                        lines.append(f"  - {key}: {value}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _extract_problem_ids_from_baseline(self, baseline: str) -> set[str]:
        """
        Extract LeetCode problem IDs mentioned in the baseline markmap.

        Matches patterns like:
        - LeetCode 3
        - LeetCode 76
        - [LeetCode 3 - Title](url)
        """
        import re
        # Match "LeetCode" followed by a number
        matches = re.findall(r'LeetCode\s+(\d+)', baseline, re.IGNORECASE)
        return set(matches)

    def _format_problems_tiered(
        self,
        problems: dict[str, Any],
        baseline: str,
    ) -> str:
        """
        Format problems with tiered detail levels to save tokens.

        Tier 1: Problems in baseline → Full table (ID, Title, Difficulty, Patterns)
        Tier 2: Other solved problems → Compact (ID + Difficulty)
        Tier 3: Unsolved problems → ID list only

        This preserves full context for problems experts will discuss,
        while reducing token usage for peripheral data.
        """
        if not problems:
            return "No problem data available."

        baseline_ids = self._extract_problem_ids_from_baseline(baseline)

        tier1_problems = []  # In baseline
        tier2_problems = []  # Solved, not in baseline
        tier3_ids = []       # Unsolved

        for key, problem in problems.items():
            if not isinstance(problem, dict):
                continue

            pid = str(problem.get("id", key))
            # Normalize ID (remove leading zeros for comparison)
            pid_normalized = pid.lstrip("0") or "0"

            # Check if has solution
            files = problem.get("files", {})
            has_solution = bool(files.get("solution"))

            if pid_normalized in baseline_ids or pid in baseline_ids:
                tier1_problems.append(problem)
            elif has_solution:
                tier2_problems.append(problem)
            else:
                tier3_ids.append(pid)

        lines = []

        # Tier 1: Full table for baseline problems
        if tier1_problems:
            lines.append("**Tier 1 — Problems in baseline (full detail):**")
            lines.append("| ID | Title | Difficulty | Patterns |")
            lines.append("|---|---|---|---|")
            for p in sorted(tier1_problems, key=lambda x: str(x.get("id", ""))):
                pid = p.get("id", "?")
                title = p.get("title", "Unknown")[:40]
                diff = p.get("difficulty", "?")
                patterns = ", ".join(p.get("patterns", [])[:3])
                lines.append(f"| {pid} | {title} | {diff} | {patterns} |")
            lines.append("")

        # Tier 2: Compact format for other solved problems
        if tier2_problems:
            lines.append("**Tier 2 — Other solved problems (compact):**")
            # Group by difficulty for readability
            by_diff = {"easy": [], "medium": [], "hard": []}
            for p in tier2_problems:
                diff = p.get("difficulty", "medium").lower()
                pid = p.get("id", "?")
                if diff in by_diff:
                    by_diff[diff].append(pid)

            for diff, pids in by_diff.items():
                if pids:
                    lines.append(f"- {diff.upper()}: {', '.join(sorted(pids)[:20])}")
                    if len(pids) > 20:
                        lines.append(f"  (+{len(pids) - 20} more)")
            lines.append("")

        # Tier 3: ID list only for unsolved
        if tier3_ids:
            lines.append(f"**Tier 3 — Unsolved ({len(tier3_ids)} problems):**")
            lines.append(f"IDs: {', '.join(sorted(tier3_ids)[:30])}")
            if len(tier3_ids) > 30:
                lines.append(f"(+{len(tier3_ids) - 30} more)")

        # Summary
        lines.insert(0, f"*Problem data: {len(tier1_problems)} in baseline, {len(tier2_problems)} solved, {len(tier3_ids)} unsolved*\n")

        return "\n".join(lines)

    def _format_problems(self, problems: dict[str, Any], baseline: str = "") -> str:
        """
        Format problems for prompt.

        If baseline is provided, uses tiered formatting to save tokens.
        Otherwise falls back to simple table format.
        """
        if baseline:
            return self._format_problems_tiered(problems, baseline)

        # Fallback: simple table (for backward compatibility)
        if not problems:
            return "No problem data available."

        lines = ["| ID | Title | Difficulty | Patterns |", "|---|---|---|---|"]

        for key, problem in list(problems.items())[:50]:
            if isinstance(problem, dict):
                pid = problem.get("id", key)
                title = problem.get("title", "Unknown")[:40]
                diff = problem.get("difficulty", "?")
                patterns = ", ".join(problem.get("patterns", [])[:3])
                lines.append(f"| {pid} | {title} | {diff} | {patterns} |")

        if len(problems) > 50:
            lines.append(f"| ... | ({len(problems) - 50} more problems) | | |")

        return "\n".join(lines)
    
    def _format_suggestions_list(self, suggestions: list[Suggestion]) -> str:
        """Format a list of suggestions for display."""
        if not suggestions:
            return "(No suggestions)"
        
        lines = []
        for s in suggestions:
            lines.append(f"""### {s.id}: {s.what[:60]}...
- **Type**: {s.type}
- **Location**: {s.location}
- **What**: {s.what}
- **Why**: {s.why}
""")
        return "\n".join(lines)
    
    def _parse_suggestions(self, response: str) -> list[Suggestion]:
        """Parse suggestions from LLM response."""
        suggestions = []
        
        # Pattern to match suggestion blocks
        # Looking for patterns like: ### A1: Title or ## A1 - Title
        suggestion_pattern = r'#{2,3}\s*([A-Z]\d+)[:\s-]+(.+?)(?=#{2,3}\s*[A-Z]\d+|$)'
        matches = re.findall(suggestion_pattern, response, re.DOTALL)
        
        for match in matches:
            suggestion_id = match[0]
            content = match[1].strip()
            
            # Extract fields
            type_match = re.search(r'\*\*Type\*\*:\s*(\w+)', content, re.IGNORECASE)
            location_match = re.search(r'\*\*Location\*\*:\s*(.+?)(?=\n\*\*|\n-|\n#|$)', content, re.IGNORECASE | re.DOTALL)
            what_match = re.search(r'\*\*What\*\*:\s*(.+?)(?=\n\*\*|\n-|\n#|$)', content, re.IGNORECASE | re.DOTALL)
            why_match = re.search(r'\*\*Why\*\*:\s*(.+?)(?=\n\*\*|\n-|\n#|$)', content, re.IGNORECASE | re.DOTALL)
            
            suggestions.append(Suggestion(
                id=suggestion_id,
                expert_id=self.agent_id,
                type=type_match.group(1).strip().lower() if type_match else "modify",
                location=location_match.group(1).strip() if location_match else "",
                what=what_match.group(1).strip() if what_match else content[:200],
                why=why_match.group(1).strip() if why_match else "",
                raw_text=content,
            ))
        
        return suggestions
    
    def _parse_adoption_list(self, response: str) -> AdoptionList:
        """Parse adoption list from discussion response."""
        adopted_ids = []
        
        # Strategy 1: Look for explicit adoption section
        # The regex was failing because "###" contains "##" 
        # Use a more robust pattern: find the adoption header and take everything after it
        adoption_patterns = [
            r'(?:^|\n)#+\s*(?:My\s+)?Final\s+Adoption\s+List.*',  # "### My Final Adoption List"
            r'I\s+recommend\s+adopting\s+(?:these\s+)?suggestions?:?\s*\n.*',  # "I recommend adopting..."
            r'(?:^|\n)#+\s*Part\s*2\s*:?\s*Final\s+Adoption.*',  # "## Part 2: Final Adoption..."
        ]
        
        section_text = ""
        for pattern in adoption_patterns:
            match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
            if match:
                # Take from match position to end of response
                section_text = response[match.start():]
                break
        
        # Strategy 2: If no explicit section found, look for all ✅ Agree votes
        if not section_text:
            # Fallback: collect IDs from ✅ Agree vote lines
            agree_pattern = r'\*\*Vote\*\*:\s*✅\s*Agree.*?(?:^|\n)#+\s*([APE]\d+)'
            agrees = re.findall(agree_pattern, response, re.IGNORECASE | re.DOTALL | re.MULTILINE)
            if agrees:
                adopted_ids = list(dict.fromkeys(agrees))
        
        # Extract IDs from section text
        if section_text:
            # Find all suggestion IDs (A1, P2, E3, etc.)
            # Match IDs that appear in list items or bold text
            ids = re.findall(r'\b([APE]\d+)\b', section_text)
            adopted_ids = list(dict.fromkeys(ids))  # Remove duplicates, preserve order
        
        return AdoptionList(
            expert_id=self.agent_id,
            adopted_ids=adopted_ids,
        )
    
    def review(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Conduct independent review (Round 1).
        
        Args:
            state: Workflow state with baseline_markmap
            
        Returns:
            Updated state with expert suggestions
        """
        input_data = self._prepare_review_input(state)
        response = self.invoke(input_data)
        
        # Parse suggestions
        suggestions = self._parse_suggestions(response)
        
        # Store in state
        if "expert_suggestions" not in state:
            state["expert_suggestions"] = {}
        state["expert_suggestions"][self.agent_id] = suggestions
        
        # Store raw response for debugging
        if "expert_raw_responses" not in state:
            state["expert_raw_responses"] = {}
        state["expert_raw_responses"][self.agent_id] = response
        
        return state
    
    def discuss(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Participate in full discussion (Round 2).
        
        Args:
            state: Workflow state with all expert suggestions
            
        Returns:
            Updated state with adoption list
        """
        input_data = self._prepare_discussion_input(state)
        
        # Use discussion template if available
        discussion_template = input_data.pop("_discussion_template", self.behavior_prompt)
        
        # Format the discussion prompt
        formatted_prompt = discussion_template.format(**input_data)
        messages = self._build_messages(formatted_prompt)
        
        # Save LLM input
        self._save_llm_call_input(messages, "discuss")
        
        response = self.llm.invoke(messages)
        
        # Save LLM output
        self._save_llm_call_output(response.content, "discuss")
        
        # Parse adoption list
        adoption_list = self._parse_adoption_list(response.content)
        
        # Store in state
        if "adoption_lists" not in state:
            state["adoption_lists"] = {}
        state["adoption_lists"][self.agent_id] = adoption_list
        
        # Store raw response
        if "discussion_raw_responses" not in state:
            state["discussion_raw_responses"] = {}
        state["discussion_raw_responses"][self.agent_id] = response.content
        
        return state
    
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Main processing method (for compatibility).
        Delegates to review() or discuss() based on current phase.
        """
        current_phase = state.get("current_phase", "review")
        
        if current_phase == "review":
            return self.review(state)
        elif current_phase == "discussion":
            return self.discuss(state)
        else:
            return self.review(state)


class ArchitectExpert(ExpertAgent):
    """Top Software Architect - focuses on API design and modularity."""
    
    def __init__(self, model_config: dict[str, Any], config: dict[str, Any] | None = None):
        focus_areas = model_config.get("focus_areas", [
            "API Kernel abstraction and composability",
            "Pattern relationships and modularity",
            "Code template reusability",
            "System design mapping",
        ])
        super().__init__(
            agent_id="architect",
            name="Top Software Architect",
            emoji="🏗️",
            focus="api_kernel_design",
            focus_areas=focus_areas,
            model_config=model_config,
            config=config,
        )


class ProfessorExpert(ExpertAgent):
    """Distinguished Algorithm Professor - focuses on correctness and pedagogy."""
    
    def __init__(self, model_config: dict[str, Any], config: dict[str, Any] | None = None):
        focus_areas = model_config.get("focus_areas", [
            "Concept accuracy and precision",
            "Learning progression and cognitive load",
            "Complexity analysis correctness",
            "Invariant descriptions",
        ])
        super().__init__(
            agent_id="professor",
            name="Distinguished Algorithm Professor",
            emoji="📚",
            focus="correctness_pedagogy",
            focus_areas=focus_areas,
            model_config=model_config,
            config=config,
        )


class EngineerExpert(ExpertAgent):
    """Senior Principal Engineer - focuses on practical value."""
    
    def __init__(self, model_config: dict[str, Any], config: dict[str, Any] | None = None):
        focus_areas = model_config.get("focus_areas", [
            "Interview frequency and importance",
            "Real-world engineering applications",
            "Trade-off explanations",
            "Knowledge discoverability",
        ])
        super().__init__(
            agent_id="engineer",
            name="Senior Principal Engineer",
            emoji="⚙️",
            focus="practical_value",
            focus_areas=focus_areas,
            model_config=model_config,
            config=config,
        )


def create_experts(config: dict[str, Any]) -> list[ExpertAgent]:
    """
    Create expert agents based on configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List of expert agents
    """
    experts = []
    experts_config = config.get("experts", {})
    enabled_experts = experts_config.get("enabled", ["architect", "professor", "engineer"])
    definitions = experts_config.get("definitions", {})
    
    expert_classes = {
        "architect": ArchitectExpert,
        "professor": ProfessorExpert,
        "engineer": EngineerExpert,
    }
    
    for expert_id in enabled_experts:
        if expert_id in expert_classes:
            expert_config = definitions.get(expert_id, {})
            expert = expert_classes[expert_id](
                model_config=expert_config,
                config=config,
            )
            experts.append(expert)
    
    return experts

