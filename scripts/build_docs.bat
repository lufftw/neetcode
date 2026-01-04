@echo off
chcp 65001 >nul
REM ============================================
REM  Build Documentation Locally
REM  Usage: 
REM    scripts\build_docs.bat              (build only)
REM    scripts\build_docs.bat --serve      (build and serve locally)
REM    scripts\build_docs.bat --clean      (clean build directory first)
REM ============================================

REM Get project root directory (parent of scripts/)
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set VENV_PYTHON=%PROJECT_ROOT%\leetcode\Scripts\python.exe

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
    cd /d "%PROJECT_ROOT%"
    "%VENV_PYTHON%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        exit /b 1
    )
)

REM Change to project root directory
cd /d "%PROJECT_ROOT%"

REM Clean build directory if requested
if "%~1"=="--clean" (
    echo Cleaning build directory...
    if exist "%PROJECT_ROOT%\site" (
        rmdir /s /q "%PROJECT_ROOT%\site"
    )
    shift
)

echo.
echo ============================================
echo Building Documentation
echo ============================================
echo.

REM Step 1: Generate Mind Maps (Markdown)
echo [1/5] Generating mind maps (Markdown)...
"%VENV_PYTHON%" tools/mindmaps/generate_mindmaps.py
if errorlevel 1 (
    echo Error: Failed to generate mind maps
    exit /b 1
)

REM Step 2: Generate Mind Maps (HTML)
echo [2/5] Generating mind maps (HTML)...
"%VENV_PYTHON%" tools/mindmaps/generate_mindmaps.py --html
if errorlevel 1 (
    echo Error: Failed to generate HTML mind maps
    exit /b 1
)

REM Step 3: Ask if user wants to generate AI mind maps
echo.
echo [3/5] Generate AI-powered mind maps?
echo Note: This requires OPENAI_API_KEY environment variable
echo.
set /p GENERATE_AI="Generate AI mind maps? (Y/N): "
if /i "%GENERATE_AI%"=="Y" (
    echo Generating AI mind maps...
    "%VENV_PYTHON%" tools/mindmaps/generate_mindmaps_ai.py
    if errorlevel 1 (
        echo Warning: Failed to generate AI mind maps (may need OPENAI_API_KEY)
        echo Continuing with build...
    ) else (
        echo AI mind maps generated successfully.
    )
) else (
    echo Skipping AI mind map generation.
)

REM Step 4: Build MkDocs site
echo [4/5] Building MkDocs site...
"%VENV_PYTHON%" -m mkdocs build
if errorlevel 1 (
    echo Error: Failed to build MkDocs site
    exit /b 1
)

REM Step 5: Copy mind map HTML files
echo [5/5] Copying mind map HTML files...
if exist "%PROJECT_ROOT%\docs\pages\mindmaps" (
    xcopy /E /I /Y "%PROJECT_ROOT%\docs\pages\mindmaps" "%PROJECT_ROOT%\site\pages\mindmaps" >nul
)
if exist "%PROJECT_ROOT%\docs\pages\assets" (
    xcopy /E /I /Y "%PROJECT_ROOT%\docs\pages\assets" "%PROJECT_ROOT%\site\pages\assets" >nul 2>nul
)

echo.
echo ============================================
echo Build Complete!
echo ============================================
echo.
echo Output directory: %PROJECT_ROOT%\site
echo.

REM Serve locally if requested
if "%~1"=="--serve" (
    echo Starting local server...
    echo Visit http://127.0.0.1:8000
    echo Press Ctrl+C to stop
    echo.
    "%VENV_PYTHON%" -m mkdocs serve
)

