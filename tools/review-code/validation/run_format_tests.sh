#!/bin/bash
# Run solution format compliance tests
#
# This script tests solution file format compliance with
# Pure Polymorphic Architecture standards.
#
# Tests include:
#   - Solution comment format (Solution 1:)
#   - Time/Space complexity comments
#   - SOLUTIONS dictionary structure
#   - No wrapper functions
#   - Uses get_solver()

echo "========================================"
echo "Running Solution Format Tests"
echo "========================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/.."

# Use virtual environment Python
PYTHON_EXE="$PROJECT_ROOT/leetcode/bin/python"

# Check if virtual environment exists
if [ ! -f "$PYTHON_EXE" ]; then
    echo "[ERROR] Virtual environment not found: $PYTHON_EXE"
    echo "Please create virtual environment first:"
    echo "  python -m venv leetcode"
    echo "  source leetcode/bin/activate"
    echo "  pip install -r requirements.txt"
    echo ""
    exit 1
fi

# Change to project root directory
cd "$PROJECT_ROOT"

# Run format checker first (quick check)
echo "[1/2] Running format checker..."
"$PYTHON_EXE" tools/check_solutions.py
CHECKER_RESULT=$?

if [ $CHECKER_RESULT -ne 0 ]; then
    echo ""
    echo "Format checker found issues!"
    echo ""
fi

echo ""
echo "[2/2] Running format unit tests..."
"$PYTHON_EXE" -m pytest tools/review-code/validation/tests/test_solution_format.py -v --tb=short

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "All format tests passed!"
    echo "========================================"
else
    echo ""
    echo "========================================"
    echo "Some format tests failed!"
    echo "========================================"
    exit 1
fi
