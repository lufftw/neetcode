# Create Practice File (`new_practice`)

> **Status**: Informational  
> **Scope**: Creating practice skeleton files in `practices/` via `scripts/new_practice.bat` / `scripts/new_practice.sh`  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

`scripts/new_practice.bat` / `scripts/new_practice.sh` are **thin wrappers** around CodeGen:

- They run `python -m packages.codegen practice ...`
- They forward all arguments as-is
- They return the same exit code as CodeGen

Source: [`scripts/new_practice.bat`](https://github.com/lufftw/neetcode/blob/main/scripts/new_practice.bat)

---

## When to use this

Use this command when you want to **generate or refresh** a practice file:

- Output file location: `practices/`
- Output filename format: `<id:04d>_<slug>.py` (example: `0023_merge_k_sorted_lists.py`)

If the practice file already exists (and you are **not** using `--dry-run`), it will be backed up to:

- `practices/_history/<filename>.<YYYYMMDD_HHMMSS>.bak`

---

## Usage

Run from the repository root.

### Windows

```bash
.\scripts\new_practice.bat <problem_id> [--all-solutions] [--dry-run]
```

### Linux / macOS

```bash
./scripts/new_practice.sh <problem_id> [--all-solutions] [--dry-run]
```

Equivalent direct command (same behavior):

```bash
python -m packages.codegen practice <problem_id> [--all-solutions] [--dry-run]
```

---

## Parameters

### Required

- **`problem_id`** *(int)*: LeetCode problem number (frontend id), e.g. `23`

### Optional flags

- **`--all-solutions`**: If the reference solution contains multiple `Solution` classes, include **all** of them in the generated practice file.  
  - Default behavior (without this flag): include only the **single** practice `Solution`.
- **`--dry-run`**: Print generated content to stdout and **do not write** `practices/<file>.py`.  
  - Important: in dry-run mode, no history backup is created.

---

## What gets generated

CodeGen tries to generate the practice file using one of two strategies:

- **Reuse from an existing reference solution** (preferred): if `solutions/<id>_<slug>.py` exists, CodeGen reuses its imports/helpers/codec infrastructure and only clears the practice implementation.
- **Generate a fresh skeleton**: if no reference solution exists, CodeGen fetches problem metadata (slug/title) and generates a standard skeleton.

---

## Examples

Generate practice file for problem 23:

```bash
.\scripts\new_practice.bat 23
```

Include all solution variants (when the reference has multiple):

```bash
.\scripts\new_practice.bat 23 --all-solutions
```

Preview generated content without writing:

```bash
.\scripts\new_practice.bat 23 --dry-run
```

---

## Troubleshooting

### `python` not found / wrong Python

`new_practice.bat` uses `python` from your PATH. If you have a project virtual environment, activate it first, or run the equivalent `python -m ...` using the correct interpreter.

### "Failed to fetch problem ..."

CodeGen needs the problem slug to compute the filename. If it cannot resolve the slug locally, it may try to fetch it (depending on your DataSource/cache setup). Ensure your environment is configured to access LeetCode data, or generate the reference solution first.

---

## Related docs

- [CodeGen (Package Spec)](../packages/codegen/README.md)
- [Practice Workspace (History/Restore)](../packages/practice_workspace/README.md)


