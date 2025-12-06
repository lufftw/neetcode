@echo off
chcp 65001 >nul
REM ============================================
REM  Create New Problem
REM  Usage: 
REM    new_problem.bat 0001_two_sum           (single solution)
REM    new_problem.bat 0001_two_sum --multi   (multi-solution template)
REM ============================================

if "%~1"=="" (
    echo Usage: new_problem.bat ^<problem_name^> [--multi]
    echo.
    echo Examples:
    echo   new_problem.bat 0001_two_sum           ^(single solution^)
    echo   new_problem.bat 0023_merge_k_lists --multi  ^(multi-solution template^)
    exit /b 1
)

set PROBLEM=%~1
set BASE_DIR=%~dp0
set TEMPLATE=template_solution.py

REM Check if using multi-solution template
if "%~2"=="--multi" (
    set TEMPLATE=template_solution_multi.py
    echo Using multi-solution template
) else (
    echo Using single-solution template
)

REM Create solution file
if not exist "%BASE_DIR%solutions\%PROBLEM%.py" (
    copy "%BASE_DIR%templates\%TEMPLATE%" "%BASE_DIR%solutions\%PROBLEM%.py" >nul
    echo Created: solutions\%PROBLEM%.py
) else (
    echo Already exists: solutions\%PROBLEM%.py
)

REM Create first test case
if not exist "%BASE_DIR%tests\%PROBLEM%_1.in" (
    echo. > "%BASE_DIR%tests\%PROBLEM%_1.in"
    echo Created: tests\%PROBLEM%_1.in
) else (
    echo Already exists: tests\%PROBLEM%_1.in
)

if not exist "%BASE_DIR%tests\%PROBLEM%_1.out" (
    echo. > "%BASE_DIR%tests\%PROBLEM%_1.out"
    echo Created: tests\%PROBLEM%_1.out
) else (
    echo Already exists: tests\%PROBLEM%_1.out
)

echo.
echo Done! Now edit:
echo    - solutions\%PROBLEM%.py
echo    - tests\%PROBLEM%_1.in
echo    - tests\%PROBLEM%_1.out

if "%~2"=="--multi" (
    echo.
    echo Multi-solution tips:
    echo    - Define methods in SOLUTIONS dict
    echo    - Test all: python runner/test_runner.py %PROBLEM% --all
    echo    - Benchmark: python runner/test_runner.py %PROBLEM% --all --benchmark
)
