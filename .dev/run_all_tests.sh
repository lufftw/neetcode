#!/bin/bash
# ============================================================================
# Run ALL tests for the neetcode project
# ============================================================================
#
# This script runs three categories of tests:
#
# 1. Component Tests (.dev/tests/)
#    - Runner module unit tests
#    - Integration tests
#    - Edge case tests
#
# 2. Solution Correctness Tests (.dev/tests_solutions/)
#    - Static test cases (from tests/ directory)
#    - Generated test cases (if available)
#
# 3. Solution Format Tests (tools/tests/)
#    - Pure Polymorphic Architecture compliance
#    - Solution comment format
#    - Complexity comments
#
# Exit Codes:
#   0 - All tests passed
#   1 - One or more test categories failed
#
# ============================================================================

echo "================================================================================"
echo "                        NEETCODE PROJECT - FULL TEST SUITE"
echo "================================================================================"
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

# Change to project root directory
cd "$PROJECT_ROOT"

TOTAL_FAILED=0

# ============================================================================
# 1. Solution Format Tests
# ============================================================================
echo ""
echo "================================================================================"
echo "[1/3] SOLUTION FORMAT TESTS"
echo "================================================================================"
echo ""
echo "Checking Pure Polymorphic Architecture compliance..."
echo ""

"$PYTHON_EXE" tools/check_solutions.py
if [ $? -ne 0 ]; then
    echo ""
    echo "[WARN] Format checker found issues"
fi

echo ""
"$PYTHON_EXE" -m pytest tools/tests/test_solution_format.py -v --tb=short
if [ $? -ne 0 ]; then
    echo ""
    echo "[FAIL] Solution format tests failed!"
    ((TOTAL_FAILED++))
else
    echo ""
    echo "[PASS] Solution format tests passed"
fi

# ============================================================================
# 2. Component Tests (Runner modules)
# ============================================================================
echo ""
echo "================================================================================"
echo "[2/3] COMPONENT TESTS (Runner Modules)"
echo "================================================================================"
echo ""
echo "Testing runner module functionality..."
echo ""

"$PYTHON_EXE" -m pytest .dev/tests -v --tb=short
if [ $? -ne 0 ]; then
    echo ""
    echo "[FAIL] Component tests failed!"
    ((TOTAL_FAILED++))
else
    echo ""
    echo "[PASS] Component tests passed"
fi

# ============================================================================
# 3. Solution Correctness Tests
# ============================================================================
echo ""
echo "================================================================================"
echo "[3/3] SOLUTION CORRECTNESS TESTS"
echo "================================================================================"
echo ""
echo "Testing all solutions with test cases..."
echo ""

"$PYTHON_EXE" -m pytest .dev/tests_solutions -v --tb=short
if [ $? -ne 0 ]; then
    echo ""
    echo "[FAIL] Solution correctness tests failed!"
    ((TOTAL_FAILED++))
else
    echo ""
    echo "[PASS] Solution correctness tests passed"
fi

# ============================================================================
# Summary
# ============================================================================
echo ""
echo "================================================================================"
echo "                                TEST SUMMARY"
echo "================================================================================"
echo ""

if [ $TOTAL_FAILED -eq 0 ]; then
    echo "  [OK] All test categories passed!"
    echo ""
    echo "  - Solution Format Tests:      PASSED"
    echo "  - Component Tests:            PASSED"
    echo "  - Solution Correctness Tests: PASSED"
    echo ""
    echo "================================================================================"
    exit 0
else
    echo "  [FAILED] $TOTAL_FAILED test category(ies) failed!"
    echo ""
    echo "  Please review the output above for details."
    echo ""
    echo "================================================================================"
    exit 1
fi

