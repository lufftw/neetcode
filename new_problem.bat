@echo off
chcp 65001 >nul
REM ============================================
REM  建立新題目 (Create New Problem)
REM  用法: 
REM    new_problem.bat 0001_two_sum           (單一解法)
REM    new_problem.bat 0001_two_sum --multi   (多解法模板)
REM ============================================

if "%~1"=="" (
    echo 用法: new_problem.bat ^<problem_name^> [--multi]
    echo.
    echo Examples:
    echo   new_problem.bat 0001_two_sum           ^(單一解法^)
    echo   new_problem.bat 0023_merge_k_lists --multi  ^(多解法模板^)
    exit /b 1
)

set PROBLEM=%~1
set BASE_DIR=%~dp0
set TEMPLATE=template_solution.py

REM 檢查是否使用多解法模板
if "%~2"=="--multi" (
    set TEMPLATE=template_solution_multi.py
    echo 📦 Using multi-solution template
) else (
    echo 📦 Using single-solution template
)

REM 建立 solution 檔案
if not exist "%BASE_DIR%solutions\%PROBLEM%.py" (
    copy "%BASE_DIR%templates\%TEMPLATE%" "%BASE_DIR%solutions\%PROBLEM%.py" >nul
    echo ✅ Created: solutions\%PROBLEM%.py
) else (
    echo ⚠️ Already exists: solutions\%PROBLEM%.py
)

REM 建立第一筆測資
if not exist "%BASE_DIR%tests\%PROBLEM%_1.in" (
    echo. > "%BASE_DIR%tests\%PROBLEM%_1.in"
    echo ✅ Created: tests\%PROBLEM%_1.in
) else (
    echo ⚠️ Already exists: tests\%PROBLEM%_1.in
)

if not exist "%BASE_DIR%tests\%PROBLEM%_1.out" (
    echo. > "%BASE_DIR%tests\%PROBLEM%_1.out"
    echo ✅ Created: tests\%PROBLEM%_1.out
) else (
    echo ⚠️ Already exists: tests\%PROBLEM%_1.out
)

echo.
echo 🎉 Done! Now edit:
echo    - solutions\%PROBLEM%.py
echo    - tests\%PROBLEM%_1.in
echo    - tests\%PROBLEM%_1.out

if "%~2"=="--multi" (
    echo.
    echo 💡 Multi-solution tips:
    echo    - Define methods in SOLUTIONS dict
    echo    - Test all: python runner/test_runner.py %PROBLEM% --all
    echo    - Benchmark: python runner/test_runner.py %PROBLEM% --all --benchmark
)
