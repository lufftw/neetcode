#!/usr/bin/env python3
"""
Next Problem Selector - Get next unsolved problem by acceptance rate + difficulty.

Usage:
    python tools/next_problem.py           # Show next 10 problems
    python tools/next_problem.py --count 5 # Show next 5 problems
    python tools/next_problem.py --json    # Output as JSON (for automation)
    python tools/next_problem.py --first   # Show only the first problem
    python tools/next_problem.py --exclude-neetcode  # Exclude NeetCode 150 problems

Sorting Logic:
    1. Lower acceptance rate first (harder)
    2. If same acceptance rate, harder difficulty first (Hard > Medium > Easy)
"""
import sqlite3
import os
import json
import argparse
from pathlib import Path


# NeetCode 150 Core Problems (to be excluded when using --exclude-neetcode)
NEETCODE_150 = {
    1, 2, 3, 4, 5, 11, 15, 17, 19, 20, 21, 22, 23, 33, 36, 39, 42, 46, 48, 49,
    53, 54, 55, 56, 62, 70, 73, 74, 76, 78, 79, 84, 91, 98, 100, 102, 104, 105,
    121, 124, 125, 127, 128, 130, 131, 133, 138, 139, 141, 143, 146, 152, 153,
    155, 167, 169, 190, 191, 198, 200, 206, 207, 208, 210, 211, 212, 213, 215,
    217, 226, 230, 235, 238, 239, 242, 252, 253, 261, 268, 269, 271, 287, 295,
    297, 300, 322, 323, 332, 338, 347, 355, 371, 417, 424, 435, 494, 518, 543,
    567, 572, 621, 647, 684, 695, 703, 704, 739, 743, 746, 763, 778, 787, 846,
    853, 875, 920, 973, 981, 994, 1046, 1143, 1584
}


def get_project_root() -> Path:
    """Find project root by looking for .neetcode directory."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".neetcode").exists():
            return current
        current = current.parent
    # Fallback
    return Path(__file__).resolve().parent.parent


def get_solved_problem_ids(solutions_dir: Path) -> set:
    """Get set of already solved problem IDs from solutions directory."""
    solved = set()
    if not solutions_dir.exists():
        return solved

    for f in solutions_dir.iterdir():
        if f.suffix == ".py" and f.name[0].isdigit():
            try:
                problem_id = int(f.name.split("_")[0])
                solved.add(problem_id)
            except ValueError:
                continue
    return solved


def get_next_problems(
    db_path: Path,
    solved_ids: set,
    count: int = 10,
    exclude_paid: bool = True
) -> list:
    """
    Get next unsolved problems sorted by acceptance rate and difficulty.

    Returns:
        List of dicts with: id, slug, title, difficulty, acceptance_rate
    """
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row

        # Build exclusion clause
        if solved_ids:
            placeholders = ",".join("?" * len(solved_ids))
            exclude_clause = f"AND frontend_question_id NOT IN ({placeholders})"
            params = list(solved_ids) + [count]
        else:
            exclude_clause = ""
            params = [count]

        paid_clause = "AND paid_only = 0" if exclude_paid else ""

        query = f"""
            SELECT
                frontend_question_id as id,
                title_slug as slug,
                title,
                difficulty,
                total_acs,
                total_submitted,
                CASE WHEN total_submitted > 0
                     THEN ROUND(100.0 * total_acs / total_submitted, 2)
                     ELSE 0
                END AS acceptance_rate
            FROM problem_index
            WHERE total_submitted > 0
              {paid_clause}
              {exclude_clause}
            ORDER BY
                acceptance_rate ASC,
                CASE difficulty
                    WHEN 'Hard' THEN 3
                    WHEN 'Medium' THEN 2
                    WHEN 'Easy' THEN 1
                    ELSE 0
                END DESC
            LIMIT ?
        """

        cursor = conn.execute(query, params)

        return [dict(row) for row in cursor.fetchall()]


def format_problem_id(problem_id: int) -> str:
    """Format problem ID as 4-digit zero-padded string."""
    return f"{problem_id:04d}"


def main():
    parser = argparse.ArgumentParser(
        description="Get next unsolved LeetCode problems by acceptance rate"
    )
    parser.add_argument(
        "--count", "-n",
        type=int,
        default=10,
        help="Number of problems to show (default: 10)"
    )
    parser.add_argument(
        "--first", "-1",
        action="store_true",
        help="Show only the first problem"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--include-paid",
        action="store_true",
        help="Include paid/premium problems"
    )
    parser.add_argument(
        "--exclude-neetcode",
        action="store_true",
        help="Exclude NeetCode 150 problems (use when focusing on other problems)"
    )
    parser.add_argument(
        "--exclude",
        type=str,
        help="Comma-separated list of problem IDs to exclude (e.g., '1,2,3,42')"
    )

    args = parser.parse_args()

    # Find paths
    project_root = get_project_root()
    db_path = project_root / ".neetcode" / "leetcode_datasource" / "store" / "leetcode.sqlite3"
    solutions_dir = project_root / "solutions"

    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        print("Run 'python -m leetcode_datasource sync' to initialize.")
        return 1

    # Get solved problems
    solved_ids = get_solved_problem_ids(solutions_dir)

    # Add NeetCode 150 to exclusion if requested
    if args.exclude_neetcode:
        solved_ids = solved_ids | NEETCODE_150
        print(f"[*] Excluding NeetCode 150 ({len(NEETCODE_150)} problems)")

    # Add custom exclusions
    if args.exclude:
        custom_exclude = {int(x.strip()) for x in args.exclude.split(",") if x.strip().isdigit()}
        solved_ids = solved_ids | custom_exclude
        print(f"[*] Excluding {len(custom_exclude)} custom problem IDs")

    # Get next problems
    count = 1 if args.first else args.count
    problems = get_next_problems(
        db_path,
        solved_ids,
        count=count,
        exclude_paid=not args.include_paid
    )

    if not problems:
        print("All problems solved! :)")
        return 0

    # Output
    if args.json:
        print(json.dumps(problems, indent=2))
    else:
        print(f"\n[Stats] Stats: {len(solved_ids)} solved, showing next {len(problems)}")
        print(f"[*] Sorting: Acceptance Rate (low first), Difficulty (high first)\n")
        print(f"{'#':>3} | {'ID':>5} | {'Acc':>8} | {'Diff':>6} | Title")
        print("-" * 80)

        for i, p in enumerate(problems, 1):
            formatted_id = format_problem_id(p["id"])
            print(f"{i:>3} | {formatted_id} | {p['acceptance_rate']:>7.2f}% | {p['difficulty']:>6} | {p['title'][:45]}")

        if args.first or count == 1:
            p = problems[0]
            print()
            print("=" * 80)
            print(f">> Next Problem: {format_problem_id(p['id'])} - {p['title']}")
            print(f"  Difficulty: {p['difficulty']}, Acceptance: {p['acceptance_rate']}%")
            print(f"  Command: python -m codegen new {p['id']} --with-tests")
            print("=" * 80)

    return 0


if __name__ == "__main__":
    exit(main())
