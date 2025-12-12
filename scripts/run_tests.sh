#!/bin/bash
# ============================================
#  Run All Tests
#  Usage: ./run_tests.sh 0001_two_sum
# ============================================

if [ -z "$1" ]; then
    echo "Usage: ./run_tests.sh <problem_name> [options]"
    echo "Example: ./run_tests.sh 0001_two_sum"
    echo "         ./run_tests.sh 0001_two_sum --all"
    echo "         ./run_tests.sh 0001_two_sum --all --benchmark"
    exit 1
fi

# Get the directory where the script is located (parent directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Use virtual environment Python
"${SCRIPT_DIR}/leetcode/bin/python" "${SCRIPT_DIR}/runner/test_runner.py" "$@"

