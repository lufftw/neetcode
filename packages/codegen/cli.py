"""
CodeGen CLI - Command line interface for code generation.

Commands:
    codegen new <problem_id>       Generate reference skeleton
    codegen practice <problem_id>  Generate practice skeleton
    codegen check [problem_id]     Check test consistency
"""

import argparse
import sys
import io
from typing import Optional, List

from .core.config import load_config, HeaderLevel
from .reference.generator import generate_reference_skeleton
from .practice.generator import generate_practice_skeleton
from .checker import TestChecker, generate_report, CheckStatus


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
    
    # codegen check
    check_parser = subparsers.add_parser(
        "check",
        help="Check test file consistency with LeetCode examples",
    )
    check_parser.add_argument(
        "problem_id",
        nargs="?",
        default=None,
        help="Problem ID to check (e.g., 1, 0001, 0001_two_sum). If omitted, use --all",
    )
    check_parser.add_argument(
        "--all",
        action="store_true",
        dest="check_all",
        help="Check all problems in solutions/",
    )
    check_parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of problems to check (with --all)",
    )
    check_parser.add_argument(
        "--generatable",
        action="store_true",
        help="Only check if examples can be parsed (skip consistency check)",
    )
    check_parser.add_argument(
        "--report",
        choices=["text", "markdown", "json"],
        default="text",
        help="Output format for report (default: text)",
    )
    check_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed information for each example",
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


def cmd_check(args: argparse.Namespace) -> int:
    """Handle 'codegen check' command."""
    checker = TestChecker()
    
    if args.check_all:
        # Check all problems
        results = checker.check_all(limit=args.limit)
        
        if args.report == "json":
            print(generate_report(results, format="json"))
        else:
            # Print summary first
            total = len(results)
            ok = sum(1 for r in results if r.status in (CheckStatus.OK, CheckStatus.MATCH))
            mismatch = sum(1 for r in results if r.status == CheckStatus.MISMATCH)
            missing = sum(1 for r in results if r.status == CheckStatus.MISSING_TESTS)
            errors = sum(1 for r in results if r.status in (CheckStatus.PARSE_ERROR, CheckStatus.FETCH_ERROR))
            
            print(f"Test Consistency Check")
            print(f"=" * 50)
            print(f"Total: {total} problems")
            print(f"  Match:   {ok}")
            print(f"  Mismatch: {mismatch}")
            print(f"  Missing:  {missing}")
            print(f"  Errors:   {errors}")
            print()
            
            # Print details
            for r in results:
                if args.verbose or r.status not in (CheckStatus.OK, CheckStatus.MATCH):
                    print(r.summary())
                    if args.verbose:
                        for ex in r.examples:
                            status_str = ex.status.value
                            print(f"    Example {ex.example_num}: {status_str}")
                            if ex.diff_details:
                                for line in ex.diff_details.split("\n")[:4]:
                                    print(f"      {line}")
        
        # Return 0 if all OK, 1 if any issues
        has_issues = any(r.status not in (CheckStatus.OK, CheckStatus.MATCH) for r in results)
        return 1 if has_issues else 0
    
    elif args.problem_id:
        # Check single problem
        if args.generatable:
            result = checker.check_generatable(args.problem_id)
        else:
            result = checker.check_problem(args.problem_id)
        
        if args.report == "json":
            print(generate_report([result], format="json"))
        else:
            print(result.summary())
            print(f"  Generatable: {result.generatable}")
            print(f"  Consistent:  {result.consistent}")
            
            if args.verbose or result.status not in (CheckStatus.OK, CheckStatus.MATCH):
                for ex in result.examples:
                    print(f"  Example {ex.example_num}: {ex.status.value}")
                    if args.verbose:
                        print(f"    Expected IN:  {ex.expected_in[:60]}{'...' if len(ex.expected_in) > 60 else ''}")
                        print(f"    Actual IN:    {ex.actual_in[:60]}{'...' if len(ex.actual_in) > 60 else ''}")
                        print(f"    Expected OUT: {ex.expected_out[:60]}{'...' if len(ex.expected_out) > 60 else ''}")
                        print(f"    Actual OUT:   {ex.actual_out[:60]}{'...' if len(ex.actual_out) > 60 else ''}")
            
            if result.warnings:
                print("  Warnings:")
                for w in result.warnings:
                    print(f"    - {w}")
        
        return 0 if result.status in (CheckStatus.OK, CheckStatus.MATCH) else 1
    
    else:
        print("Error: Please specify a problem_id or use --all")
        return 1


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
    elif args.command == "check":
        return cmd_check(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

