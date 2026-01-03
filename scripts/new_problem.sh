#!/bin/bash
# ============================================
#  Create New Problem (pass-through wrapper)
#  All logic lives in packages/codegen
#  
#  Usage:
#    ./new_problem.sh 1                      Generate solution skeleton
#    ./new_problem.sh 1 --with-tests         Also generate test files
#    ./new_problem.sh 1 --solve-mode infer   Auto-generate solve()
#    ./new_problem.sh 1 --solve-mode tiered  Use tiered codec generation
#    ./new_problem.sh 1 --codec-mode import  Use import mode (default)
#    ./new_problem.sh 1 --codec-mode inline  Embed codec inline
#    ./new_problem.sh 1 --dry-run            Preview without writing
#  
#  Tiered Problem Generation:
#    Tier-1/1.5 problems auto-detect and use tiered mode.
#    No need to specify --solve-mode for ListNode/TreeNode problems.
#  
#  Examples:
#    ./new_problem.sh 15                     3Sum (Tier-0)
#    ./new_problem.sh 104                    Max Depth of Binary Tree (Tier-1, auto-tiered)
#    ./new_problem.sh 142                    Linked List Cycle II (Tier-1.5, auto-tiered)
#    ./new_problem.sh 15 --with-tests        3Sum with example tests
# ============================================

python -m packages.codegen new "$@"
