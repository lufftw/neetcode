@echo off
chcp 65001 >nul
REM ============================================
REM  Create New Problem
REM  Usage: 
REM    new_problem.bat 0001_two_sum             (single solution)
REM    new_problem.bat 0001_two_sum --multi     (multiple solutions, polymorphic)
REM ============================================

if "%~1"=="" (
    echo Usage: new_problem.bat ^<problem_name^> [--multi]
    echo.
    echo Templates:
    echo   ^(none^)      Single solution template
    echo   --multi     Multiple solutions ^(polymorphic pattern^)
    echo.
    echo Examples:
    echo   new_problem.bat 0001_two_sum
    echo   new_problem.bat 0023_merge_k_lists --multi
    exit /b 1
)

set PROBLEM=%~1
set BASE_DIR=%~dp0
set TEMPLATE=template_solution.py
set TEMPLATE_TYPE=single

REM Check which template to use
if "%~2"=="--multi" (
    set TEMPLATE=template_solution_multi.py
    set TEMPLATE_TYPE=multi
    echo Using multi-solution template ^(polymorphic pattern^)
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

if "%TEMPLATE_TYPE%"=="multi" (
    echo.
    echo Multi-solution tips ^(Polymorphic Pattern^):
    echo    - Create separate classes ^(SolutionOptimal, SolutionBruteforce, etc.^)
    echo    - Each class implements the SAME method name ^(polymorphism^)
    echo    - Register each class in SOLUTIONS dict with 'class' and 'method' fields
    echo    - Test all: python runner/test_runner.py %PROBLEM% --all
    echo    - Benchmark: python runner/test_runner.py %PROBLEM% --all --benchmark
)
