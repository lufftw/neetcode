"""
CodeGen configuration.

Handles configuration loading and merging from:
- CLI flags (highest priority)
- .neetcode/codegen.toml
- Package defaults (lowest priority)
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional, Dict, Any
import os

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Fallback for older Python


# Type aliases
HeaderLevel = Literal["minimal", "standard", "full"]
HelperMode = Literal["inline", "import", "none"]
SolveMode = Literal["placeholder", "infer"]
MultiSolutionMode = Literal["single", "all"]


@dataclass
class CodeGenConfig:
    """
    CodeGen configuration.
    
    Attributes:
        header_level: Level of detail in solution header
        helper_mode: How to emit helper classes
        solve_mode: How to generate solve() function
        multi_solution_mode: How to handle multiple solutions in practice
        project_root: Project root directory
        solutions_dir: Directory for reference solutions
        practices_dir: Directory for practice files
    """
    
    # Header settings
    header_level: HeaderLevel = "full"
    
    # Helper settings
    helper_mode: HelperMode = "inline"
    
    # Skeleton settings
    solve_mode: SolveMode = "placeholder"
    
    # Practice settings
    multi_solution_mode: MultiSolutionMode = "single"
    
    # Paths (will be resolved relative to project_root)
    project_root: Optional[Path] = None
    solutions_dir: str = "solutions"
    practices_dir: str = "practices"
    
    def __post_init__(self):
        """Resolve project root if not set."""
        if self.project_root is None:
            self.project_root = _find_project_root()
    
    @property
    def solutions_path(self) -> Path:
        """Get absolute path to solutions directory."""
        return self.project_root / self.solutions_dir
    
    @property
    def practices_path(self) -> Path:
        """Get absolute path to practices directory."""
        return self.project_root / self.practices_dir
    
    @property
    def history_path(self) -> Path:
        """Get absolute path to practice history directory."""
        return self.practices_path / "_history"


def load_config(
    config_path: Optional[Path] = None,
    cli_overrides: Optional[Dict[str, Any]] = None,
) -> CodeGenConfig:
    """
    Load configuration with priority: CLI > file > defaults.
    
    Args:
        config_path: Path to config file (default: .neetcode/codegen.toml)
        cli_overrides: CLI flag overrides
        
    Returns:
        Merged CodeGenConfig
    """
    # Start with defaults
    config_dict: Dict[str, Any] = {}
    
    # Load from file if exists
    if config_path is None:
        project_root = _find_project_root()
        config_path = project_root / ".neetcode" / "codegen.toml"
    
    if config_path.exists():
        file_config = _load_toml_config(config_path)
        config_dict.update(file_config)
    
    # Apply CLI overrides
    if cli_overrides:
        config_dict.update(cli_overrides)
    
    # Create config object
    return _dict_to_config(config_dict)


def _find_project_root() -> Path:
    """
    Find project root by looking for marker files.
    
    Looks for: pyproject.toml, .git, .neetcode/
    """
    current = Path.cwd()
    markers = ["pyproject.toml", ".git", ".neetcode"]
    
    while current != current.parent:
        for marker in markers:
            if (current / marker).exists():
                return current
        current = current.parent
    
    # Fallback to cwd
    return Path.cwd()


def _load_toml_config(path: Path) -> Dict[str, Any]:
    """Load and flatten TOML config."""
    with open(path, "rb") as f:
        data = tomllib.load(f)
    
    # Flatten nested sections
    flat: Dict[str, Any] = {}
    
    if "header" in data:
        flat["header_level"] = data["header"].get("level")
    
    if "helpers" in data:
        flat["helper_mode"] = data["helpers"].get("mode")
    
    if "skeleton" in data:
        flat["solve_mode"] = data["skeleton"].get("solve_mode")
    
    if "practice" in data:
        flat["multi_solution_mode"] = data["practice"].get("multi_solution_mode")
    
    if "paths" in data:
        flat["solutions_dir"] = data["paths"].get("solutions")
        flat["practices_dir"] = data["paths"].get("practices")
    
    # Remove None values
    return {k: v for k, v in flat.items() if v is not None}


def _dict_to_config(d: Dict[str, Any]) -> CodeGenConfig:
    """Convert dict to CodeGenConfig, ignoring unknown keys."""
    valid_keys = {
        "header_level",
        "helper_mode",
        "solve_mode",
        "multi_solution_mode",
        "project_root",
        "solutions_dir",
        "practices_dir",
    }
    
    filtered = {k: v for k, v in d.items() if k in valid_keys}
    
    # Convert project_root string to Path if needed
    if "project_root" in filtered and isinstance(filtered["project_root"], str):
        filtered["project_root"] = Path(filtered["project_root"])
    
    return CodeGenConfig(**filtered)


# Default configuration instance
DEFAULT_CONFIG = CodeGenConfig()

