#!/bin/bash
# ============================================
#  Build Documentation Locally
#  Usage: 
#    ./scripts/build_docs.sh              (build only)
#    ./scripts/build_docs.sh --serve      (build and serve locally)
#    ./scripts/build_docs.sh --clean      (clean build directory first)
# ============================================

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."
VENV_PYTHON="$PROJECT_ROOT/leetcode/bin/python"

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
    cd "$PROJECT_ROOT"
    "$VENV_PYTHON" -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

# Change to project root directory
cd "$PROJECT_ROOT"

# Clean build directory if requested
if [ "$1" = "--clean" ]; then
    echo "Cleaning build directory..."
    rm -rf "$PROJECT_ROOT/site"
    shift
fi

echo ""
echo "============================================"
echo "Building Documentation"
echo "============================================"
echo ""

# Step 1: Generate Mind Maps (Markdown)
echo "[1/5] Generating mind maps (Markdown)..."
"$VENV_PYTHON" tools/generate_mindmaps.py
if [ $? -ne 0 ]; then
    echo "Error: Failed to generate mind maps"
    exit 1
fi

# Step 2: Generate Mind Maps (HTML)
echo "[2/5] Generating mind maps (HTML)..."
"$VENV_PYTHON" tools/generate_mindmaps.py --html
if [ $? -ne 0 ]; then
    echo "Error: Failed to generate HTML mind maps"
    exit 1
fi

# Step 3: Ask if user wants to generate AI mind maps
echo ""
echo "[3/5] Generate AI-powered mind maps?"
echo "Note: This requires OPENAI_API_KEY environment variable"
echo ""
read -p "Generate AI mind maps? (y/N): " GENERATE_AI
if [ "$GENERATE_AI" = "y" ] || [ "$GENERATE_AI" = "Y" ]; then
    echo "Generating AI mind maps..."
    "$VENV_PYTHON" tools/generate_mindmaps_ai.py
    if [ $? -ne 0 ]; then
        echo "Warning: Failed to generate AI mind maps (may need OPENAI_API_KEY)"
        echo "Continuing with build..."
    else
        echo "AI mind maps generated successfully."
    fi
else
    echo "Skipping AI mind map generation."
fi

# Step 4: Build MkDocs site
echo "[4/5] Building MkDocs site..."
"$VENV_PYTHON" -m mkdocs build
if [ $? -ne 0 ]; then
    echo "Error: Failed to build MkDocs site"
    exit 1
fi

# Step 5: Copy mind map HTML files
echo "[5/5] Copying mind map HTML files..."
if [ -d "$PROJECT_ROOT/docs/pages/mindmaps" ]; then
    cp -r "$PROJECT_ROOT/docs/pages/mindmaps" "$PROJECT_ROOT/site/pages/" 2>/dev/null || true
fi
if [ -d "$PROJECT_ROOT/docs/pages/assets" ]; then
    cp -r "$PROJECT_ROOT/docs/pages/assets" "$PROJECT_ROOT/site/pages/" 2>/dev/null || true
fi

echo ""
echo "============================================"
echo "Build Complete!"
echo "============================================"
echo ""
echo "Output directory: $PROJECT_ROOT/site"
echo ""

# Serve locally if requested
if [ "$1" = "--serve" ]; then
    echo "Starting local server..."
    echo "Visit http://127.0.0.1:8000"
    echo "Press Ctrl+C to stop"
    echo ""
    "$VENV_PYTHON" -m mkdocs serve
fi

