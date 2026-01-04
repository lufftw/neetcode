"""
Reference skeleton generator.

Generates canonical solution files in solutions/ directory.
"""

from pathlib import Path
from typing import Optional, Tuple

from leetcode_datasource import LeetCodeDataSource, Question

from ..core.config import CodeGenConfig, load_config, HeaderLevel
from ..core.solution_header import render_solution_header
from ..core.stub_parser import parse_code_stub, format_params_for_signature
from ..core.helpers import (
    detect_required_helpers,
    emit_helpers,
    emit_helper_functions,
    HelperEmitMode,
)
from ..core.helpers.detect import detect_helper_functions, suggest_imports
from ..core.helpers.emit import emit_typing_imports, emit_all_imports
from ..core.assemble import (
    assemble_module,
    assemble_solutions_dict,
    assemble_solution_class,
    assemble_solve_function,
)
from ..core.io_schema import infer_io_schema
from ..core.solve_generator import generate_solve_function
from ..core.tiered_solve_generator import generate_tiered_solve
from ..core.problem_support import load_problem_config, get_tier


class ReferenceGenerationResult:
    """Result of reference skeleton generation."""
    
    def __init__(
        self,
        success: bool,
        path: Optional[Path] = None,
        message: str = "",
        content: Optional[str] = None,
    ):
        self.success = success
        self.path = path
        self.message = message
        self.content = content
    
    def __repr__(self) -> str:
        return f"ReferenceGenerationResult(success={self.success}, path={self.path})"


def generate_reference_skeleton(
    problem_id: int,
    config: Optional[CodeGenConfig] = None,
    dry_run: bool = False,
    header_level: Optional[HeaderLevel] = None,
    codec_mode_override: Optional[str] = None,
) -> ReferenceGenerationResult:
    """
    Generate reference skeleton for a LeetCode problem.
    
    Args:
        problem_id: LeetCode frontend question ID (e.g., 1 for Two Sum)
        config: CodeGen configuration (uses defaults if None)
        dry_run: If True, only generate content without writing file
        header_level: Override header level from config
        
    Returns:
        ReferenceGenerationResult with success status and details
        
    Example:
        >>> result = generate_reference_skeleton(1)
        >>> print(result.path)
        solutions/0001_two_sum.py
    """
    # Load config
    if config is None:
        config = load_config()
    
    if header_level is not None:
        config.header_level = header_level
    
    # Get problem metadata
    ds = LeetCodeDataSource()
    
    try:
        question = ds.get_by_frontend_id(problem_id)
    except Exception as e:
        return ReferenceGenerationResult(
            success=False,
            message=f"Failed to fetch problem {problem_id}: {e}",
        )
    
    # Determine output path
    slug = question.titleSlug.replace("-", "_")
    filename = f"{problem_id:04d}_{slug}.py"
    output_path = config.solutions_path / filename
    
    # Check if already exists
    if output_path.exists() and not dry_run:
        return ReferenceGenerationResult(
            success=False,
            path=output_path,
            message=f"Reference already exists: {output_path}\n"
                    f"Use `codegen practice {problem_id}` to start practicing.",
        )
    
    # Generate skeleton content
    content = _generate_skeleton_content(question, config, codec_mode_override=codec_mode_override)
    
    if dry_run:
        return ReferenceGenerationResult(
            success=True,
            path=output_path,
            message="Dry run - content generated but not written",
            content=content,
        )
    
    # Ensure directory exists
    config.solutions_path.mkdir(parents=True, exist_ok=True)
    
    # Write file
    output_path.write_text(content, encoding="utf-8")
    
    # Build success message
    stub_info = parse_code_stub(question.Code)
    helpers = detect_required_helpers(stub_info)
    helper_msg = f"   (detected helpers: {', '.join(sorted(helpers))})" if helpers else ""
    
    return ReferenceGenerationResult(
        success=True,
        path=output_path,
        message=f"✅ Created: {output_path}{helper_msg}",
        content=content,
    )


def _generate_skeleton_content(
    question: Question,
    config: CodeGenConfig,
    codec_mode_override: Optional[str] = None,
) -> str:
    """Generate the skeleton file content."""
    
    # 1. Parse code stub
    stub_info = parse_code_stub(question.Code)
    
    # 2. Render header
    header = render_solution_header(question, level=config.header_level)
    
    # 3. Detect required helpers
    required_helpers = detect_required_helpers(stub_info)
    helper_functions = detect_helper_functions(required_helpers)
    typing_imports = suggest_imports(stub_info)
    
    # 4. Generate imports
    imports = emit_all_imports(typing_imports, include_runner=True)
    
    # 5. Generate helper classes
    helper_mode = HelperEmitMode(config.helper_mode)
    helpers_code = emit_helpers(required_helpers, mode=helper_mode)
    
    # 6. Generate SOLUTIONS dict
    solutions_dict = assemble_solutions_dict(
        method_name=stub_info.method_name,
        class_name=stub_info.class_name,
    )
    
    # 7. Generate Solution class
    params_str = format_params_for_signature(stub_info.params)
    solution_class = assemble_solution_class(
        method_name=stub_info.method_name,
        params_str=params_str,
        return_type=stub_info.return_type,
        class_name=stub_info.class_name,
    )
    
    # 8. Generate solve() function (with potential tiered helpers)
    solve_result = _generate_solve_function(
        stub_info, config, problem_id=question.frontend_question_id, codec_mode_override=codec_mode_override
    )
    
    # 9. Determine helper code and imports
    if solve_result.helper_code:
        # Tiered inline mode: embed all codec functions (including classes)
        helpers_code = solve_result.helper_code
        helper_func_code = ""  # Tiered inline includes all needed functions
    elif solve_result.codec_import:
        # Tiered import mode: import everything from codec (classes + functions)
        imports = imports.rstrip() + "\n" + solve_result.codec_import
        helpers_code = ""  # Classes imported from codec, no local definition
        helper_func_code = ""  # Functions imported from codec
    else:
        # Standard mode: use detected helper functions
        helper_func_code = emit_helper_functions(helper_functions, mode=helper_mode)
    
    # 10. Assemble module
    return assemble_module(
        header=header,
        imports=imports,
        helpers=helpers_code,
        judge_func="",  # Reference doesn't have JUDGE_FUNC by default
        solutions_dict=solutions_dict,
        solution_classes=solution_class,
        helper_functions=helper_func_code,
        solve_fn=solve_result.solve_code,
    )


class TieredSolveResult:
    """Result from tiered solve generation."""
    def __init__(self, solve_code: str, helper_code: str = "", codec_import: str = "", tier: str = "0"):
        self.solve_code = solve_code
        self.helper_code = helper_code
        self.codec_import = codec_import
        self.tier = tier


def _generate_solve_function(
    stub_info,
    config: CodeGenConfig,
    problem_id: int = None,
    codec_mode_override: Optional[str] = None,
) -> TieredSolveResult:
    """
    Generate the solve() function based on config.
    
    Modes:
        - "placeholder": Old-style placeholder with TODOs
        - "infer": Use solve_generator to auto-generate based on IO schema
        - "tiered": Use tiered solve generator with problem config
    
    Auto-detection:
        - If problem_id is provided and problem has tier "1" or "1.5" in config,
          automatically use tiered mode regardless of solve_mode setting.
        - This ensures Tier-1/1.5 problems always get proper codec support.
    """
    method_name = stub_info.method_name
    
    # Auto-detect tiered mode: if problem has tier 1 or 1.5, use tiered generator
    if problem_id:
        try:
            tier = get_tier(str(problem_id).zfill(4))
            if tier in ("1", "1.5"):
                # Auto-use tiered mode for Tier-1/1.5 problems
                result = generate_tiered_solve(
                    stub_info,
                    str(problem_id).zfill(4),
                    codec_mode_override=codec_mode_override,
                )
                return TieredSolveResult(
                    solve_code=result.solve_code,
                    helper_code=result.helper_code,
                    codec_import=result.codec_import,
                    tier=result.tier,
                )
        except Exception:
            # If config lookup fails, fall through to manual mode selection
            pass
    
    # Check config for solve_mode
    solve_mode = getattr(config, 'solve_mode', 'placeholder')
    
    if solve_mode == "tiered" and problem_id:
        # Use tiered solve generator
        result = generate_tiered_solve(
            stub_info,
            str(problem_id).zfill(4),
            codec_mode_override=codec_mode_override,
        )
        return TieredSolveResult(
            solve_code=result.solve_code,
            helper_code=result.helper_code,
            codec_import=result.codec_import,
            tier=result.tier,
        )
    
    if solve_mode == "infer":
        # Use new solve_generator with IO schema inference
        io_schema = infer_io_schema(stub_info)
        result = generate_solve_function(stub_info, io_schema)
        return TieredSolveResult(solve_code=result.code)
    
    # Default: placeholder mode (backwards compatible)
    param_names = [name for name, _ in stub_info.params]
    
    if param_names:
        parse_comment = "# TODO: Parse input from lines"
        call_code = f"# result = solver.{method_name}({', '.join(param_names)})"
    else:
        parse_comment = "# No parameters to parse"
        call_code = f"# result = solver.{method_name}()"
    
    solve_code = assemble_solve_function(
        method_name=method_name,
        input_format="TODO: Define based on problem",
        example_input="TODO: Add example from problem description",
        parse_code=parse_comment,
        call_code=call_code,
        output_format="# print(result)",
    )
    return TieredSolveResult(solve_code=solve_code)


def get_reference_path(problem_id: int, config: Optional[CodeGenConfig] = None) -> Path:
    """
    Get the expected path for a reference solution.
    
    Args:
        problem_id: LeetCode frontend question ID
        config: CodeGen configuration
        
    Returns:
        Path to the reference solution file
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
    
    return config.solutions_path / filename


def reference_exists(problem_id: int, config: Optional[CodeGenConfig] = None) -> bool:
    """
    Check if a reference solution exists.
    
    Args:
        problem_id: LeetCode frontend question ID
        config: CodeGen configuration
        
    Returns:
        True if reference exists
    """
    path = get_reference_path(problem_id, config)
    return path.exists()

