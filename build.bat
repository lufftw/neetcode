@echo off
REM ============================================
REM Local Build Script (mirrors CI/CD pipeline)
REM ============================================
REM Usage:
REM   build.bat           - Build only
REM   build.bat serve     - Build and serve locally
REM   build.bat clean     - Clean build artifacts
REM   build.bat ai        - Generate AI mindmaps (requires OPENAI_API_KEY)
REM ============================================

setlocal enabledelayedexpansion

REM Configuration
set VENV_PATH=leetcode\Scripts\python.exe
set SITE_DIR=site
set MINDMAPS_MD=docs\mindmaps
set MINDMAPS_HTML=docs\pages\mindmaps

REM Check if virtual environment exists
if not exist "%VENV_PATH%" (
    echo [ERROR] Virtual environment not found at %VENV_PATH%
    echo Please run: py -3.11 -m venv leetcode
    exit /b 1
)

REM Parse command
set CMD=%1
if "%CMD%"=="" set CMD=build

if "%CMD%"=="clean" goto :clean
if "%CMD%"=="serve" goto :build_and_serve
if "%CMD%"=="ai" goto :ai
if "%CMD%"=="build" goto :build
if "%CMD%"=="help" goto :help

echo [ERROR] Unknown command: %CMD%
goto :help

:help
echo.
echo Usage: build.bat [command]
echo.
echo Commands:
echo   build   - Generate mindmaps and build MkDocs site (default)
echo   serve   - Build and serve locally at http://127.0.0.1:8000
echo   clean   - Remove generated files
echo   ai      - Generate AI mindmaps (requires OPENAI_API_KEY)
echo   help    - Show this help message
echo.
exit /b 0

:clean
echo.
echo [1/3] Cleaning build artifacts...
if exist "%SITE_DIR%" rmdir /s /q "%SITE_DIR%"
echo       Removed %SITE_DIR%/

echo [2/3] Cleaning generated mindmaps (keeping AI and manual files)...
for %%f in (%MINDMAPS_MD%\*.md) do (
    set "filename=%%~nxf"
    if not "!filename!"=="index.md" (
        if not "!filename!"=="README.md" (
            echo !filename! | findstr /i "neetcode_ontology_ai" >nul
            if errorlevel 1 (
                del "%%f" 2>nul
                echo       Removed %%f
            )
        )
    )
)

echo [3/3] Cleaning generated HTML (keeping AI files)...
for %%f in (%MINDMAPS_HTML%\*.html) do (
    set "filename=%%~nxf"
    echo !filename! | findstr /i "neetcode_ontology_ai" >nul
    if errorlevel 1 (
        del "%%f" 2>nul
        echo       Removed %%f
    )
)

echo.
echo [OK] Clean complete!
exit /b 0

:build
echo.
echo ============================================
echo  Local Build (mirrors CI/CD pipeline)
echo ============================================
echo.

echo [1/4] Generating Markdown mindmaps...
%VENV_PATH% tools/generate_mindmaps.py
if errorlevel 1 (
    echo [ERROR] Failed to generate Markdown mindmaps
    exit /b 1
)
echo       Done!

echo [2/4] Generating HTML mindmaps...
%VENV_PATH% tools/generate_mindmaps.py --html
if errorlevel 1 (
    echo [ERROR] Failed to generate HTML mindmaps
    exit /b 1
)
echo       Done!

echo [3/4] Building MkDocs site...
%VENV_PATH% -m mkdocs build
if errorlevel 1 (
    echo [ERROR] Failed to build MkDocs site
    exit /b 1
)
echo       Done!

echo [4/4] Copying HTML mindmaps to site...
if not exist "%SITE_DIR%\pages\mindmaps" mkdir "%SITE_DIR%\pages\mindmaps"
xcopy /s /y /q "%MINDMAPS_HTML%\*" "%SITE_DIR%\pages\mindmaps\" >nul
if exist "docs\pages\assets" (
    if not exist "%SITE_DIR%\pages\assets" mkdir "%SITE_DIR%\pages\assets"
    xcopy /s /y /q "docs\pages\assets\*" "%SITE_DIR%\pages\assets\" >nul
)
echo       Done!

echo.
echo ============================================
echo  Build complete!
echo ============================================
echo  Output: %SITE_DIR%\
echo  Preview: build.bat serve
echo ============================================
exit /b 0

:build_and_serve
call :build
if errorlevel 1 exit /b 1

echo.
echo [Serve] Starting local server...
echo         http://127.0.0.1:8000
echo         Press Ctrl+C to stop
echo.
%VENV_PATH% -m mkdocs serve
exit /b 0

:ai
echo.
echo ============================================
echo  AI Mind Map Generation
echo ============================================
echo.

if "%OPENAI_API_KEY%"=="" (
    echo [ERROR] OPENAI_API_KEY environment variable not set
    echo.
    echo Please set it first:
    echo   $env:OPENAI_API_KEY = "sk-..."
    echo.
    echo Or generate prompt only and copy to ChatGPT:
    echo   The prompt will be saved to tools\prompts\generated\mindmap_prompt.md
    echo.
)

echo [1/2] Generating AI mindmaps...
%VENV_PATH% tools/generate_mindmaps_ai.py
if errorlevel 1 (
    echo [WARNING] AI generation may have failed or was skipped
    echo          Check tools\prompts\generated\mindmap_prompt.md for manual use
)

echo [2/2] Rebuilding site with new AI mindmaps...
call :build
exit /b 0

