#!/bin/bash
# ============================================
#  Create Practice File (pass-through wrapper)
#  All logic lives in src/codegen
#  
#  Usage:
#    ./new_practice.sh 23                    Generate practice skeleton
#    ./new_practice.sh 23 --all-solutions    Include all solution variants
#    ./new_practice.sh 23 --dry-run          Preview without writing
#  
#  Features:
#    - Generates LeetCode-style class Solution
#    - Keeps __init__ + public methods (for Design problems)
#    - Removes private helper methods (_method)
#    - Reuses infrastructure from reference solution
#  
#  Examples:
#    ./new_practice.sh 1                     Two Sum (algorithm)
#    ./new_practice.sh 146                   LRU Cache (design)
#    ./new_practice.sh 23                    Merge k Sorted Lists
# ============================================

python -m codegen practice "$@"

