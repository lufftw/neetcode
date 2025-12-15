# =============================================================================
# Resume / Replay Module
# =============================================================================
# Allows resuming or replaying from previous pipeline runs.
# Supports partial reruns (from specific stages) and reusing outputs.
# =============================================================================

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

# Imports handled lazily to avoid circular dependencies


class RunInfo:
    """Information about a previous pipeline run."""
    
    def __init__(self, run_dir: Path):
        self.run_dir = run_dir
        self.run_id = run_dir.name
        self.timestamp = self._parse_timestamp()
        self.files = self._scan_files()
    
    def _parse_timestamp(self) -> datetime | None:
        """Parse timestamp from run_id (run_YYYYMMDD_HHMMSS)."""
        try:
            parts = self.run_id.split("_")
            if len(parts) >= 3:
                date_str = parts[1]  # YYYYMMDD
                time_str = parts[2]  # HHMMSS
                dt_str = f"{date_str}_{time_str}"
                return datetime.strptime(dt_str, "%Y%m%d_%H%M%S")
        except (ValueError, IndexError):
            pass
        return None
    
    def _scan_files(self) -> dict[str, dict[str, Any]]:
        """Scan files in run directory and categorize by phase."""
        files_by_phase = {
            "expert_review": [],
            "full_discussion": [],
            "consensus": [],
            "writer": [],
            "translation": [],
            "post_processing": [],
            "llm_input": [],
            "llm_output": [],
        }
        
        if not self.run_dir.exists():
            return files_by_phase
        
        for file_path in self.run_dir.iterdir():
            if not file_path.is_file():
                continue
            
            filename = file_path.name
            size = file_path.stat().st_size
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            
            file_info = {
                "path": file_path,
                "filename": filename,
                "size": size,
                "size_str": self._format_size(size),
                "mtime": mtime,
                "mtime_str": mtime.strftime("%Y-%m-%d %H:%M:%S"),
            }
            
            # Categorize file - precise pattern matching
            filename_lower = filename.lower()
            
            # Expert review: llm_input/output with invoke or review, for expert agents
            if filename.startswith("llm_input_") or filename.startswith("llm_output_"):
                if "invoke" in filename_lower or "review" in filename_lower:
                    # Check if it's an expert agent
                    if any(expert in filename_lower for expert in ["architect", "professor", "engineer", "optimizer"]):
                        files_by_phase["expert_review"].append(file_info)
                elif "discuss" in filename_lower:
                    # Check if it's an expert agent
                    if any(expert in filename_lower for expert in ["architect", "professor", "engineer", "optimizer"]):
                        files_by_phase["full_discussion"].append(file_info)
                elif "writer" in filename_lower:
                    files_by_phase["writer"].append(file_info)
                elif "translator" in filename_lower or "translation" in filename_lower:
                    files_by_phase["translation"].append(file_info)
                else:
                    # Generic LLM input/output (add to both lists for backward compatibility)
                    files_by_phase["llm_input"].append(file_info)
                    if filename.startswith("llm_output_"):
                        files_by_phase["llm_output"].append(file_info)
            elif "consensus" in filename_lower:
                files_by_phase["consensus"].append(file_info)
            elif "writer" in filename_lower:
                files_by_phase["writer"].append(file_info)
            elif "translation" in filename_lower or "translator" in filename_lower:
                files_by_phase["translation"].append(file_info)
            elif "postproc" in filename_lower or "post_processing" in filename_lower:
                files_by_phase["post_processing"].append(file_info)
        
        return files_by_phase
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def has_stage_output(self, stage: str) -> bool:
        """Check if this run has output for a specific stage."""
        # Check directly by stage name (files are categorized by stage)
        stage_files = self.files.get(stage, [])
        return len(stage_files) > 0
    
    def get_stage_files(self, stage: str) -> list[dict[str, Any]]:
        """Get files for a specific stage."""
        # Return files categorized for this specific stage
        return self.files.get(stage, [])


def scan_previous_runs(debug_output_dir: Path) -> list[RunInfo]:
    """
    Scan for previous pipeline runs.
    
    Args:
        debug_output_dir: Path to debug outputs directory
        
    Returns:
        List of RunInfo objects, sorted by timestamp (oldest first)
    """
    if not debug_output_dir.exists():
        return []
    
    runs = []
    for item in debug_output_dir.iterdir():
        if item.is_dir() and item.name.startswith("run_") and not item.name.endswith("_regen_"):
            # Skip regeneration runs (they will be handled separately)
            runs.append(RunInfo(item))
    
    # Sort by timestamp (oldest first) - so newest prints at the bottom
    runs.sort(key=lambda r: r.timestamp or datetime.min, reverse=False)
    
    return runs


def select_run_interactive(runs: list[RunInfo]) -> RunInfo | None:
    """
    Interactive selection of a previous run.
    
    Args:
        runs: List of available runs
        
    Returns:
        Selected RunInfo, or None if cancelled
    """
    if not runs:
        print("\n  ⚠ No previous runs found")
        return None
    
    print("\n" + "=" * 60)
    print("Available Previous Runs (oldest to newest)")
    print("=" * 60)
    
    for i, run in enumerate(runs, 1):
        timestamp_str = run.timestamp.strftime("%Y-%m-%d %H:%M:%S") if run.timestamp else "Unknown"
        file_count = sum(len(files) for files in run.files.values())
        is_latest = (i == len(runs))  # Last one is newest
        marker = " ← Latest" if is_latest else ""
        print(f"\n[{i}] {run.run_id}{marker}")
        print(f"    Last modified: {timestamp_str}")
        print(f"    Files: {file_count} total")
        
        # Show stage completion
        stages = ["expert_review", "full_discussion", "consensus", "writer", "translation", "post_processing"]
        completed = [s for s in stages if run.has_stage_output(s)]
        if completed:
            print(f"    Completed stages: {', '.join(completed)}")
    
    print()
    
    while True:
        try:
            choice = input(f"Select a run (1-{len(runs)}, or 'q' to cancel): ").strip()
            
            if choice.lower() == 'q':
                return None
            
            idx = int(choice) - 1
            if 0 <= idx < len(runs):
                return runs[idx]
            else:
                print(f"  ⚠ Invalid choice. Please enter 1-{len(runs)} or 'q'")
        except ValueError:
            print("  ⚠ Invalid input. Please enter a number or 'q'")
        except KeyboardInterrupt:
            print("\n\n  ⚠ Cancelled")
            return None


def ask_reuse_stage(stage: str, run_info: RunInfo) -> bool:
    """
    Ask user whether to reuse output from a specific stage.
    
    Args:
        stage: Stage name
        run_info: Run information
        
    Returns:
        True to reuse, False to regenerate
    """
    files = run_info.get_stage_files(stage)
    
    if not files:
        return False  # No files to reuse
    
    print(f"\n  Stage: {stage}")
    print(f"  Existing output found:")
    
    for file_info in files[:3]:  # Show up to 3 files
        print(f"    - {file_info['filename']}")
        print(f"      Size: {file_info['size_str']}")
        print(f"      Modified: {file_info['mtime_str']}")
    
    if len(files) > 3:
        print(f"    ... and {len(files) - 3} more files")
    
    while True:
        choice = input(f"  Reuse this output? [y/N]: ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no', '']:
            return False
        else:
            print("  ⚠ Please enter 'y' or 'n'")


def load_consensus_from_run(run_info: RunInfo) -> dict[str, Any] | None:
    """Load consensus data from a previous run."""
    # Look for consensus JSON files
    consensus_files = [
        f for f in run_info.files.get("consensus", [])
        if f["filename"].endswith(".json")
    ]
    
    if not consensus_files:
        # Try to find any consensus file
        consensus_files = run_info.files.get("consensus", [])
    
    if not consensus_files:
        return None
    
    # Use the most recent consensus file
    latest = max(consensus_files, key=lambda f: f["mtime"])
    
    try:
        content = latest["path"].read_text(encoding="utf-8")
        return json.loads(content)
    except Exception as e:
        print(f"  ⚠ Error loading consensus: {e}")
        return None


def load_expert_responses_from_run(run_info: RunInfo) -> dict[str, dict[str, str]] | None:
    """
    Load expert responses from LLM output files.
    
    Returns:
        Dict with structure:
        {
            "expert_review": {"architect": "...", "professor": "...", ...},
            "full_discussion": {"architect": "...", ...}
        }
    """
    expert_review_outputs = {}
    discussion_outputs = {}
    
    # Scan expert_review files (llm_output_*_invoke.md)
    for file_info in run_info.files.get("expert_review", []):
        filename = file_info["filename"]
        
        # Only process llm_output files (skip llm_input)
        if not filename.startswith("llm_output_"):
            continue
        
        # Parse filename: llm_output_{agent}_{action}.md
        parts = filename.replace("llm_output_", "").replace(".md", "").split("_")
        
        if len(parts) >= 2:
            action = parts[-1]  # "invoke"
            agent = "_".join(parts[:-1])  # "architect", "professor", etc.
            
            try:
                content = file_info["path"].read_text(encoding="utf-8")
                expert_review_outputs[agent] = content
            except Exception as e:
                print(f"  ⚠ Error loading {filename}: {e}")
    
    # Scan full_discussion files (llm_output_*_discuss.md)
    for file_info in run_info.files.get("full_discussion", []):
        filename = file_info["filename"]
        
        # Only process llm_output files (skip llm_input)
        if not filename.startswith("llm_output_"):
            continue
        
        # Parse filename: llm_output_{agent}_{action}.md
        parts = filename.replace("llm_output_", "").replace(".md", "").split("_")
        
        if len(parts) >= 2:
            action = parts[-1]  # "discuss"
            agent = "_".join(parts[:-1])  # "architect", "professor", etc.
            
            try:
                content = file_info["path"].read_text(encoding="utf-8")
                discussion_outputs[agent] = content
            except Exception as e:
                print(f"  ⚠ Error loading {filename}: {e}")
    
    result = {}
    if expert_review_outputs:
        result["expert_review"] = expert_review_outputs
    if discussion_outputs:
        result["full_discussion"] = discussion_outputs
    
    return result if result else None


def load_writer_output_from_run(run_info: RunInfo) -> str | None:
    """Load writer output from a previous run."""
    # Look for writer output files
    writer_files = [
        f for f in run_info.files.get("writer", [])
        if "writer_output" in f["filename"] or "llm_output_writer" in f["filename"]
    ]
    
    if not writer_files:
        return None
    
    # Use the most recent writer output
    latest = max(writer_files, key=lambda f: f["mtime"])
    
    try:
        return latest["path"].read_text(encoding="utf-8")
    except Exception as e:
        print(f"  ⚠ Error loading writer output: {e}")
        return None


def load_translation_outputs_from_run(run_info: RunInfo) -> dict[str, str] | None:
    """
    Load translation outputs from a previous run.
    
    Returns:
        Dict mapping target_key to translated content, e.g.:
        {"general_zh-TW": "...", "pattern_zh-TW": "..."}
    """
    # Look for translation result files (after translation, not before)
    translation_files = [
        f for f in run_info.files.get("translation", [])
        if "translation_result" in f["filename"]
    ]
    
    if not translation_files:
        return None
    
    translated_outputs = {}
    
    # Parse each translation file to extract target_key and content
    for file_info in translation_files:
        filename = file_info["filename"]
        
        # Extract target_key from filename
        # Format: 05_translation_result_{target_key}_{timestamp}.md
        # Example: 05_translation_result_general_zh-TW_143022.md
        try:
            # Remove extension
            name_without_ext = filename.replace(".md", "").replace(".json", "")
            
            # Split by underscore
            parts = name_without_ext.split("_")
            
            # Find "translation_result" and get everything after it
            if "translation_result" in parts:
                idx = parts.index("translation_result")
                # Get all parts after "translation_result"
                key_parts = parts[idx + 1:]
                
                # Remove timestamp if present (last part if it's 6 digits)
                if key_parts and len(key_parts[-1]) == 6 and key_parts[-1].isdigit():
                    key_parts = key_parts[:-1]
                
                if key_parts:
                    target_key = "_".join(key_parts)
                    
                    # Read content
                    content = file_info["path"].read_text(encoding="utf-8")
                    translated_outputs[target_key] = content
        except Exception as e:
            print(f"  ⚠ Error loading translation file {filename}: {e}")
            continue
    
    return translated_outputs if translated_outputs else None


def generate_regen_run_id(original_run_id: str) -> str:
    """
    Generate a regeneration run ID from an original run ID.
    
    Args:
        original_run_id: Original run ID (e.g., "run_20251215_111303")
        
    Returns:
        New run ID (e.g., "run_20251215_111303_regen_1")
    """
    base_dir = Path(__file__).parent.parent.parent / "outputs" / "debug"
    
    # Find existing regen runs
    existing_regen = []
    if base_dir.exists():
        for item in base_dir.iterdir():
            if item.is_dir() and item.name.startswith(f"{original_run_id}_regen_"):
                existing_regen.append(item.name)
    
    # Determine next regen number
    regen_num = 1
    if existing_regen:
        # Extract numbers and find max
        numbers = []
        for name in existing_regen:
            try:
                num = int(name.split("_regen_")[-1])
                numbers.append(num)
            except (ValueError, IndexError):
                pass
        
        if numbers:
            regen_num = max(numbers) + 1
    
    return f"{original_run_id}_regen_{regen_num}"

