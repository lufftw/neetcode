@echo off
setlocal EnableExtensions

REM ============================================
REM  Create Practice File (pass-through wrapper)
REM  All logic lives in src/codegen
REM  
REM  Usage:
REM    new_practice.bat 23                    Generate practice skeleton
REM    new_practice.bat 23 --all-solutions    Include all solution variants
REM    new_practice.bat 23 --dry-run          Preview without writing
REM  
REM  Features:
REM    - Generates LeetCode-style class Solution
REM    - Keeps __init__ + public methods (for Design problems)
REM    - Removes private helper methods (_method)
REM    - Reuses infrastructure from reference solution
REM  
REM  Examples:
REM    new_practice.bat 1                     Two Sum (algorithm)
REM    new_practice.bat 146                   LRU Cache (design)
REM    new_practice.bat 23                    Merge k Sorted Lists
REM ============================================

python -m codegen practice %*
exit /b %ERRORLEVEL%

