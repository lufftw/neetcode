#!/bin/bash
# ============================================
# Local Build Script (mirrors CI/CD pipeline)
# ============================================
# Usage:
#   ./build.sh           - Build only
#   ./build.sh serve     - Build and serve locally
#   ./build.sh clean     - Clean build artifacts
#   ./build.sh ai        - Generate AI mindmaps (requires OPENAI_API_KEY)
# ============================================

set -e

# Configuration
VENV_PATH="leetcode/bin/python"
SITE_DIR="site"
MINDMAPS_MD="docs/mindmaps"
MINDMAPS_HTML="docs/pages/mindmaps"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -f "$VENV_PATH" ]; then
    echo -e "${RED}[ERROR]${NC} Virtual environment not found at $VENV_PATH"
    echo "Please run: python -m venv leetcode"
    exit 1
fi

# Parse command
CMD=${1:-build}

show_help() {
    echo ""
    echo "Usage: ./build.sh [command]"
    echo ""
    echo "Commands:"
    echo "  build   - Generate mindmaps and build MkDocs site (default)"
    echo "  serve   - Build and serve locally at http://127.0.0.1:8000"
    echo "  clean   - Remove generated files"
    echo "  ai      - Generate AI mindmaps (requires OPENAI_API_KEY)"
    echo "  help    - Show this help message"
    echo ""
}

do_clean() {
    echo ""
    echo -e "${YELLOW}[1/3]${NC} Cleaning build artifacts..."
    rm -rf "$SITE_DIR"
    echo "       Removed $SITE_DIR/"

    echo -e "${YELLOW}[2/3]${NC} Cleaning generated mindmaps (keeping AI and manual files)..."
    for f in "$MINDMAPS_MD"/*.md; do
        filename=$(basename "$f")
        if [[ "$filename" != "index.md" && "$filename" != "README.md" && "$filename" != *"neetcode_ontology_ai"* ]]; then
            rm -f "$f"
            echo "       Removed $f"
        fi
    done

    echo -e "${YELLOW}[3/3]${NC} Cleaning generated HTML (keeping AI files)..."
    for f in "$MINDMAPS_HTML"/*.html 2>/dev/null; do
        filename=$(basename "$f")
        if [[ "$filename" != *"neetcode_ontology_ai"* ]]; then
            rm -f "$f"
            echo "       Removed $f"
        fi
    done

    echo ""
    echo -e "${GREEN}[OK]${NC} Clean complete!"
}

do_build() {
    echo ""
    echo "============================================"
    echo " Local Build (mirrors CI/CD pipeline)"
    echo "============================================"
    echo ""

    echo -e "${YELLOW}[1/4]${NC} Generating Markdown mindmaps..."
    $VENV_PATH tools/generate_mindmaps.py
    echo "       Done!"

    echo -e "${YELLOW}[2/4]${NC} Generating HTML mindmaps..."
    $VENV_PATH tools/generate_mindmaps.py --html
    echo "       Done!"

    echo -e "${YELLOW}[3/4]${NC} Building MkDocs site..."
    $VENV_PATH -m mkdocs build
    echo "       Done!"

    echo -e "${YELLOW}[4/4]${NC} Copying HTML mindmaps to site..."
    mkdir -p "$SITE_DIR/pages/mindmaps"
    cp -r "$MINDMAPS_HTML"/* "$SITE_DIR/pages/mindmaps/" 2>/dev/null || true
    if [ -d "docs/pages/assets" ]; then
        mkdir -p "$SITE_DIR/pages/assets"
        cp -r docs/pages/assets/* "$SITE_DIR/pages/assets/" 2>/dev/null || true
    fi
    echo "       Done!"

    echo ""
    echo "============================================"
    echo -e " ${GREEN}Build complete!${NC}"
    echo "============================================"
    echo " Output: $SITE_DIR/"
    echo " Preview: ./build.sh serve"
    echo "============================================"
}

do_serve() {
    do_build
    echo ""
    echo -e "${YELLOW}[Serve]${NC} Starting local server..."
    echo "         http://127.0.0.1:8000"
    echo "         Press Ctrl+C to stop"
    echo ""
    $VENV_PATH -m mkdocs serve
}

do_ai() {
    echo ""
    echo "============================================"
    echo " AI Mind Map Generation"
    echo "============================================"
    echo ""

    if [ -z "$OPENAI_API_KEY" ]; then
        echo -e "${RED}[ERROR]${NC} OPENAI_API_KEY environment variable not set"
        echo ""
        echo "Please set it first:"
        echo "  export OPENAI_API_KEY=\"sk-...\""
        echo ""
        echo "Or generate prompt only and copy to ChatGPT:"
        echo "  The prompt will be saved to tools/prompts/generated/mindmap_prompt.md"
        echo ""
    fi

    echo -e "${YELLOW}[1/2]${NC} Generating AI mindmaps..."
    $VENV_PATH tools/generate_mindmaps_ai.py || {
        echo -e "${YELLOW}[WARNING]${NC} AI generation may have failed or was skipped"
        echo "          Check tools/prompts/generated/mindmap_prompt.md for manual use"
    }

    echo -e "${YELLOW}[2/2]${NC} Rebuilding site with new AI mindmaps..."
    do_build
}

case "$CMD" in
    build)
        do_build
        ;;
    serve)
        do_serve
        ;;
    clean)
        do_clean
        ;;
    ai)
        do_ai
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}[ERROR]${NC} Unknown command: $CMD"
        show_help
        exit 1
        ;;
esac

