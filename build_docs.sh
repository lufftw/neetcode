#!/bin/bash
# ============================================
#  Build Documentation Locally
#  Usage: 
#    ./build_docs.sh              (build only)
#    ./build_docs.sh --serve      (build and serve locally)
#    ./build_docs.sh --clean      (clean build directory first)
# ============================================

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="${SCRIPT_DIR}/leetcode/bin/python"

# Check if virtual environment exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please create it first:"
    echo "  python -m venv leetcode"
    echo "  source leetcode/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Check if requirements are installed
if ! "$VENV_PYTHON" -c "import mkdocs" 2>/dev/null; then
    echo "Installing dependencies..."
    "$VENV_PYTHON" -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

# Clean build directory if requested
if [ "$1" = "--clean" ]; then
    echo "Cleaning build directory..."
    rm -rf "${SCRIPT_DIR}/site"
    shift
fi

echo ""
echo "============================================"
echo "Building Documentation"
echo "============================================"
echo ""

# Step 1: Generate Mind Maps (Markdown)
echo "[1/4] Generating mind maps (Markdown)..."
"$VENV_PYTHON" tools/generate_mindmaps.py
if [ $? -ne 0 ]; then
    echo "Error: Failed to generate mind maps"
    exit 1
fi

# Step 2: Generate Mind Maps (HTML)
echo "[2/4] Generating mind maps (HTML)..."
"$VENV_PYTHON" tools/generate_mindmaps.py --html
if [ $? -ne 0 ]; then
    echo "Error: Failed to generate HTML mind maps"
    exit 1
fi

# Step 3: Build MkDocs site
echo "[3/4] Building MkDocs site..."
"$VENV_PYTHON" -m mkdocs build
if [ $? -ne 0 ]; then
    echo "Error: Failed to build MkDocs site"
    exit 1
fi

# Step 4: Copy mind map HTML files
echo "[4/4] Copying mind map HTML files..."
if [ -d "${SCRIPT_DIR}/docs/pages/mindmaps" ]; then
    cp -r "${SCRIPT_DIR}/docs/pages/mindmaps" "${SCRIPT_DIR}/site/pages/" 2>/dev/null || true
fi
if [ -d "${SCRIPT_DIR}/docs/pages/assets" ]; then
    cp -r "${SCRIPT_DIR}/docs/pages/assets" "${SCRIPT_DIR}/site/pages/" 2>/dev/null || true
fi

echo ""
echo "============================================"
echo "Build Complete!"
echo "============================================"
echo ""
echo "Output directory: ${SCRIPT_DIR}/site"
echo ""

# Serve locally if requested
if [ "$1" = "--serve" ]; then
    echo "Starting local server..."
    echo "Visit http://127.0.0.1:8000"
    echo "Press Ctrl+C to stop"
    echo ""
    "$VENV_PYTHON" -m mkdocs serve
fi

