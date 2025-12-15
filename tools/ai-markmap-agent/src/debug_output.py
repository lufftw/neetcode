# =============================================================================
# Debug Output Module
# =============================================================================
# Saves intermediate outputs from each phase for debugging and verification.
# =============================================================================

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class DebugOutputManager:
    """
    Manages debug output saving for each phase of the pipeline.
    
    Saves intermediate outputs to help with debugging and verification.
    """
    
    def __init__(self, config: dict[str, Any] | None = None, run_dir: Path | str | None = None):
        """
        Initialize the debug output manager.
        
        Args:
            config: Configuration dictionary
            run_dir: Optional run directory path (for resume mode).
                     If provided, uses this directory instead of creating new one.
        """
        from .config_loader import ConfigLoader
        
        config = config or ConfigLoader.get_config()
        debug_config = config.get("debug_output", {})
        
        self.enabled = debug_config.get("enabled", False)
        self.output_dir = Path(debug_config.get("output_dir", "outputs/debug"))
        self.phases_config = debug_config.get("phases", {})
        self.format_config = debug_config.get("format", {})
        
        # Create output directory if enabled
        if self.enabled:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            if run_dir:
                # Resume mode: use existing run directory
                self.run_dir = Path(run_dir)
                if not self.run_dir.exists():
                    self.run_dir.mkdir(parents=True, exist_ok=True)
                print(f"  📁 Debug outputs (resume): {self.run_dir}")
            else:
                # New run: create run-specific directory with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.run_dir = self.output_dir / f"run_{timestamp}"
                self.run_dir.mkdir(parents=True, exist_ok=True)
                print(f"  📁 Debug outputs: {self.run_dir}")
    
    def _get_filename(
        self,
        phase_num: int,
        phase: str,
        agent: str = "",
        lang: str = "",
        extra: str = "",
    ) -> str:
        """Generate filename based on config template."""
        include_timestamp = self.format_config.get("include_timestamp", True)
        include_phase_num = self.format_config.get("include_phase_number", True)
        
        parts = []
        
        if include_phase_num:
            parts.append(f"{phase_num:02d}")
        
        parts.append(phase)
        
        if agent:
            parts.append(agent)
        
        if lang:
            parts.append(lang)
        
        if extra:
            parts.append(extra)
        
        if include_timestamp:
            parts.append(datetime.now().strftime("%H%M%S"))
        
        return "_".join(parts)
    
    def save(
        self,
        phase_num: int,
        phase: str,
        content: str | dict | list,
        agent: str = "",
        lang: str = "",
        extra: str = "",
        extension: str = "md",
    ) -> Path | None:
        """
        Save debug output.
        
        Args:
            phase_num: Phase number (1-7)
            phase: Phase name (baseline, optimization, judging, etc.)
            content: Content to save (string, dict, or list)
            agent: Agent name (optional)
            lang: Language (optional)
            extra: Extra identifier (optional)
            extension: File extension (md or json)
            
        Returns:
            Path to saved file, or None if not enabled
        """
        if not self.enabled:
            return None
        
        # Check if this phase is enabled
        phase_config = self.phases_config.get(phase, {})
        if not phase_config.get("enabled", False):
            return None
        
        # Generate filename
        filename = self._get_filename(phase_num, phase, agent, lang, extra)
        filepath = self.run_dir / f"{filename}.{extension}"
        
        # Convert content to string if needed
        if isinstance(content, (dict, list)):
            content_str = json.dumps(content, indent=2, ensure_ascii=False)
            if extension == "md":
                extension = "json"
                filepath = self.run_dir / f"{filename}.json"
        else:
            content_str = content
        
        # Save file
        filepath.write_text(content_str, encoding="utf-8")
        print(f"    💾 Saved: {filepath.name}")
        
        return filepath
    
    # =========================================================================
    # Phase-specific save methods
    # =========================================================================
    
    def save_baseline(
        self,
        content: str,
        generator: str,
        lang: str,
    ) -> Path | None:
        """Save Phase 1 baseline output."""
        config = self.phases_config.get("baseline", {})
        if not config.get("save_each_generator", False):
            return None
        return self.save(1, "baseline", content, generator, lang)
    
    def save_optimization_round(
        self,
        content: str,
        round_num: int,
        output_key: str,
    ) -> Path | None:
        """Save Phase 2 optimization round output."""
        config = self.phases_config.get("optimization", {})
        if not config.get("save_each_round", False):
            return None
        return self.save(2, "optimization", content, f"round{round_num}", output_key)
    
    def save_optimizer_suggestion(
        self,
        suggestion: str | dict,
        optimizer_name: str,
        round_num: int,
        output_key: str,
    ) -> Path | None:
        """Save individual optimizer suggestion."""
        config = self.phases_config.get("optimization", {})
        if not config.get("save_optimizer_suggestions", False):
            return None
        return self.save(
            2, "optimizer",
            suggestion,
            optimizer_name.lower().replace(" ", "_"),
            output_key,
            f"round{round_num}",
        )
    
    def save_summarizer_output(
        self,
        content: str,
        round_num: int,
        output_key: str,
    ) -> Path | None:
        """Save summarizer consolidated output."""
        config = self.phases_config.get("optimization", {})
        if not config.get("save_summarizer_output", False):
            return None
        return self.save(2, "summarizer", content, f"round{round_num}", output_key)
    
    def save_judge_evaluation(
        self,
        evaluation: dict,
        judge_name: str,
        output_key: str,
    ) -> Path | None:
        """Save Phase 3 judge evaluation."""
        config = self.phases_config.get("judging", {})
        if not config.get("save_initial_evaluations", False):
            return None
        return self.save(
            3, "judge_eval",
            evaluation,
            judge_name.lower().replace(" ", "_"),
            output_key,
            extension="json",
        )
    
    def save_debate_round(
        self,
        debate_content: dict,
        round_num: int,
    ) -> Path | None:
        """Save judge debate round."""
        config = self.phases_config.get("judging", {})
        if not config.get("save_debate_rounds", False):
            return None
        return self.save(
            3, "debate",
            debate_content,
            f"round{round_num}",
            extension="json",
        )
    
    def save_consensus(
        self,
        consensus: dict,
    ) -> Path | None:
        """Save final consensus."""
        config = self.phases_config.get("judging", {})
        if not config.get("save_final_consensus", False):
            return None
        return self.save(3, "consensus", consensus, extension="json")
    
    def save_writer_input(
        self,
        selected_markmap: str,
        feedback: list,
        suggestions: list,
        output_key: str,
    ) -> Path | None:
        """Save Phase 4 writer input."""
        config = self.phases_config.get("writer", {})
        if not config.get("save_writer_input", False):
            return None
        
        # Save markmap
        self.save(4, "writer_input_markmap", selected_markmap, output_key)
        
        # Save feedback as JSON
        input_data = {
            "feedback": feedback,
            "consensus_suggestions": suggestions,
        }
        return self.save(
            4, "writer_input_feedback",
            input_data,
            output_key,
            extension="json",
        )
    
    def save_writer_output(
        self,
        content: str,
        output_key: str,
    ) -> Path | None:
        """Save Phase 4 writer output."""
        config = self.phases_config.get("writer", {})
        if not config.get("save_writer_output", False):
            return None
        return self.save(4, "writer_output", content, output_key)
    
    def save_translation(
        self,
        content: str,
        source_key: str,
        target_key: str,
        is_before: bool = False,
    ) -> Path | None:
        """Save Phase 5 translation."""
        config = self.phases_config.get("translation", {})
        
        if is_before:
            if not config.get("save_before_translation", False):
                return None
            return self.save(5, "translation_source", content, source_key)
        else:
            if not config.get("save_after_translation", False):
                return None
            return self.save(5, "translation_result", content, target_key)
    
    def save_post_processing(
        self,
        content: str,
        output_key: str,
        is_before: bool = False,
    ) -> Path | None:
        """Save Phase 6 post-processing."""
        config = self.phases_config.get("post_processing", {})
        
        if is_before:
            if not config.get("save_before_processing", False):
                return None
            return self.save(6, "postproc_before", content, output_key)
        else:
            if not config.get("save_after_processing", False):
                return None
            return self.save(6, "postproc_after", content, output_key)


# Global instance (lazy initialization)
_debug_manager: DebugOutputManager | None = None


def get_debug_manager(config: dict[str, Any] | None = None, run_dir: Path | str | None = None) -> DebugOutputManager:
    """Get or create the global debug output manager."""
    global _debug_manager
    if _debug_manager is None:
        _debug_manager = DebugOutputManager(config, run_dir=run_dir)
    return _debug_manager


def reset_debug_manager():
    """Reset the global debug manager (for new runs)."""
    global _debug_manager
    _debug_manager = None

