# Documentation Naming Convention (kebab-case)

> **Status**: Canonical Reference  
> **Scope**: All documentation files across the repository (with explicit exceptions)  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

---

## Purpose

Standardize documentation filenames to **kebab-case** (e.g., `memory-profiling.md`) to improve readability, cross-platform consistency, and link stability.

---

## Applies To

### ✅ Included
- All documentation-like files, especially Markdown: `*.md`
- Documentation under directories such as:
  - `docs/`
  - `tools/**/docs/`
  - `meta/**` (see exceptions for special-role files)

### ❌ Explicit Exceptions (Do NOT rename)
These filenames are intentionally preserved for ecosystem compatibility or routing semantics:

1. **README variants**
   - `README.md`
   - `README_zh-TW.md`

2. **Index entrypoints (routing / site entry)**
   - `index.md`
   - `index_zh-TW.md` (or any `index_*.md` used by the site)

3. **System role marker files (leading underscore)**
   - Files starting with `_` (e.g., `_header.md`, `_templates.md`)
   - Rationale: the underscore conveys a special role and may be referenced by build scripts or conventions.

---

## Naming Rules

### 1) Format
- **lowercase only**
- Words separated by a single hyphen `-`
- **ASCII characters only**
- No spaces
- No underscores `_` (except leading-underscore role files, which are excluded)

✅ Good:
- `memory-profiling.md`
- `github-pages-setup.md`
- `documentation-header-spec.md`

❌ Bad:
- `Memory_Profiling.md`
- `GITHUB_PAGES_SETUP.md`
- `writer behavior.md`
- `writer_behavior.md`
- `writer_behavior - copy.md`

---

## Version & Suffix Rules

### 2) Version suffix
Preserve version markers but normalize separators and casing:

✅ Recommended:
- `design-v2.md`
- `design-v3.md`
- `design-v4.md`

❌ Avoid:
- `DESIGN_V4.md`
- `Design-v4.md` (mixed case)

---

## Acronyms & Proper Nouns

### 3) Acronyms
Acronyms should be **lowercased** in filenames to maintain consistency.

✅ Recommended:
- `cli-output-contract.md`
- `mkdocs-content-guide.md`
- `vscode-setup.md`

---

## Examples

### 4) Common conversions

| Before | After |
|------|------|
| `docs/ARCHITECTURE_MIGRATION.md` | `docs/architecture-migration.md` |
| `docs/GITHUB_PAGES_SETUP.md` | `docs/github-pages-setup.md` |
| `docs/runner/benchmarking/Memory_Metrics.md` | `docs/runner/benchmarking/memory-metrics.md` |
| `docs/runner/profiling/Cli_Output_Memory.md` | `docs/runner/profiling/cli-output-memory.md` |
| `meta/patterns/.../_header.md` | **UNCHANGED** (excluded: leading `_`) |

---

## Migration Principles

### 5) Reference integrity (must not break)
When renaming a file:
- Use `git mv` (never rename via a file explorer)
- Update **all references**, including:
  - Markdown links
  - Documentation site configs (MkDocs / Astro / VitePress)
  - Scripts, code comments, tests
  - Generated documentation pointers

### 6) Acceptance criteria
- All applicable documentation filenames follow kebab-case
- Repo-wide search for old filenames yields **zero results**
- Documentation build passes with **no broken link errors/warnings** (when applicable)

---

## Recommended Workflow

1. Create a mapping table: `old_name -> new_name`
2. Rename using `git mv`
3. Update references via repo-wide search
4. Run documentation build / link checks (if available)
5. Commit in a single focused PR (or a small set of atomic PRs)

---

## Step-by-Step Operation Guide

This guide uses the automated script `tools/doc-naming/rename_docs_to_kebab_case.py` to perform the migration safely.

### Prerequisites

- Python 3.7+ installed
- Git repository in clean state (no uncommitted changes)
- MkDocs installed (for final verification)

### Step 1: Review the Mapping Table

Generate and review the rename mapping before execution:

```bash
python tools/doc-naming/rename_docs_to_kebab_case.py --dry-run
```

This will:
- Scan all `.md` files (excluding README, index, and `_`-prefixed files)
- Generate `rename_mapping.txt` and `rename_mapping.json` in the repository root
- Display the mapping table without making any changes

**Review checklist:**
- ✅ Check `rename_mapping.txt` for any unexpected conversions
- ✅ Verify special mappings (e.g., `writer_behavior - 預備.md` → `writer-behavior-delete.md`)
- ✅ Ensure no collisions (same target filename from different sources)
- ✅ Confirm excluded files are not in the mapping

### Step 2: Execute the Renaming

Once the mapping is approved, execute the full migration:

```bash
python tools/doc-naming/rename_docs_to_kebab_case.py
```

This will:
1. **Rename files** using `git mv` (preserves Git history)
2. **Update references** in:
   - Markdown links: `[text](path/to/old_name.md)`
   - YAML configs: `mkdocs.yml` navigation entries
   - Python/JSON/TOML files: string literals and comments
   - All file types: `.md`, `.yml`, `.yaml`, `.py`, `.txt`, `.json`, `.toml`
3. **Generate reports**: Shows which files were renamed and updated

**Important notes:**
- The script uses forward slashes (`/`) for all paths (cross-platform compatible)
- Collision detection prevents duplicate target filenames
- All paths are normalized before processing

### Step 3: Verify Old References Are Gone

Check that no old filenames remain in the repository:

```bash
# Option 1: Automated verification (recommended)
# Checks all renamed files and reports which ones still have old references
python tools/verify_all_renames.py

# Option 2: Manual verification with git grep
git grep -l "ACT_LOCAL_GITHUB_ACTIONS.md" || echo "No old references found"
git grep -l "VSCODE_SETUP.md" || echo "No old references found"
git grep -l "SOLUTION_CONTRACT.md" || echo "No old references found"

# Option 3: Use the main script's verification mode
python tools/doc-naming/rename_docs_to_kebab_case.py --verify-only
```

**Expected output from `verify_all_renames.py`:**
```
✓ ACT_LOCAL_GITHUB_ACTIONS.md                    → No old references found
✓ VSCODE_SETUP.md                                → No old references found
✓ SOLUTION_CONTRACT.md                           → No old references found
...
✓ SUCCESS: All renamed files have no old references remaining!
```

**Expected result:** Zero matches for old filenames.

### Step 4: Build Documentation Site

Verify that the documentation site builds without errors:

```bash
mkdocs build --strict
```

**Check for:**
- ✅ No broken link warnings
- ✅ No missing file errors
- ✅ Navigation structure intact
- ✅ All pages render correctly

### Step 5: Manual Spot Checks

Perform manual verification:

1. **Check key files:**
   ```bash
   # Verify mkdocs.yml was updated
   git diff mkdocs.yml
   
   # Check a few renamed files exist
   ls docs/act-local-github-actions.md
   ls docs/contributors/vscode-setup.md
   ```

2. **Test a few links:**
   - Open `docs/contributors/documentation-naming.md`
   - Verify internal links work
   - Check that referenced files exist

3. **Review git status:**
   ```bash
   git status
   # Should show renamed files and updated reference files
   ```

### Step 6: Commit Changes

Once all verifications pass:

```bash
# Review all changes
git diff --staged

# Commit with descriptive message
git commit -m "chore(docs): standardize filenames to kebab-case (except README and index)"
```

### Troubleshooting

#### Issue: Script reports collisions

**Solution:** The script will skip colliding files and print warnings. Manually resolve collisions by:
1. Reviewing `rename_mapping.txt` for duplicate targets
2. Adjusting `SPECIAL_MAPPINGS` in the script if needed
3. Re-running the dry-run to verify

#### Issue: `git mv` fails on Windows

**Solution:** The script normalizes paths to forward slashes. If issues persist:
- Use Git Bash instead of PowerShell/CMD
- Ensure Git is up to date
- Check file permissions

#### Issue: References not updated in some files

**Solution:** The script searches common file types. If a file type is missed:
1. Manually search: `git grep "OLD_FILENAME.md"`
2. Update references manually
3. Consider adding the file extension to `search_extensions` in the script

#### Issue: MkDocs build fails

**Solution:**
1. Check `mkdocs.yml` syntax: `mkdocs build --strict`
2. Verify all navigation paths use forward slashes
3. Check for typos in updated paths
4. Review build logs for specific file errors

### Script Features

The `tools/doc-naming/rename_docs_to_kebab_case.py` script includes:

- **Automatic kebab-case conversion**: Handles underscores, spaces, CamelCase, and acronyms
- **Collision detection**: Prevents duplicate target filenames
- **Path normalization**: Uses forward slashes (`/`) for cross-platform compatibility
- **Comprehensive reference updates**: Updates Markdown links, YAML configs, code strings, and comments
- **Git history preservation**: Uses `git mv` for all renames
- **Dry-run mode**: Safe preview before execution
- **Verification mode**: Post-migration checks for remaining old references

### Future Maintenance

The script can be reused for:
- **Auditing**: Run `--dry-run` periodically to check for new non-kebab-case files
- **Incremental updates**: Add new files to `SPECIAL_MAPPINGS` as needed
- **Reference verification**: Use `--verify-only` to check for broken references

---

## Branch & Commit

### Branch name
- `chore/docs-kebab-case-naming`

### Commit message
- `chore(docs): standardize filenames to kebab-case (except README and index)`

---

## FAQ

**Q: Why exclude `index.md`?**  
A: Many static site generators treat `index.md` as a routing entrypoint. Renaming it may break navigation.

**Q: Why exclude files starting with `_`?**  
A: Leading underscores denote special system roles (partials/templates/metadata). Renaming them may break implicit conventions or scripts.

---

```bash
$ git ls-files '*.md' | grep -v '^README' | grep -v 'README\.md$' | grep -v 'README_zh-TW\.md$'
```

```
docs/act-local-github-actions.md
docs/architecture-migration.md
docs/build-docs-manual.md
docs/documentation-header-spec.md
docs/generator-contract.md
docs/github-pages-setup.md
docs/local-docs-build.md
docs/mkdocs-content-guide.md
docs/ontology-design.md
docs/solution-contract.md
docs/contributors/documentation-architecture.md
docs/contributors/testing.md
docs/contributors/virtual-env-setup.md
docs/contributors/vscode-setup.md
docs/index.md
docs/index_zh-TW.md
docs/mindmaps/index.md
docs/mindmaps/neetcode_ontology_agent_evolved_en.md
docs/mindmaps/neetcode_ontology_agent_evolved_zh-TW.md
docs/mindmaps/neetcode_ontology_ai_en.md
docs/mindmaps/neetcode_ontology_ai_zh-TW.md
docs/patterns/backtracking_exploration/intuition.md
docs/patterns/backtracking_exploration/templates.md
docs/patterns/sliding_window/intuition.md
docs/patterns/sliding_window/templates.md
docs/patterns/two_pointers/intuition.md
docs/patterns/two_pointers/templates.md
docs/runner/CLI_OUTPUT_CONTRACT.md
docs/runner/benchmarking/Memory_Metrics.md
docs/runner/profiling/Cli_Output_Memory.md
docs/runner/profiling/Input_Scale_Metrics.md
meta/patterns/backtracking_exploration/0039_combination_sum.md
meta/patterns/backtracking_exploration/0040_combination_sum_ii.md
meta/patterns/backtracking_exploration/0046_permutations.md
meta/patterns/backtracking_exploration/0047_permutations_duplicates.md
meta/patterns/backtracking_exploration/0051_n_queens.md
meta/patterns/backtracking_exploration/0077_combinations.md
meta/patterns/backtracking_exploration/0078_subsets.md
meta/patterns/backtracking_exploration/0079_word_search.md
meta/patterns/backtracking_exploration/0090_subsets_duplicates.md
meta/patterns/backtracking_exploration/0093_restore_ip.md
meta/patterns/backtracking_exploration/0131_palindrome_partitioning.md
meta/patterns/backtracking_exploration/0216_combination_sum_iii.md
meta/patterns/backtracking_exploration/_comparison.md
meta/patterns/backtracking_exploration/_decision.md
meta/patterns/backtracking_exploration/_deduplication.md
meta/patterns/backtracking_exploration/_header.md
meta/patterns/backtracking_exploration/_mapping.md
meta/patterns/backtracking_exploration/_pruning.md
meta/patterns/backtracking_exploration/_templates.md
meta/patterns/sliding_window/0003_base.md
meta/patterns/sliding_window/0076_min_window.md
meta/patterns/sliding_window/0209_min_subarray.md
meta/patterns/sliding_window/0340_k_distinct.md
meta/patterns/sliding_window/0438_anagrams.md
meta/patterns/sliding_window/0567_permutation.md
meta/patterns/sliding_window/_comparison.md
meta/patterns/sliding_window/_decision.md
meta/patterns/sliding_window/_header.md
meta/patterns/sliding_window/_templates.md
meta/patterns/two_pointers/_comparison.md
meta/patterns/two_pointers/_decision.md
meta/patterns/two_pointers/_header.md
meta/patterns/two_pointers/_mapping.md
meta/patterns/two_pointers/_templates.md
tools/ai-markmap-agent/docs/DATA_SOURCES.md
tools/ai-markmap-agent/docs/DESIGN.md
tools/ai-markmap-agent/docs/DESIGN_V2.md
tools/ai-markmap-agent/docs/DESIGN_V3.md
tools/ai-markmap-agent/docs/DESIGN_V4.md
tools/ai-markmap-agent/docs/POST_PROCESSING_LINKS.md
tools/ai-markmap-agent/docs/POST_PROCESSING_SOLUTION_LINKS.md
tools/ai-markmap-agent/docs/PROMPTS.md
tools/ai-markmap-agent/docs/WORKFLOW_PROCESSING_ORDER.md
tools/ai-markmap-agent/outputs/versions/v1/neetcode_ontology_agent_evolved_zh-TW.md  
tools/ai-markmap-agent/prompts/compressor/compressor_behavior.md
tools/ai-markmap-agent/prompts/evaluators/content_evaluator_behavior.md
tools/ai-markmap-agent/prompts/evaluators/structure_evaluator_behavior.md
tools/ai-markmap-agent/prompts/experts/architect_behavior.md
tools/ai-markmap-agent/prompts/experts/architect_persona.md
tools/ai-markmap-agent/prompts/experts/discussion_behavior.md
tools/ai-markmap-agent/prompts/experts/engineer_behavior.md
tools/ai-markmap-agent/prompts/experts/engineer_persona.md
tools/ai-markmap-agent/prompts/experts/professor_behavior.md
tools/ai-markmap-agent/prompts/experts/professor_persona.md
tools/ai-markmap-agent/prompts/generators/generalist_behavior.md
tools/ai-markmap-agent/prompts/generators/generalist_persona.md
tools/ai-markmap-agent/prompts/generators/specialist_behavior.md
tools/ai-markmap-agent/prompts/generators/specialist_persona.md
tools/ai-markmap-agent/prompts/integrator/integrator_behavior.md
tools/ai-markmap-agent/prompts/integrator/integrator_persona.md
tools/ai-markmap-agent/prompts/judges/judge_completeness_behavior.md
tools/ai-markmap-agent/prompts/judges/judge_completeness_persona.md
tools/ai-markmap-agent/prompts/judges/judge_quality_behavior.md
tools/ai-markmap-agent/prompts/judges/judge_quality_persona.md
tools/ai-markmap-agent/prompts/meta/generate_optimizer_behavior.md
tools/ai-markmap-agent/prompts/meta/generate_optimizer_persona.md
tools/ai-markmap-agent/prompts/meta/suggest_optimizer_roles.md
tools/ai-markmap-agent/prompts/optimizers/optimizer_apidesigner_behavior.md
tools/ai-markmap-agent/prompts/optimizers/optimizer_apidesigner_persona.md
tools/ai-markmap-agent/prompts/optimizers/optimizer_architect_behavior.md
tools/ai-markmap-agent/prompts/optimizers/optimizer_architect_persona.md
tools/ai-markmap-agent/prompts/optimizers/optimizer_professor_behavior.md
tools/ai-markmap-agent/prompts/optimizers/optimizer_professor_persona.md
tools/ai-markmap-agent/prompts/planners/generalist_planner_behavior.md
tools/ai-markmap-agent/prompts/planners/generalist_planner_persona.md
tools/ai-markmap-agent/prompts/planners/specialist_planner_behavior.md
tools/ai-markmap-agent/prompts/planners/specialist_planner_persona.md
tools/ai-markmap-agent/prompts/strategists/architect_strategist_behavior.md
tools/ai-markmap-agent/prompts/strategists/architect_strategist_persona.md
tools/ai-markmap-agent/prompts/strategists/professor_strategist_behavior.md
tools/ai-markmap-agent/prompts/strategists/professor_strategist_persona.md
tools/ai-markmap-agent/prompts/strategists/ux_strategist_behavior.md
tools/ai-markmap-agent/prompts/strategists/ux_strategist_persona.md
tools/ai-markmap-agent/prompts/summarizer/summarizer_behavior.md
tools/ai-markmap-agent/prompts/summarizer/summarizer_persona.md
tools/ai-markmap-agent/prompts/translator/generic_translator_behavior.md
tools/ai-markmap-agent/prompts/translator/zh_tw_translator_behavior.md
tools/ai-markmap-agent/prompts/writer/markmap_format_guide.md
"tools/ai-markmap-agent/prompts/writer/writer_behavior - \350\244\207\350\243\275.md"
tools/ai-markmap-agent/prompts/writer/writer_behavior.md
tools/ai-markmap-agent/prompts/writer/writer_behavior_v3.md
tools/ai-markmap-agent/prompts/writer/writer_persona.md
tools/html_meta_description_generator.md
tools/html_meta_description_generator_zh-TW.md
tools/leetcode_api_discussion.md
tools/prompts/generated/mindmap_prompt.md
tools/prompts/system_prompt.md
tools/verify_integration.md
```

## Changelog
- **2025-12-26**: Initial version
- **2025-12-26**: Added step-by-step operation guide for `tools/doc-naming/rename_docs_to_kebab_case.py`
