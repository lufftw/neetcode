@echo off
chcp 65001 >nul
REM ============================================================================
REM Run ALL tests for the neetcode project
REM ============================================================================
REM
REM This script runs three categories of tests:
REM
REM 1. Solution Format Tests (tools/review-code/validation/tests/)
REM    - Pure Polymorphic Architecture compliance
REM    - Solution comment format
REM    - Complexity comments
REM
REM 2. Component Tests (.dev/tests/)
REM    - Runner module unit tests
REM    - Integration tests
REM    - Edge case tests
REM
REM 3. Solution Correctness Tests (.dev/tests_solutions/)
REM    - Static test cases (from tests/ directory)
REM    - Generated test cases (if available)
REM
REM Exit Codes:
REM   0 - All tests passed
REM   1 - One or more test categories failed
REM
REM ============================================================================

echo ================================================================================
echo                         NEETCODE PROJECT - FULL TEST SUITE
echo ================================================================================
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

REM Check if pytest is installed
"%PYTHON_EXE%" -m pytest --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pytest is not installed in virtual environment
    echo Please install pytest first:
    echo   leetcode\Scripts\activate
    echo   pip install pytest pytest-cov
    echo.
    exit /b 1
)

REM Change to project root directory
cd /d "%~dp0.."

set FORMAT_RESULT=0
set COMPONENT_RESULT=0
set SOLUTION_RESULT=0

REM ============================================================================
REM 1. Solution Format Tests
REM ============================================================================
echo.
echo ================================================================================
echo [1/3] SOLUTION FORMAT TESTS
echo ================================================================================
echo.
echo Checking Pure Polymorphic Architecture compliance...
echo.

"%PYTHON_EXE%" tools/review-code/validation/check_solutions.py
if %errorlevel% neq 0 (
    echo.
    echo [WARN] Format checker found issues
)

echo.
"%PYTHON_EXE%" -m pytest tools/review-code/validation/tests/test_solution_format.py -v --tb=short
if %errorlevel% neq 0 (
    echo.
    echo [FAIL] Solution format tests failed!
    set FORMAT_RESULT=1
) else (
    echo.
    echo [PASS] Solution format tests passed
)

REM ============================================================================
REM 2. Component Tests (Runner modules)
REM ============================================================================
echo.
echo ================================================================================
echo [2/3] COMPONENT TESTS (Runner Modules)
echo ================================================================================
echo.
echo Testing runner module functionality...
echo.

"%PYTHON_EXE%" -m pytest .dev/tests -v --tb=short
if %errorlevel% neq 0 (
    echo.
    echo [FAIL] Component tests failed!
    set COMPONENT_RESULT=1
) else (
    echo.
    echo [PASS] Component tests passed
)

REM ============================================================================
REM 3. Solution Correctness Tests
REM ============================================================================
echo.
echo ================================================================================
echo [3/3] SOLUTION CORRECTNESS TESTS
echo ================================================================================
echo.
echo Testing all solutions with test cases...
echo.

"%PYTHON_EXE%" -m pytest .dev/tests_solutions -v --tb=short
if %errorlevel% neq 0 (
    echo.
    echo [FAIL] Solution correctness tests failed!
    set SOLUTION_RESULT=1
) else (
    echo.
    echo [PASS] Solution correctness tests passed
)

REM ============================================================================
REM Summary
REM ============================================================================
echo.
echo ================================================================================
echo                                 TEST SUMMARY
echo ================================================================================
echo.

set /a TOTAL_FAILED=%FORMAT_RESULT%+%COMPONENT_RESULT%+%SOLUTION_RESULT%

if %TOTAL_FAILED% equ 0 (
    echo   [OK] All test categories passed!
    echo.
    echo   - Solution Format Tests:      PASSED
    echo   - Component Tests:            PASSED
    echo   - Solution Correctness Tests: PASSED
    echo.
    echo ================================================================================
    exit /b 0
) else (
    echo   [FAILED] %TOTAL_FAILED% test category(ies) failed!
    echo.
    if %FORMAT_RESULT% equ 1 (
        echo   - Solution Format Tests:      FAILED
    ) else (
        echo   - Solution Format Tests:      PASSED
    )
    if %COMPONENT_RESULT% equ 1 (
        echo   - Component Tests:            FAILED
    ) else (
        echo   - Component Tests:            PASSED
    )
    if %SOLUTION_RESULT% equ 1 (
        echo   - Solution Correctness Tests: FAILED
    ) else (
        echo   - Solution Correctness Tests: PASSED
    )
    echo.
    echo   Please review the output above for details.
    echo.
    echo ================================================================================
    exit /b 1
)
