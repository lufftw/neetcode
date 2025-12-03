@echo off
chcp 65001 >nul
REM ============================================
REM  執行單一測資 (Run Single Case)
REM  用法: run_case.bat 0001_two_sum 1
REM ============================================

if "%~1"=="" (
    echo 用法: run_case.bat ^<problem_name^> ^<case_index^>
    echo Example: run_case.bat 0001_two_sum 1
    exit /b 1
)

if "%~2"=="" (
    echo 用法: run_case.bat ^<problem_name^> ^<case_index^>
    echo Example: run_case.bat 0001_two_sum 1
    exit /b 1
)

REM 使用虛擬環境的 Python
"%~dp0leetcode\Scripts\python.exe" runner/case_runner.py %1 %2
