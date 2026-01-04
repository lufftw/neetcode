# Create New Problem (`new_problem`)

> **Status**: Informational  
> **Scope**: Creating solution skeleton files in `solutions/` via `scripts/new_problem.bat` / `scripts/new_problem.sh`  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

`scripts/new_problem.bat` / `scripts/new_problem.sh` are **thin wrappers** around CodeGen:

- They run `python -m codegen new ...`
- They forward all arguments as-is
- They return the same exit code as CodeGen

---

## When to use this

Use this when you want to **create a new reference solution skeleton** for a LeetCode problem:

- Output directory: `solutions/`
- Output filename format: `<id:04d>_<slug>.py` (example: `0001_two_sum.py`)

If the solution file already exists, CodeGen will **refuse to overwrite** (unless you delete it and regenerate).

---

## Usage

Run from the repository root.

### Windows

```bash
.\scripts\new_problem.bat <problem_id> [options]
```

### Linux / macOS

```bash
./scripts/new_problem.sh <problem_id> [options]
```

### Equivalent direct command (same behavior)

```bash
python -m codegen new <problem_id> [options]
```

---

## Parameters

### Required

- **`problem_id`** *(int)*: LeetCode problem number (frontend id), e.g. `1`

### Optional flags

- **`--with-tests`**: Generate `.in`/`.out` test files from LeetCode examples (under `tests/`).
- **`--force`**: Overwrite existing test files *(only applies with `--with-tests`)*.
- **`--dry-run`**: Print generated content to stdout and **do not write** files.
- **`--solve-mode {placeholder,infer,tiered}`**:
  - `placeholder`: TODO-style `solve()`
  - `infer`: auto-generate `solve()` based on inferred I/O schema
  - `tiered`: config-based Tier-1 / Tier-1.5 `solve()` generation (codec-based)
- **`--codec-mode {import,inline}`**: Override codec emission strategy for tiered solve generation (default: from `config/problem-support.yaml`)
- **`--header-level {minimal,standard,full}`**: Controls the amount of problem header content (default: `full`)

---

## Tiered auto-detection (Tier-1 / Tier-1.5)

Even if you do **not** pass `--solve-mode tiered`, CodeGen will **auto-use tiered solve generation** when the problem is marked as Tier `"1"` or `"1.5"` in:

- `config/problem-support.yaml`

This is what enables correct handling for structures like ListNode / TreeNode / cycles via the codec layer.

### Codec mode (import vs inline)

Tiered generation supports two codec emission strategies:

- **import**: `solve()` imports codec utilities from `runner.utils.codec`
- **inline**: codec utilities are embedded into the generated solution file

Default behavior is controlled by **problem config** (`codec_mode` in `config/problem-support.yaml`).
You can override it for a single run via `--codec-mode`.

---

## Examples

Generate a new solution skeleton:

```bash
.\scripts\new_problem.bat 1
```

Generate solution skeleton + LeetCode example tests:

```bash
.\scripts\new_problem.bat 1 --with-tests
```

Generate with auto-inferred `solve()`:

```bash
.\scripts\new_problem.bat 1 --solve-mode infer
```

Preview without writing:

```bash
.\scripts\new_problem.bat 1 --with-tests --dry-run
```

---

## Related docs

- [CodeGen (Package Spec)](../packages/codegen/README.md)
- [Problem Support Boundary](../contracts/problem-support-boundary.md)
- [Test File Format](../contracts/test-file-format.md)


