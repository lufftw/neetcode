# ============================================
# NeetCode Build System
# ============================================
# Usage:
#   make          - Build site (same as CI/CD)
#   make serve    - Build and serve locally
#   make clean    - Clean generated files
#   make ai       - Generate AI mindmaps
#   make help     - Show all commands
# ============================================

.PHONY: help build serve clean ai mindmaps html mkdocs test

# Default Python (adjust if needed)
PYTHON := leetcode/Scripts/python.exe
ifeq ($(OS),Windows_NT)
    PYTHON := leetcode/Scripts/python.exe
else
    PYTHON := leetcode/bin/python
endif

# Directories
SITE_DIR := site
MINDMAPS_MD := docs/mindmaps
MINDMAPS_HTML := docs/pages/mindmaps

help:
	@echo ""
	@echo "NeetCode Build System"
	@echo "====================="
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build     Build site (mirrors CI/CD pipeline)"
	@echo "  serve     Build and serve locally at http://127.0.0.1:8000"
	@echo "  clean     Remove generated files"
	@echo "  ai        Generate AI mindmaps (requires OPENAI_API_KEY)"
	@echo "  test      Run all tests"
	@echo "  help      Show this help"
	@echo ""

# Main build target (mirrors CI/CD)
build: mindmaps html mkdocs copy-html
	@echo ""
	@echo "============================================"
	@echo " Build complete!"
	@echo "============================================"
	@echo " Output: $(SITE_DIR)/"
	@echo " Preview: make serve"
	@echo "============================================"

# Generate Markdown mindmaps
mindmaps:
	@echo "[1/4] Generating Markdown mindmaps..."
	@$(PYTHON) tools/generate_mindmaps.py

# Generate HTML mindmaps
html:
	@echo "[2/4] Generating HTML mindmaps..."
	@$(PYTHON) tools/generate_mindmaps.py --html

# Build MkDocs site
mkdocs:
	@echo "[3/4] Building MkDocs site..."
	@$(PYTHON) -m mkdocs build

# Copy HTML to site directory
copy-html:
	@echo "[4/4] Copying HTML mindmaps to site..."
	@mkdir -p $(SITE_DIR)/pages/mindmaps
	@cp -r $(MINDMAPS_HTML)/* $(SITE_DIR)/pages/mindmaps/ 2>/dev/null || true
	@if [ -d "docs/pages/assets" ]; then \
		mkdir -p $(SITE_DIR)/pages/assets; \
		cp -r docs/pages/assets/* $(SITE_DIR)/pages/assets/ 2>/dev/null || true; \
	fi

# Build and serve
serve: build
	@echo ""
	@echo "[Serve] Starting local server..."
	@echo "        http://127.0.0.1:8000"
	@echo "        Press Ctrl+C to stop"
	@$(PYTHON) -m mkdocs serve

# Clean generated files
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf $(SITE_DIR)
	@echo "Cleaning generated mindmaps..."
	@find $(MINDMAPS_MD) -name "*.md" \
		! -name "index.md" \
		! -name "README.md" \
		! -name "*neetcode_ontology_ai*" \
		-delete 2>/dev/null || true
	@find $(MINDMAPS_HTML) -name "*.html" \
		! -name "*neetcode_ontology_ai*" \
		-delete 2>/dev/null || true
	@echo "Clean complete!"

# Generate AI mindmaps
ai:
	@echo "Generating AI mindmaps..."
	@$(PYTHON) tools/generate_mindmaps_ai.py
	@echo "Rebuilding site..."
	@$(MAKE) build

# Run tests
test:
	@echo "Running tests..."
	@$(PYTHON) -m pytest .dev/tests -q

