"""
CodeGen CLI - Command line interface for code generation.

Commands:
    codegen new <problem_id>       Generate reference skeleton
    codegen practice <problem_id>  Generate practice skeleton
"""

import argparse
import sys
import io
from typing import Optional, List

from .core.config import load_config, HeaderLevel
from .reference.generator import generate_reference_skeleton
from .practice.generator import generate_practice_skeleton


# Ensure stdout uses UTF-8 encoding on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="codegen",
        description="CodeGen - LeetCode solution skeleton generator",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # codegen new
    new_parser = subparsers.add_parser(
        "new",
        help="Generate reference skeleton to solutions/",
    )
    new_parser.add_argument(
        "problem_id",
        type=int,
        help="LeetCode problem number (e.g., 1 for Two Sum)",
    )
    new_parser.add_argument(
        "--header-level",
        choices=["minimal", "standard", "full"],
        help="Header detail level (default: full)",
    )
    new_parser.add_argument(
        "--solve-mode",
        choices=["placeholder", "infer"],
        help="solve() generation mode (default: placeholder)",
    )
    new_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print content, don't write file",
    )
    
    # codegen practice
    practice_parser = subparsers.add_parser(
        "practice",
        help="Generate practice skeleton to practices/",
    )
    practice_parser.add_argument(
        "problem_id",
        type=int,
        help="LeetCode problem number",
    )
    practice_parser.add_argument(
        "--all-solutions",
        action="store_true",
        help="Include all Solution classes from reference",
    )
    practice_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print content, don't write file",
    )
    
    return parser


def cmd_new(args: argparse.Namespace) -> int:
    """Handle 'codegen new' command."""
    # Build CLI overrides
    cli_overrides = {}
    if args.header_level:
        cli_overrides["header_level"] = args.header_level
    if args.solve_mode:
        cli_overrides["solve_mode"] = args.solve_mode
    
    config = load_config(cli_overrides=cli_overrides if cli_overrides else None)
    
    result = generate_reference_skeleton(
        problem_id=args.problem_id,
        config=config,
        dry_run=args.dry_run,
        header_level=args.header_level,
    )
    
    if args.dry_run and result.content:
        print("=" * 60)
        print("DRY RUN - Generated content:")
        print("=" * 60)
        print(result.content)
        print("=" * 60)
    
    print(result.message)
    
    return 0 if result.success else 1


def cmd_practice(args: argparse.Namespace) -> int:
    """Handle 'codegen practice' command."""
    config = load_config()
    
    result = generate_practice_skeleton(
        problem_id=args.problem_id,
        config=config,
        dry_run=args.dry_run,
        all_solutions=args.all_solutions,
    )
    
    if args.dry_run and result.content:
        print("=" * 60)
        print("DRY RUN - Generated content:")
        print("=" * 60)
        print(result.content)
        print("=" * 60)
    
    print(result.message)
    
    return 0 if result.success else 1


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if args.command is None:
        parser.print_help()
        return 1
    
    if args.command == "new":
        return cmd_new(args)
    elif args.command == "practice":
        return cmd_practice(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

