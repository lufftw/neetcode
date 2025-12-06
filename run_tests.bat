@echo off
chcp 65001 >nul
REM ============================================
REM  Run All Tests
REM  Usage: run_tests.bat 0001_two_sum
REM ============================================

if "%~1"=="" (
    echo Usage: run_tests.bat ^<problem_name^>
    echo Example: run_tests.bat 0001_two_sum
    exit /b 1
)

REM Use virtual environment Python
"%~dp0leetcode\Scripts\python.exe" runner/test_runner.py %1
