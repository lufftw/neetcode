@echo off
chcp 65001 >nul
REM ============================================
REM  Run Single Test Case
REM  Usage: run_case.bat 0001_two_sum 1
REM ============================================

if "%~1"=="" (
    echo Usage: run_case.bat ^<problem_name^> ^<case_index^>
    echo Example: run_case.bat 0001_two_sum 1
    exit /b 1
)

if "%~2"=="" (
    echo Usage: run_case.bat ^<problem_name^> ^<case_index^>
    echo Example: run_case.bat 0001_two_sum 1
    exit /b 1
)

REM Use virtual environment Python
"%~dp0..\leetcode\Scripts\python.exe" "%~dp0..\runner\case_runner.py" %1 %2
