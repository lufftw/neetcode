"""
CodeGen CLI - Command line interface for code generation.

Commands:
    codegen new <problem_id>       Generate reference skeleton
    codegen practice <problem_id>  Generate practice skeleton
    codegen check [problem_id]     Check test consistency
    codegen migrate [problem_id]   Migrate tests to canonical format
"""

import argparse
import sys
import io
from typing import Optional, List

from .core.config import load_config, HeaderLevel
from .reference.generator import generate_reference_skeleton
from .practice.generator import generate_practice_skeleton
from .checker import TestChecker, generate_report, CheckStatus
from .migrator import migrate_problem, migrate_all, generate_report as migrate_generate_report
from .core.test_generator import generate_tests_from_datasource


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
        choices=["placeholder", "infer", "tiered"],
        help="solve() generation mode: placeholder (TODO), infer (auto), tiered (config-based)",
    )
    new_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print content, don't write file",
    )
    new_parser.add_argument(
        "--with-tests",
        action="store_true",
        help="Also generate test files from LeetCode examples",
    )
    new_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing test files (with --with-tests)",
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
    
    # codegen migrate
    migrate_parser = subparsers.add_parser(
        "migrate",
        help="Migrate test files to canonical JSON literal format",
    )
    migrate_parser.add_argument(
        "problem_id",
        nargs="?",
        default=None,
        help="Problem ID to migrate (e.g., 0001_two_sum). If omitted, use --all",
    )
    migrate_parser.add_argument(
        "--all",
        action="store_true",
        dest="migrate_all",
        help="Migrate all problems",
    )
    migrate_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files",
    )
    migrate_parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't create backup files",
    )
    migrate_parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of problems (with --all)",
    )
    migrate_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output",
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
    
    # Generate test files if requested
    if args.with_tests:
        force = getattr(args, 'force', False)
        test_result = generate_tests_from_datasource(
            problem_id=args.problem_id,
            force=force,
            dry_run=args.dry_run,
        )
        
        if test_result.success:
            print(f"📝 Generated {test_result.test_count} test file(s)")
            if args.dry_run:
                for test in test_result.tests:
                    print(f"  Would create: {test.input_path.name}, {test.output_path.name}")
        else:
            print(f"⚠️ Test generation: {len(test_result.warnings)} warnings, {len(test_result.errors)} errors")
            for w in test_result.warnings[:3]:
                print(f"    {w}")
    
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


def cmd_migrate(args: argparse.Namespace) -> int:
    """Handle 'codegen migrate' command."""
    backup = not args.no_backup
    
    if args.dry_run:
        print("DRY RUN - No files will be modified\n")
    
    if args.migrate_all:
        results = migrate_all(
            dry_run=args.dry_run,
            backup=backup,
            limit=args.limit,
        )
        print()
        print(migrate_generate_report(results))
        
        # Return 0 if no errors
        has_errors = any(r.error_count > 0 for r in results)
        return 1 if has_errors else 0
    
    elif args.problem_id:
        result = migrate_problem(
            args.problem_id,
            dry_run=args.dry_run,
            backup=backup,
        )
        print(result.summary())
        
        if args.verbose:
            for fr in result.results:
                status = "MIGRATED" if fr.migrated else ("ERROR" if fr.error else "SKIP")
                print(f"  {fr.file_path.name}: {status} ({fr.original_format.value})")
                if fr.migrated and args.verbose:
                    orig_preview = fr.original_content[:50].replace('\n', '\\n')
                    new_preview = fr.new_content[:50].replace('\n', '\\n')
                    print(f"    Before: {orig_preview}...")
                    print(f"    After:  {new_preview}...")
        
        return 0 if result.error_count == 0 else 1
    
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
    elif args.command == "migrate":
        return cmd_migrate(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

