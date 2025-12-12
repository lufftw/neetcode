#!/bin/bash
# ============================================
#  Create New Problem
#  Usage: 
#    ./new_problem.sh 0001_two_sum             (single solution)
#    ./new_problem.sh 0001_two_sum --multi     (multiple solutions, polymorphic)
# ============================================

if [ -z "$1" ]; then
    echo "Usage: ./new_problem.sh <problem_name> [--multi]"
    echo ""
    echo "Templates:"
    echo "  (none)      Single solution template"
    echo "  --multi     Multiple solutions (polymorphic pattern)"
    echo ""
    echo "Examples:"
    echo "  ./new_problem.sh 0001_two_sum"
    echo "  ./new_problem.sh 0023_merge_k_lists --multi"
    exit 1
fi

PROBLEM="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE="template_solution.py"
TEMPLATE_TYPE="single"

# Check which template to use
if [ "$2" == "--multi" ]; then
    TEMPLATE="template_solution_multi.py"
    TEMPLATE_TYPE="multi"
    echo "Using multi-solution template (polymorphic pattern)"
else
    echo "Using single-solution template"
fi

# Create solution file
if [ ! -f "${SCRIPT_DIR}/solutions/${PROBLEM}.py" ]; then
    cp "${SCRIPT_DIR}/templates/${TEMPLATE}" "${SCRIPT_DIR}/solutions/${PROBLEM}.py"
    echo "Created: solutions/${PROBLEM}.py"
else
    echo "Already exists: solutions/${PROBLEM}.py"
fi

# Create first test case (with proper LF line ending)
if [ ! -f "${SCRIPT_DIR}/tests/${PROBLEM}_1.in" ]; then
    printf "\n" > "${SCRIPT_DIR}/tests/${PROBLEM}_1.in"
    echo "Created: tests/${PROBLEM}_1.in"
else
    echo "Already exists: tests/${PROBLEM}_1.in"
fi

if [ ! -f "${SCRIPT_DIR}/tests/${PROBLEM}_1.out" ]; then
    printf "\n" > "${SCRIPT_DIR}/tests/${PROBLEM}_1.out"
    echo "Created: tests/${PROBLEM}_1.out"
else
    echo "Already exists: tests/${PROBLEM}_1.out"
fi

echo ""
echo "Done! Now edit:"
echo "   - solutions/${PROBLEM}.py"
echo "   - tests/${PROBLEM}_1.in"
echo "   - tests/${PROBLEM}_1.out"

if [ "$TEMPLATE_TYPE" == "multi" ]; then
    echo ""
    echo "Multi-solution tips (Polymorphic Pattern):"
    echo "   - Create separate classes (SolutionOptimal, SolutionBruteforce, etc.)"
    echo "   - Each class implements the SAME method name (polymorphism)"
    echo "   - Register each class in SOLUTIONS dict with 'class' and 'method' fields"
    echo "   - Test all: python runner/test_runner.py ${PROBLEM} --all"
    echo "   - Benchmark: python runner/test_runner.py ${PROBLEM} --all --benchmark"
fi
