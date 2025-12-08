@echo off
chcp 65001 >nul
REM Run unit tests for neetcode runner system
REM
REM This script runs all characterization tests to ensure
REM that refactoring doesn't break existing behavior.

echo ========================================
echo Running Unit Tests
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

REM Change to project root directory to run tests
cd /d "%~dp0.."

REM Run tests with verbose output
echo Running all tests...
echo Using Python: %PYTHON_EXE%
echo.
"%PYTHON_EXE%" -m pytest .dev/tests -v --tb=short

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo All tests passed!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Some tests failed!
    echo ========================================
    exit /b 1
)

