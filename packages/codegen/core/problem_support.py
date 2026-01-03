"""
Problem support configuration reader.

Loads and validates problem-specific configuration from config/problem-support.yaml.

Reference: docs/contracts/problem-support-boundary.md
"""

from pathlib import Path
from typing import Dict, List, Optional, Any, Literal
from dataclasses import dataclass, field
import functools

try:
    import yaml
except ImportError:
    yaml = None


# =============================================================================
# Type Definitions
# =============================================================================

Tier = Literal["0", "1", "1.5", "2"]
CodecMode = Literal["import", "inline"]


@dataclass
class ProblemConfig:
    """Configuration for a single problem."""
    
    id: str
    tier: Tier = "0"
    codec_mode: CodecMode = "import"
    io_format: str = "primitive_to_primitive"
    codec_hints: List[str] = field(default_factory=list)
    inline_reason: Optional[str] = None
    
    # Generator flags
    random_generator: bool = True
    complexity_generator: bool = True
    
    def __post_init__(self):
        """Validate configuration."""
        if self.codec_mode == "inline" and not self.inline_reason:
            raise ValueError(
                f"Problem {self.id}: inline_reason is required when codec_mode is 'inline'"
            )
        
        # Tier-1.5 should default to no generators
        if self.tier == "1.5":
            # Only override if not explicitly set
            pass  # Keep defaults from config
    
    @property
    def requires_custom_adapter(self) -> bool:
        """Check if problem requires custom adapter in solve()."""
        return self.tier in ("1.5", "2")
    
    @property
    def supports_practice(self) -> bool:
        """Check if problem can be practiced (solution exists)."""
        # This would need to check filesystem, handled by caller
        return True
    
    @property
    def supports_auto_generation(self) -> bool:
        """Check if codegen can auto-generate solution from scratch."""
        return self.tier in ("0", "1")


# =============================================================================
# Config Loading
# =============================================================================

_CONFIG_CACHE: Optional[Dict[str, Any]] = None


def _get_config_path() -> Path:
    """Get path to problem-support.yaml."""
    # Try current directory first, then look for project root
    current = Path.cwd()
    markers = ["pyproject.toml", ".git", ".neetcode"]
    
    while current != current.parent:
        config_path = current / "config" / "problem-support.yaml"
        if config_path.exists():
            return config_path
        for marker in markers:
            if (current / marker).exists():
                return current / "config" / "problem-support.yaml"
        current = current.parent
    
    return Path.cwd() / "config" / "problem-support.yaml"


def _load_raw_config() -> Dict[str, Any]:
    """Load raw YAML config (cached)."""
    global _CONFIG_CACHE
    
    if _CONFIG_CACHE is not None:
        return _CONFIG_CACHE
    
    if yaml is None:
        raise ImportError("PyYAML is required for problem support config. Install with: pip install pyyaml")
    
    config_path = _get_config_path()
    
    if not config_path.exists():
        _CONFIG_CACHE = {"defaults": {}, "problems": {}}
        return _CONFIG_CACHE
    
    with open(config_path, 'r', encoding='utf-8') as f:
        _CONFIG_CACHE = yaml.safe_load(f) or {"defaults": {}, "problems": {}}
    
    return _CONFIG_CACHE


def reload_config() -> None:
    """Force reload of config (for testing)."""
    global _CONFIG_CACHE
    _CONFIG_CACHE = None


def get_defaults() -> Dict[str, Any]:
    """Get default configuration values."""
    config = _load_raw_config()
    return config.get("defaults", {})


def load_problem_config(problem_id: str) -> ProblemConfig:
    """
    Load configuration for a specific problem.
    
    Args:
        problem_id: Problem ID (e.g., "0142")
        
    Returns:
        ProblemConfig with merged defaults
    """
    config = _load_raw_config()
    defaults = config.get("defaults", {})
    problems = config.get("problems", {})
    
    # Normalize problem ID (ensure 4-digit format)
    normalized_id = problem_id.zfill(4) if problem_id.isdigit() else problem_id
    
    # Get problem-specific config or empty dict
    problem_data = problems.get(normalized_id, {})
    
    # Merge with defaults
    merged = {
        "id": normalized_id,
        "tier": problem_data.get("tier", defaults.get("tier", "0")),
        "codec_mode": problem_data.get("codec_mode", defaults.get("codec_mode", "import")),
        "io_format": problem_data.get("io_format", defaults.get("io_format", "primitive_to_primitive")),
        "codec_hints": problem_data.get("codec_hints", []),
        "inline_reason": problem_data.get("inline_reason"),
    }
    
    # Handle generators
    generators = problem_data.get("generators", {})
    merged["random_generator"] = generators.get("random", defaults.get("generators", {}).get("random", True))
    merged["complexity_generator"] = generators.get("complexity", defaults.get("generators", {}).get("complexity", True))
    
    return ProblemConfig(**merged)


def get_tier(problem_id: str) -> Tier:
    """
    Get tier for a problem.
    
    Args:
        problem_id: Problem ID
        
    Returns:
        Tier string ("0", "1", "1.5", or "2")
    """
    config = load_problem_config(problem_id)
    return config.tier


def get_codec_mode(problem_id: str) -> CodecMode:
    """
    Get codec_mode for a problem.
    
    Args:
        problem_id: Problem ID
        
    Returns:
        "import" or "inline"
    """
    config = load_problem_config(problem_id)
    return config.codec_mode


def get_codec_hints(problem_id: str) -> List[str]:
    """
    Get codec_hints for a problem.
    
    Args:
        problem_id: Problem ID
        
    Returns:
        List of codec function names
    """
    config = load_problem_config(problem_id)
    return config.codec_hints


def is_tier_1_5_or_higher(problem_id: str) -> bool:
    """Check if problem is Tier-1.5 or Tier-2."""
    tier = get_tier(problem_id)
    return tier in ("1.5", "2")


def validate_config(problem_id: str) -> List[str]:
    """
    Validate problem configuration.
    
    Args:
        problem_id: Problem ID
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    try:
        config = load_problem_config(problem_id)
    except ValueError as e:
        return [str(e)]
    
    # Check inline_reason for inline mode
    if config.codec_mode == "inline" and not config.inline_reason:
        errors.append(f"Problem {problem_id}: inline_reason required when codec_mode is 'inline'")
    
    # Check tier is valid
    valid_tiers = ("0", "1", "1.5", "2")
    if config.tier not in valid_tiers:
        errors.append(f"Problem {problem_id}: invalid tier '{config.tier}', must be one of {valid_tiers}")
    
    return errors


# =============================================================================
# Tier-2 Problems (Not Supported)
# =============================================================================

def get_tier2_problems() -> List[Dict[str, str]]:
    """
    Get list of Tier-2 (not supported) problems.
    
    Returns:
        List of {"id": ..., "name": ..., "reason": ...} dicts
    """
    config = _load_raw_config()
    return config.get("tier2", [])


def is_tier2(problem_id: str) -> bool:
    """Check if problem is Tier-2 (not supported)."""
    tier2_list = get_tier2_problems()
    normalized_id = problem_id.zfill(4) if problem_id.isdigit() else problem_id
    return any(p.get("id") == normalized_id for p in tier2_list)


# =============================================================================
# Utility Functions
# =============================================================================

def list_configured_problems() -> List[str]:
    """List all problem IDs with explicit configuration."""
    config = _load_raw_config()
    return list(config.get("problems", {}).keys())


def get_problems_by_tier(tier: Tier) -> List[str]:
    """
    Get all problems of a specific tier.
    
    Args:
        tier: Tier to filter by
        
    Returns:
        List of problem IDs
    """
    config = _load_raw_config()
    problems = config.get("problems", {})
    
    return [
        pid for pid, pdata in problems.items()
        if pdata.get("tier", "0") == tier
    ]

