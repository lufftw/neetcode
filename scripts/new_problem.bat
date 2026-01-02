@echo off
setlocal EnableExtensions

REM ============================================
REM  Create New Problem (pass-through wrapper)
REM  All logic lives in packages/codegen
REM  
REM  Usage:
REM    new_problem.bat 1                     Generate solution skeleton
REM    new_problem.bat 1 --with-tests        Also generate test files
REM    new_problem.bat 1 --solve-mode infer  Auto-generate solve() 
REM    new_problem.bat 1 --dry-run           Preview without writing
REM  
REM  Examples:
REM    new_problem.bat 15                    3Sum
REM    new_problem.bat 15 --with-tests       3Sum with example tests
REM    new_problem.bat 0015                  Same (auto-padded)
REM ============================================

python -m packages.codegen new %*
exit /b %ERRORLEVEL%
