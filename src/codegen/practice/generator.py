"""
Practice skeleton generator.

Generates practice files in practices/ directory,
reusing infrastructure from reference solutions when available.
"""

from pathlib import Path
from typing import Optional

from leetcode_datasource import LeetCodeDataSource

from ..core.config import CodeGenConfig, load_config
from ..core.assemble import assemble_module, assemble_practice_marker
from ..reference.generator import (
    generate_reference_skeleton,
    get_reference_path,
    reference_exists,
    _generate_skeleton_content,
)
from .reuse import (
    extract_infrastructure,
    transform_solutions_dict_for_practice,
    get_solution_classes_for_practice,
)


class PracticeGenerationResult:
    """Result of practice skeleton generation."""
    
    def __init__(
        self,
        success: bool,
        path: Optional[Path] = None,
        message: str = "",
        content: Optional[str] = None,
        history_path: Optional[Path] = None,
    ):
        self.success = success
        self.path = path
        self.message = message
        self.content = content
        self.history_path = history_path
    
    def __repr__(self) -> str:
        return f"PracticeGenerationResult(success={self.success}, path={self.path})"


def generate_practice_skeleton(
    problem_id: int,
    config: Optional[CodeGenConfig] = None,
    dry_run: bool = False,
    all_solutions: bool = False,
) -> PracticeGenerationResult:
    """
    Generate practice skeleton for a LeetCode problem.
    
    If a reference solution exists, reuse its infrastructure.
    Otherwise, generate a fresh skeleton.
    
    Args:
        problem_id: LeetCode frontend question ID
        config: CodeGen configuration
        dry_run: If True, only generate content without writing
        all_solutions: If True, include all Solution classes
        
    Returns:
        PracticeGenerationResult with success status and details
    """
    if config is None:
        config = load_config()
    
    # Get problem slug for filename
    ds = LeetCodeDataSource()
    slug = ds.get_slug(problem_id)
    
    if not slug:
        # Try to fetch from network
        try:
            question = ds.get_by_frontend_id(problem_id)
            slug = question.titleSlug
        except Exception as e:
            return PracticeGenerationResult(
                success=False,
                message=f"Failed to fetch problem {problem_id}: {e}",
            )
    
    # Determine paths
    slug_underscore = slug.replace("-", "_")
    filename = f"{problem_id:04d}_{slug_underscore}.py"
    practice_path = config.practices_path / filename
    reference_path = config.solutions_path / filename
    
    # Handle existing practice file
    history_path = None
    if practice_path.exists() and not dry_run:
        history_path = _save_to_history(practice_path, config)
    
    # Determine generation strategy
    if reference_path.exists():
        # Reuse from reference
        content = _generate_from_reference(
            reference_path,
            config,
            all_solutions=all_solutions,
        )
        reuse_msg = f"   (reusing infrastructure from {reference_path.name})"
    else:
        # Generate fresh skeleton
        try:
            question = ds.get_by_frontend_id(problem_id)
            content = _generate_skeleton_content(question, config)
            reuse_msg = ""
        except Exception as e:
            return PracticeGenerationResult(
                success=False,
                message=f"Failed to generate skeleton: {e}",
            )
    
    if dry_run:
        return PracticeGenerationResult(
            success=True,
            path=practice_path,
            message="Dry run - content generated but not written",
            content=content,
        )
    
    # Ensure directory exists
    config.practices_path.mkdir(parents=True, exist_ok=True)
    
    # Write file
    practice_path.write_text(content, encoding="utf-8")
    
    # Build success message
    messages = []
    if history_path:
        messages.append(f"ℹ️  Existing practice saved to: {history_path.name}")
    messages.append(f"✅ Created: {practice_path}{reuse_msg}")
    
    return PracticeGenerationResult(
        success=True,
        path=practice_path,
        message="\n".join(messages),
        content=content,
        history_path=history_path,
    )


def _generate_from_reference(
    reference_path: Path,
    config: CodeGenConfig,
    all_solutions: bool = False,
) -> str:
    """Generate practice content by reusing reference infrastructure."""
    
    # Extract all components from reference
    infra = extract_infrastructure(reference_path)
    
    # Determine mode
    mode = "all" if all_solutions else "single"
    
    # Transform SOLUTIONS dict
    solutions_dict = transform_solutions_dict_for_practice(
        infra.solutions_dict_raw,
        mode=mode,
    )
    
    # Get cleared Solution classes with practice marker
    practice_marker = assemble_practice_marker(
        reference_path=reference_path.name,
        solution_count=infra.solution_count,
    )
    
    solution_classes = get_solution_classes_for_practice(infra, mode=mode)
    solution_section = f"{practice_marker}\n{solution_classes}"
    
    # Assemble the practice file
    return assemble_module(
        header=infra.header,
        imports=infra.imports,
        helpers=infra.helper_classes.strip(),
        judge_func=infra.judge_func.strip(),
        solutions_dict=solutions_dict,
        solution_classes=solution_section,
        helper_functions=infra.helper_functions.strip(),
        solve_fn=infra.solve_fn,
    )


def _save_to_history(practice_path: Path, config: CodeGenConfig) -> Path:
    """
    Save existing practice file to history.
    
    Args:
        practice_path: Path to existing practice file
        config: CodeGen configuration
        
    Returns:
        Path to the saved history file
    """
    from datetime import datetime
    
    # Ensure history directory exists
    history_dir = config.history_path
    history_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create history filename (preserves .py extension)
    history_filename = f"{practice_path.name}.{timestamp}.bak"
    history_path = history_dir / history_filename
    
    # Copy content
    content = practice_path.read_text(encoding="utf-8")
    history_path.write_text(content, encoding="utf-8")
    
    return history_path


def get_practice_path(problem_id: int, config: Optional[CodeGenConfig] = None) -> Path:
    """
    Get the expected path for a practice file.
    
    Args:
        problem_id: LeetCode frontend question ID
        config: CodeGen configuration
        
    Returns:
        Path to the practice file
    """
    if config is None:
        config = load_config()
    
    ds = LeetCodeDataSource()
    slug = ds.get_slug(problem_id)
    
    if slug:
        slug = slug.replace("-", "_")
        filename = f"{problem_id:04d}_{slug}.py"
    else:
        filename = f"{problem_id:04d}_unknown.py"
    
    return config.practices_path / filename


def practice_exists(problem_id: int, config: Optional[CodeGenConfig] = None) -> bool:
    """
    Check if a practice file exists.
    
    Args:
        problem_id: LeetCode frontend question ID
        config: CodeGen configuration
        
    Returns:
        True if practice exists
    """
    path = get_practice_path(problem_id, config)
    return path.exists()

