@echo off
chcp 65001 >nul
REM ============================================
REM  Build Documentation Locally
REM  Usage: 
REM    build_docs.bat              (build only)
REM    build_docs.bat --serve      (build and serve locally)
REM    build_docs.bat --clean      (clean build directory first)
REM ============================================

set BASE_DIR=%~dp0
set VENV_PYTHON=%BASE_DIR%leetcode\Scripts\python.exe

REM Check if virtual environment exists
if not exist "%VENV_PYTHON%" (
    echo Error: Virtual environment not found!
    echo Please create it first:
    echo   py -3.11 -m venv leetcode
    echo   leetcode\Scripts\activate
    echo   pip install -r requirements.txt
    exit /b 1
)

REM Check if requirements are installed
"%VENV_PYTHON%" -c "import mkdocs" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    "%VENV_PYTHON%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        exit /b 1
    )
)

REM Clean build directory if requested
if "%~1"=="--clean" (
    echo Cleaning build directory...
    if exist "%BASE_DIR%site" (
        rmdir /s /q "%BASE_DIR%site"
    )
    shift
)

echo.
echo ============================================
echo Building Documentation
echo ============================================
echo.

REM Step 1: Generate Mind Maps (Markdown)
echo [1/4] Generating mind maps (Markdown)...
"%VENV_PYTHON%" tools/generate_mindmaps.py
if errorlevel 1 (
    echo Error: Failed to generate mind maps
    exit /b 1
)

REM Step 2: Generate Mind Maps (HTML)
echo [2/4] Generating mind maps (HTML)...
"%VENV_PYTHON%" tools/generate_mindmaps.py --html
if errorlevel 1 (
    echo Error: Failed to generate HTML mind maps
    exit /b 1
)

REM Step 3: Build MkDocs site
echo [3/4] Building MkDocs site...
"%VENV_PYTHON%" -m mkdocs build
if errorlevel 1 (
    echo Error: Failed to build MkDocs site
    exit /b 1
)

REM Step 4: Copy mind map HTML files
echo [4/4] Copying mind map HTML files...
if exist "%BASE_DIR%docs\pages\mindmaps" (
    xcopy /E /I /Y "%BASE_DIR%docs\pages\mindmaps" "%BASE_DIR%site\pages\mindmaps" >nul
)
if exist "%BASE_DIR%docs\pages\assets" (
    xcopy /E /I /Y "%BASE_DIR%docs\pages\assets" "%BASE_DIR%site\pages\assets" >nul 2>nul
)

echo.
echo ============================================
echo Build Complete!
echo ============================================
echo.
echo Output directory: %BASE_DIR%site
echo.

REM Serve locally if requested
if "%~1"=="--serve" (
    echo Starting local server...
    echo Visit http://127.0.0.1:8000
    echo Press Ctrl+C to stop
    echo.
    "%VENV_PYTHON%" -m mkdocs serve
)

