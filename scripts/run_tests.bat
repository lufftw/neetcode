@echo off
chcp 65001 >nul
REM ============================================
REM  Run All Tests
REM  Usage: 
REM    run_tests.bat 0001_two_sum
REM    run_tests.bat 0001_two_sum --all
REM    run_tests.bat 0001_two_sum --all --benchmark
REM ============================================

if "%~1"=="" (
    echo Usage: run_tests.bat ^<problem_name^> [options]
    echo Example: run_tests.bat 0001_two_sum
    echo          run_tests.bat 0001_two_sum --all
    echo          run_tests.bat 0001_two_sum --all --benchmark
    exit /b 1
)

REM Use virtual environment Python, pass all arguments
"%~dp0..\leetcode\Scripts\python.exe" "%~dp0..\runner\test_runner.py" %*
