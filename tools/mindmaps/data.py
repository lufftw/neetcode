# tools/mindmaps/data.py
"""Problem data structures for mind map generation."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from .config import DIFFICULTY_ICONS, get_config


@dataclass
class ProblemData:
    """Problem metadata."""
    id: str
    title: str
    slug: str = ""
    leetcode_id: int = 0
    url: str = ""
    difficulty: str = ""
    topics: list[str] = field(default_factory=list)
    companies: list[str] = field(default_factory=list)
    roadmaps: list[str] = field(default_factory=list)
    api_kernels: list[str] = field(default_factory=list)
    patterns: list[str] = field(default_factory=list)
    families: list[str] = field(default_factory=list)
    data_structures: list[str] = field(default_factory=list)
    algorithms: list[str] = field(default_factory=list)
    related_problems: list[str] = field(default_factory=list)
    is_base_template: bool = False
    base_for_kernel: str = ""
    derived_problems: list[str] = field(default_factory=list)
    solutions: list[dict[str, Any]] = field(default_factory=list)
    solution_file: str = ""
    generator_file: str = ""
    
    @property
    def display_name(self) -> str:
        num = self.leetcode_id if self.leetcode_id else int(self.id)
        return f"LeetCode {num} - {self.title}"
    
    @property
    def difficulty_icon(self) -> str:
        return DIFFICULTY_ICONS.get(self.difficulty.lower(), "⚪")
    
    def solution_link(self, use_github_link: bool | None = None) -> str:
        """Return link to solution file."""
        if self.solution_file:
            path = self.solution_file
        elif self.slug:
            path = f"solutions/{self.slug}.py"
        else:
            return ""
        
        if use_github_link is None:
            use_github_link = get_config().use_github_links
        
        if use_github_link:
            cfg = get_config()
            return f"{cfg.github_repo_url}/blob/{cfg.github_branch}/{path}"
        return f"../../{path}"
    
    def markdown_link(self, include_difficulty: bool = True, 
                      use_github_link: bool | None = None,
                      open_in_new_tab: bool = True) -> str:
        """Return markdown/HTML link."""
        num = self.leetcode_id if self.leetcode_id else int(self.id)
        name = f"LeetCode {num} - {self.title}"
        link = self.solution_link(use_github_link)
        
        if link and open_in_new_tab and link.startswith("http"):
            a_tag = f'<a href="{link}" target="_blank" rel="noopener noreferrer">{name}</a>'
            return f"{self.difficulty_icon} {a_tag}" if include_difficulty else a_tag
        
        if include_difficulty:
            return f"{self.difficulty_icon} [{name}]({link})" if link else f"{self.difficulty_icon} {name}"
        return f"[{name}]({link})" if link else name
    
    def leetcode_link(self) -> str:
        num = self.leetcode_id if self.leetcode_id else int(self.id)
        name = f"LeetCode {num} - {self.title}"
        return f"[{name}]({self.url})" if self.url else name
