#!/bin/bash
# Run unit tests for neetcode runner system
#
# This script runs all characterization tests to ensure
# that refactoring doesn't break existing behavior.

echo "========================================"
echo "Running Unit Tests"
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

# Check if pytest is installed
if ! "$PYTHON_EXE" -m pytest --version &> /dev/null; then
    echo "[ERROR] pytest is not installed in virtual environment"
    echo "Please install pytest first:"
    echo "  source leetcode/bin/activate"
    echo "  pip install pytest pytest-cov"
    echo ""
    exit 1
fi

# Change to project root directory to run tests
cd "$PROJECT_ROOT"

# Run tests with verbose output
echo "Running all tests..."
echo "Using Python: $PYTHON_EXE"
echo ""
"$PYTHON_EXE" -m pytest .dev/tests -v --tb=short

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "All tests passed!"
    echo "========================================"
else
    echo ""
    echo "========================================"
    echo "Some tests failed!"
    echo "========================================"
    exit 1
fi

