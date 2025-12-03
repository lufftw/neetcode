@echo off
chcp 65001 >nul
REM ============================================
REM  執行所有測資 (Run All Tests)
REM  用法: run_tests.bat 0001_two_sum
REM ============================================

if "%~1"=="" (
    echo 用法: run_tests.bat ^<problem_name^>
    echo Example: run_tests.bat 0001_two_sum
    exit /b 1
)

REM 使用虛擬環境的 Python
"%~dp0leetcode\Scripts\python.exe" runner/test_runner.py %1
