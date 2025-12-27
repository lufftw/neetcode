@echo off
chcp 65001 >nul
REM Run solution format compliance tests
REM
REM This script tests solution file format compliance with
REM Pure Polymorphic Architecture standards.
REM
REM Tests include:
REM   - Solution comment format (Solution 1:)
REM   - Time/Space complexity comments
REM   - SOLUTIONS dictionary structure
REM   - No wrapper functions
REM   - Uses get_solver()

echo ========================================
echo Running Solution Format Tests
echo ========================================
echo.

REM Use virtual environment Python
set PYTHON_EXE=%~dp0..\leetcode\Scripts\python.exe

REM Check if virtual environment exists
if not exist "%PYTHON_EXE%" (
    echo [ERROR] Virtual environment not found: %PYTHON_EXE%
    echo Please create virtual environment first:
    echo   python -m venv leetcode
    echo   leetcode\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    exit /b 1
)

REM Change to project root directory
cd /d "%~dp0.."

REM Run format checker first (quick check)
echo [1/2] Running format checker...
"%PYTHON_EXE%" tools/check_solutions.py
if %errorlevel% neq 0 (
    echo.
    echo Format checker found issues!
    echo.
)

echo.
echo [2/2] Running format unit tests...
"%PYTHON_EXE%" -m pytest tools/review-code/validation/tests/test_solution_format.py -v --tb=short

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo All format tests passed!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Some format tests failed!
    echo ========================================
    exit /b 1
)
