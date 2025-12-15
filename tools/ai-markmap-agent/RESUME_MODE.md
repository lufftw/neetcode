# Resume / Replay Mode Usage Guide

## Overview

Resume mode allows you to continue execution from a previous pipeline run, supporting:
- Reusing completed stage outputs (saves tokens and time)
- Re-running from a specific stage (debug-friendly)
- Not overwriting original run data (generates new regen run)

## Resume vs Reset

**Important distinction:**

- **`--resume`**: Reuses debug outputs from previous runs to save API calls. This is about **pipeline execution** (whether to run new API calls or reuse existing results).

- **`versioning.mode: reset`**: Deletes old version directories and starts fresh. This is about **version management** (how to organize final output versions).

These two features are **independent**:
- You can use `--resume` even when `versioning.mode: reset` is set
- Resume mode reuses debug outputs regardless of versioning mode
- Versioning reset only affects final output directories, not debug outputs
- When resuming, versioning reset prompts are skipped (reset applies to final output only)

## Usage

### Method 1: Interactive Resume Mode

```bash
python main.py --resume
```

After startup, it will:
1. Scan all previous runs under `outputs/debug/`
2. Display them sorted by time (newest first)
3. Let you select the run to resume
4. Ask whether to reuse each stage's output one by one

### Method 2: Start from a Specific Stage

```bash
python main.py --resume --from-stage writer
```

This will automatically:
- Select the latest run
- Reuse outputs from `expert_review`, `full_discussion`, `consensus`
- Re-run from the `writer` stage

Supported stages:
- `expert_review`
- `full_discussion`
- `consensus`
- `writer`
- `translate`
- `post_process`

## Example Workflows

### Scenario 1: Writer has no output, want to re-run

```bash
# 1. List available runs
python main.py --resume

# 2. Select the latest run (e.g., run_20251215_111303)

# 3. Ask whether to reuse each stage:
#    - expert_review: [y] (reuse)
#    - full_discussion: [y] (reuse)
#    - consensus: [y] (reuse)
#    - writer: [n] (regenerate)

# 4. Pipeline will:
#    - Skip expert_review, full_discussion, consensus
#    - Re-run writer
#    - Save output to run_20251215_111303_regen_1/
```

### Scenario 2: Only want to re-run writer

```bash
python main.py --resume --from-stage writer
```

Automatically reuses outputs from all previous stages, only re-runs writer.

## Run Naming Rules

- **Original run**: `run_YYYYMMDD_HHMMSS/`
- **Resume from original run**: `run_YYYYMMDD_HHMMSS_regen_1/`
- **Resume again**: `run_YYYYMMDD_HHMMSS_regen_2/`

**Important**: Original run data is never overwritten, all new outputs are in regen directories.

## State Loading

The system automatically loads:
- ✅ **Consensus data**: Loaded from JSON file (if reusing consensus stage)
- ✅ **Writer output**: Loaded from writer output file (if reusing writer stage)
- ⚠️ **Expert responses**: Currently only marked as reused, incomplete recovery (needs improvement)

## Debug Output

All intermediate outputs (including reused and regenerated ones) are saved in the new regen run directory for easy comparison and debugging.

## Notes

1. **Ensure debug_output.enabled = true**: Resume mode depends on debug output
2. **API Keys**: Still need to provide API keys (even when reusing stages)
3. **Configuration consistency**: Resume uses current config, which may differ from original run
4. **Partial state recovery**: Currently only partial state recovery is supported, some stages may need to be re-run
5. **Versioning mode**: Resume mode works independently of `versioning.mode`:
   - If `versioning.mode: reset`, the reset prompt is skipped during resume
   - Versioning reset only affects final output directories, not debug outputs
   - You can resume from debug outputs even when versioning is set to reset

## Future Improvements

- [ ] Complete state serialization/deserialization
- [ ] Support resuming from any intermediate state
- [ ] Automatically detect failed stages and suggest resume
- [ ] Support comparing outputs from different runs
