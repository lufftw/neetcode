# Maintenance Tools

> **Status**: Informational  
> **Scope**: Maintenance scripts in tools/maintenance/  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}  
> **Purpose**: Scripts for maintaining and standardizing documentation file naming conventions  
> **Location**: `tools/maintenance/`

This module contains maintenance scripts for standardizing documentation file naming conventions and fixing references across the project.

---

## Overview

The maintenance tools primarily focus on:

- **Documentation Naming Standardization**: Renaming documentation files to kebab-case convention
- **Reference Updates**: Fixing references to renamed files across the codebase
- **Verification**: Ensuring all references have been properly updated

---

## Directory Structure

```
tools/maintenance/
└── doc-naming/                  # Documentation naming standardization tools
    ├── rename_docs_to_kebab_case.py    # Main renaming script
    ├── rename_md_files.py              # Rename Markdown files
    ├── rename_mindmap_html_files.py     # Rename mindmap HTML files
    ├── rename_mindmap_html.py           # Rename mindmap HTML (alternative)
    ├── fix_html_references.py           # Fix HTML file references
    ├── fix_readme_filenames.py          # Fix README filename errors
    ├── fix_patterndocs_readme.py        # Fix pattern docs README
    ├── fix_remaining_references.py      # Fix remaining references
    ├── update_html_references.py        # Update HTML references
    ├── verify_all_renames.py             # Verify all renames completed
    ├── rename_mapping.json              # Generated mapping file
    └── rename_mapping.txt               # Text format mapping
```

---

## Documentation Naming Standardization

### Purpose

Standardizes all documentation filenames to kebab-case convention as specified in [documentation-naming.md](../../contributors/documentation-naming.md).

### Naming Convention

- **kebab-case**: Lowercase with hyphens (e.g., `pattern-hierarchy.md`)
- **Exclusions**: README files, index files, and files prefixed with `_` are not renamed
- **Special Mappings**: Some files have manual overrides defined in `SPECIAL_MAPPINGS`

### Main Script: `rename_docs_to_kebab_case.py`

The primary script for renaming documentation files and updating references.

#### Usage

```bash
# Generate mapping table for review (dry run)
python tools/maintenance/doc-naming/rename_docs_to_kebab_case.py --dry-run

# Execute full migration
python tools/maintenance/doc-naming/rename_docs_to_kebab_case.py

# Verify after migration
python tools/maintenance/doc-naming/rename_docs_to_kebab_case.py --verify-only
```

#### Features

- **Dry Run Mode**: Preview changes without making modifications
- **Verification Mode**: Check that all references have been updated
- **Git Integration**: Uses `git mv` to preserve file history
- **Reference Updates**: Automatically updates references in:
  - Markdown files
  - HTML files
  - Configuration files
  - Python scripts
- **Mapping Generation**: Creates `rename_mapping.json` and `rename_mapping.txt`

#### Excluded Files

The following files are excluded from renaming:

- `README.md`
- `README_zh-TW.md`
- Files starting with `_` (e.g., `_header.md`)
- `index.md` and `index_zh-TW.md`

#### Special Mappings

Some files require manual overrides due to special naming requirements:

```python
SPECIAL_MAPPINGS = {
    'tools/ai-markmap-agent/prompts/writer/writer_behavior - 預備.md': 
        'tools/ai-markmap-agent/prompts/writer/writer-behavior-delete.md',
}
```

---

## Individual Scripts

### `rename_md_files.py`

Renames all `.md` files (except README variants) to kebab-case.

```bash
python tools/maintenance/doc-naming/rename_md_files.py
```

**Features:**
- Converts filenames to kebab-case
- Handles CamelCase, snake_case, and spaces
- Creates mapping file
- Updates references using `git mv`

### `rename_mindmap_html_files.py`

Renames mindmap HTML files from snake_case to kebab-case.

```bash
python tools/maintenance/doc-naming/rename_mindmap_html_files.py
```

**Mapping:**
- `algorithm_usage.html` → `algorithm-usage.html`
- `company_coverage.html` → `company-coverage.html`
- `data_structure.html` → `data-structure.html`
- `difficulty_topics.html` → `difficulty-topics.html`
- `family_derivation.html` → `family-derivation.html`
- `pattern_hierarchy.html` → `pattern-hierarchy.html`
- `problem_relations.html` → `problem-relations.html`
- `roadmap_paths.html` → `roadmap-paths.html`
- `solution_variants.html` → `solution-variants.html`

### `fix_html_references.py`

Fixes references to renamed HTML files in `docs/pages/mindmaps/`.

```bash
python tools/maintenance/doc-naming/fix_html_references.py
```

**What it does:**
- Updates all references from snake_case to kebab-case filenames
- Scans Markdown and HTML files for old references
- Updates links and image references

### `fix_readme_filenames.py`

Fixes filename errors in `docs/patterns/README.md`.

```bash
python tools/maintenance/doc-naming/fix_readme_filenames.py
```

**Fixes:**
- Incorrect filename patterns (e.g., `@03-base.md` → `0003-base.md`)
- Missing 4-digit padding in problem numbers
- Incorrect prefix patterns

### `fix_patterndocs_readme.py`

Fixes pattern documentation README references.

```bash
python tools/maintenance/doc-naming/fix_patterndocs_readme.py
```

### `fix_remaining_references.py`

Fixes any remaining references that were missed in previous passes.

```bash
python tools/maintenance/doc-naming/fix_remaining_references.py
```

### `update_html_references.py`

Updates HTML file references across the codebase.

```bash
python tools/maintenance/doc-naming/update_html_references.py
```

### `verify_all_renames.py`

Verifies that all old filename references have been replaced.

```bash
python tools/maintenance/doc-naming/verify_all_renames.py
```

**Output:**
- Lists any files still containing old filename references
- Excludes mapping files (which are supposed to contain old names)
- Reports clean status for each renamed file

**Example Output:**
```
Checking: docs/mindmaps/pattern-hierarchy.md
  Old name: pattern_hierarchy.md
  ✅ No old references found

Checking: docs/mindmaps/family-derivation.md
  Old name: family_derivation.md
  ✅ No old references found
```

---

## Workflow

### Complete Migration Workflow

1. **Preview Changes** (Dry Run):
   ```bash
   python tools/maintenance/doc-naming/rename_docs_to_kebab_case.py --dry-run
   ```

2. **Review Mapping**:
   - Check `rename_mapping.json` or `rename_mapping.txt`
   - Verify all renames are correct

3. **Execute Migration**:
   ```bash
   python tools/maintenance/doc-naming/rename_docs_to_kebab_case.py
   ```

4. **Fix Specific References** (if needed):
   ```bash
   python tools/maintenance/doc-naming/fix_html_references.py
   python tools/maintenance/doc-naming/fix_readme_filenames.py
   python tools/maintenance/doc-naming/fix_remaining_references.py
   ```

5. **Verify Completion**:
   ```bash
   python tools/maintenance/doc-naming/verify_all_renames.py
   ```

### Incremental Fixes

For fixing specific issues:

```bash
# Fix HTML references only
python tools/maintenance/doc-naming/fix_html_references.py

# Fix README filename errors
python tools/maintenance/doc-naming/fix_readme_filenames.py

# Fix remaining references
python tools/maintenance/doc-naming/fix_remaining_references.py
```

---

## Mapping Files

### `rename_mapping.json`

JSON format mapping of old filenames to new filenames:

```json
{
  "docs/mindmaps/pattern_hierarchy.md": "docs/mindmaps/pattern-hierarchy.md",
  "docs/mindmaps/family_derivation.md": "docs/mindmaps/family-derivation.md"
}
```

### `rename_mapping.txt`

Human-readable text format mapping:

```
# Documentation Filename Rename Mapping
docs/mindmaps/pattern_hierarchy.md -> docs/mindmaps/pattern-hierarchy.md
docs/mindmaps/family_derivation.md -> docs/mindmaps/family-derivation.md
```

---

## Best Practices

1. **Always Use Dry Run First**: Preview changes before executing
2. **Review Mapping Files**: Verify all renames are correct
3. **Commit After Each Step**: Make incremental commits for easier rollback
4. **Verify After Migration**: Run verification script to ensure completeness
5. **Test References**: Check that all links still work after renaming

---

## Related Documentation

- [Documentation Naming Convention](../../contributors/documentation-naming.md) - Naming standard specification
- [Main Tools README](../README.md) - Overview of all tools
- [Documentation Architecture](../../contributors/documentation-architecture.md) - Documentation structure

---

## Troubleshooting

### Old References Still Found

If `verify_all_renames.py` reports old references:

1. Check if the file is in the mapping
2. Run `fix_remaining_references.py`
3. Manually search for the old filename: `git grep "old_filename"`

### Git History Issues

If `git mv` fails:

1. Check if files are tracked by git: `git ls-files`
2. Ensure you're in the repository root
3. Check for uncommitted changes that might conflict

### Special Characters

Files with special characters (e.g., Chinese characters, spaces) may require manual handling. Check `SPECIAL_MAPPINGS` in the script.

---

## Notes

- All scripts use forward slashes (`/`) for paths for cross-platform compatibility
- Scripts preserve git history using `git mv` instead of regular file operations
- Mapping files are excluded from reference updates (they intentionally contain old names)
- README files and `_`-prefixed files are excluded from renaming

