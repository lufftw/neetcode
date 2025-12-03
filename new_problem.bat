@echo off
chcp 65001 >nul
REM ============================================
REM  建立新題目 (Create New Problem)
REM  用法: new_problem.bat 0001_two_sum
REM ============================================

if "%~1"=="" (
    echo 用法: new_problem.bat ^<problem_name^>
    echo Example: new_problem.bat 0001_two_sum
    exit /b 1
)

set PROBLEM=%~1
set BASE_DIR=%~dp0

REM 建立 solution 檔案
if not exist "%BASE_DIR%solutions\%PROBLEM%.py" (
    copy "%BASE_DIR%templates\template_solution.py" "%BASE_DIR%solutions\%PROBLEM%.py" >nul
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
