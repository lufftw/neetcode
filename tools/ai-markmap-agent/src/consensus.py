# =============================================================================
# Consensus Calculation Module
# =============================================================================
# Programmatic consensus calculation - no AI involved.
# Uses majority voting to determine which suggestions are adopted.
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass, field
from math import ceil
from typing import Any

from .agents.expert import Suggestion, AdoptionList


@dataclass
class ConsensusResult:
    """Result of consensus calculation."""
    adopted: list[str]                          # IDs of adopted suggestions
    rejected: list[str]                         # IDs of rejected suggestions
    votes: dict[str, dict[str, bool]]           # suggestion_id -> {expert_id: voted_for}
    vote_counts: dict[str, int]                 # suggestion_id -> count of votes
    threshold: float                            # Threshold used
    num_experts: int                            # Number of experts
    required_votes: int                         # Minimum votes needed
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "adopted": self.adopted,
            "rejected": self.rejected,
            "votes": self.votes,
            "vote_counts": self.vote_counts,
            "threshold": self.threshold,
            "num_experts": self.num_experts,
            "required_votes": self.required_votes,
        }
    
    def get_adoption_summary(self) -> str:
        """Get a human-readable summary of the consensus."""
        lines = [
            f"Consensus Summary (threshold: {self.threshold:.0%}, required: {self.required_votes}/{self.num_experts})",
            "",
            "✅ Adopted:",
        ]
        
        for sid in self.adopted:
            count = self.vote_counts.get(sid, 0)
            lines.append(f"  - {sid}: {count}/{self.num_experts} votes")
        
        lines.append("")
        lines.append("❌ Rejected:")
        
        for sid in self.rejected:
            count = self.vote_counts.get(sid, 0)
            lines.append(f"  - {sid}: {count}/{self.num_experts} votes")
        
        return "\n".join(lines)


def calculate_consensus(
    adoption_lists: dict[str, AdoptionList],
    all_suggestions: dict[str, list[Suggestion]],
    threshold: float = 0.67,
    min_votes: int | None = None,
) -> ConsensusResult:
    """
    Calculate consensus from expert adoption lists.
    
    This is pure Python code - no AI involved.
    
    Args:
        adoption_lists: Dict of expert_id -> AdoptionList
        all_suggestions: Dict of expert_id -> list of Suggestions
        threshold: Fraction of experts required (default 0.67 = 2/3)
        min_votes: Absolute minimum votes (overrides threshold if higher)
        
    Returns:
        ConsensusResult with adopted and rejected suggestions
    """
    num_experts = len(adoption_lists)
    
    if num_experts == 0:
        return ConsensusResult(
            adopted=[],
            rejected=[],
            votes={},
            vote_counts={},
            threshold=threshold,
            num_experts=0,
            required_votes=0,
        )
    
    # Calculate required votes
    required_votes = ceil(num_experts * threshold)
    if min_votes is not None:
        required_votes = max(required_votes, min_votes)
    
    # Collect all suggestion IDs
    all_suggestion_ids: set[str] = set()
    for suggestions in all_suggestions.values():
        for s in suggestions:
            all_suggestion_ids.add(s.id)
    
    # Count votes for each suggestion
    votes: dict[str, dict[str, bool]] = {}
    vote_counts: dict[str, int] = {}
    
    for sid in all_suggestion_ids:
        votes[sid] = {}
        vote_counts[sid] = 0
        
        for expert_id, adoption_list in adoption_lists.items():
            voted_for = sid in adoption_list.adopted_ids
            votes[sid][expert_id] = voted_for
            if voted_for:
                vote_counts[sid] += 1
    
    # Determine adopted vs rejected
    adopted = []
    rejected = []
    
    for sid in sorted(all_suggestion_ids):
        if vote_counts[sid] >= required_votes:
            adopted.append(sid)
        else:
            rejected.append(sid)
    
    return ConsensusResult(
        adopted=adopted,
        rejected=rejected,
        votes=votes,
        vote_counts=vote_counts,
        threshold=threshold,
        num_experts=num_experts,
        required_votes=required_votes,
    )


def get_suggestion_by_id(
    suggestion_id: str,
    all_suggestions: dict[str, list[Suggestion]],
) -> Suggestion | None:
    """
    Find a suggestion by its ID across all experts.
    
    Args:
        suggestion_id: The suggestion ID (e.g., "A1", "P2")
        all_suggestions: Dict of expert_id -> list of Suggestions
        
    Returns:
        The Suggestion if found, None otherwise
    """
    for suggestions in all_suggestions.values():
        for s in suggestions:
            if s.id == suggestion_id:
                return s
    return None


def get_adopted_suggestions(
    consensus: ConsensusResult,
    all_suggestions: dict[str, list[Suggestion]],
) -> list[Suggestion]:
    """
    Get the full Suggestion objects for all adopted suggestions.
    
    Args:
        consensus: ConsensusResult from calculate_consensus
        all_suggestions: Dict of expert_id -> list of Suggestions
        
    Returns:
        List of adopted Suggestion objects
    """
    adopted = []
    for sid in consensus.adopted:
        suggestion = get_suggestion_by_id(sid, all_suggestions)
        if suggestion:
            adopted.append(suggestion)
    return adopted


def format_improvements_for_writer(
    adopted_suggestions: list[Suggestion],
) -> tuple[str, str]:
    """
    Format adopted suggestions for the writer prompt.
    
    Args:
        adopted_suggestions: List of adopted Suggestion objects
        
    Returns:
        Tuple of (brief_list, detailed_descriptions)
    """
    if not adopted_suggestions:
        return "No improvements to apply.", "No improvements were adopted."
    
    # Brief list
    brief_lines = ["The following improvements were adopted by expert consensus:", ""]
    for s in adopted_suggestions:
        brief_lines.append(f"- **{s.id}**: {s.what[:80]}...")
    
    # Detailed descriptions
    detail_lines = []
    for s in adopted_suggestions:
        detail_lines.append(f"""### {s.id} ({s.expert_id.title()})
**Type**: {s.type}
**Location**: {s.location}
**What**: {s.what}
**Why**: {s.why}
""")
    
    return "\n".join(brief_lines), "\n".join(detail_lines)


def auto_threshold(num_experts: int) -> float:
    """
    Calculate an appropriate threshold based on number of experts.
    
    Logic:
    - Small groups (2-3): Need high agreement (2/3 = 0.67)
    - Medium groups (4-5): Standard majority (0.60)
    - Large groups (6+): Simple majority (0.5)
    
    Args:
        num_experts: Number of experts
        
    Returns:
        Recommended threshold value
    """
    if num_experts <= 3:
        return 0.67  # 2/3 for small groups
    elif num_experts <= 5:
        return 0.60  # 3/5 for medium groups
    else:
        return 0.50  # Simple majority for large groups

