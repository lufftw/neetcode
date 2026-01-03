@echo off
setlocal EnableExtensions

REM ============================================
REM  Create New Problem (pass-through wrapper)
REM  All logic lives in packages/codegen
REM  
REM  Usage:
REM    new_problem.bat 1                      Generate solution skeleton
REM    new_problem.bat 1 --with-tests         Also generate test files
REM    new_problem.bat 1 --solve-mode infer   Auto-generate solve()
REM    new_problem.bat 1 --solve-mode tiered  Use tiered codec generation
REM    new_problem.bat 1 --codec-mode import  Use import mode (default)
REM    new_problem.bat 1 --codec-mode inline  Embed codec inline
REM    new_problem.bat 1 --dry-run            Preview without writing
REM  
REM  Tiered Problem Generation:
REM    Tier-1/1.5 problems auto-detect and use tiered mode.
REM    No need to specify --solve-mode for ListNode/TreeNode problems.
REM  
REM  Examples:
REM    new_problem.bat 15                     3Sum (Tier-0)
REM    new_problem.bat 104                    Max Depth of Binary Tree (Tier-1, auto-tiered)
REM    new_problem.bat 142                    Linked List Cycle II (Tier-1.5, auto-tiered)
REM    new_problem.bat 15 --with-tests        3Sum with example tests
REM ============================================

python -m packages.codegen new %*
exit /b %ERRORLEVEL%
