#!/bin/bash
# ============================================
#  Run Single Test Case
#  Usage: ./run_case.sh 0001_two_sum 1
# ============================================

if [ -z "$1" ]; then
    echo "Usage: ./run_case.sh <problem_name> <case_index>"
    echo "Example: ./run_case.sh 0001_two_sum 1"
    exit 1
fi

if [ -z "$2" ]; then
    echo "Usage: ./run_case.sh <problem_name> <case_index>"
    echo "Example: ./run_case.sh 0001_two_sum 1"
    exit 1
fi

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use virtual environment Python
"${SCRIPT_DIR}/leetcode/bin/python" "${SCRIPT_DIR}/runner/case_runner.py" "$1" "$2"

