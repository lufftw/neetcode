#!/bin/bash
# Standalone script to run solution format tests on Linux/Mac
# Usage: ./run_format_tests.sh [--verbose|--quiet]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Use virtual environment Python if available, otherwise system Python
if [ -f "$PROJECT_ROOT/leetcode/bin/python" ]; then
    "$PROJECT_ROOT/leetcode/bin/python" "$SCRIPT_DIR/run_format_tests.py" "$@"
else
    python3 "$SCRIPT_DIR/run_format_tests.py" "$@"
fi

exit $?

