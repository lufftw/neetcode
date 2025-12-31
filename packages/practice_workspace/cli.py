"""
Practice Workspace CLI - Command line interface for practice history management.

Commands:
    practice history <problem_id>   List history versions
    practice restore <problem_id>   Restore a history version
"""

import argparse
import sys
import io
from typing import Optional, List

from .history import list_history, get_history_entries
from .restore import restore_from_history, interactive_restore


# Ensure stdout uses UTF-8 encoding on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="practice",
        description="Practice Workspace - Practice file history management",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # practice history
    history_parser = subparsers.add_parser(
        "history",
        help="List history versions for a problem",
    )
    history_parser.add_argument(
        "problem_id",
        type=int,
        help="LeetCode problem number",
    )
    
    # practice restore
    restore_parser = subparsers.add_parser(
        "restore",
        help="Restore a history version",
    )
    restore_parser.add_argument(
        "problem_id",
        type=int,
        help="LeetCode problem number",
    )
    restore_parser.add_argument(
        "--latest",
        action="store_true",
        help="Restore the latest version without prompting",
    )
    restore_parser.add_argument(
        "--at",
        metavar="TIMESTAMP",
        help="Restore specific timestamp (YYYYMMDD_HHMMSS)",
    )
    
    return parser


def cmd_history(args: argparse.Namespace) -> int:
    """Handle 'practice history' command."""
    output = list_history(args.problem_id)
    print(output)
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    """Handle 'practice restore' command."""
    if args.at:
        result = restore_from_history(args.problem_id, timestamp=args.at)
    elif args.latest:
        result = restore_from_history(args.problem_id)
    else:
        # Interactive mode
        result = interactive_restore(args.problem_id)
    
    print(result.message)
    return 0 if result.success else 1


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if args.command is None:
        parser.print_help()
        return 1
    
    if args.command == "history":
        return cmd_history(args)
    elif args.command == "restore":
        return cmd_restore(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

