@echo off
REM Standalone script to run solution format tests on Windows
REM Usage: run_format_tests.bat [--verbose|--quiet]

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

REM Use virtual environment Python if available, otherwise system Python
if exist "%PROJECT_ROOT%\leetcode\Scripts\python.exe" (
    "%PROJECT_ROOT%\leetcode\Scripts\python.exe" "%SCRIPT_DIR%run_format_tests.py" %*
) else (
    python "%SCRIPT_DIR%run_format_tests.py" %*
)

exit /b %ERRORLEVEL%

