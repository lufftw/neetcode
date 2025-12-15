# =============================================================================
# Content Compressor
# =============================================================================
# Compresses long content to fit within token limits while preserving
# essential information.
# =============================================================================

from __future__ import annotations

from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from ..config_loader import ConfigLoader


class ContentCompressor:
    """
    Compresses content that exceeds token limits.
    
    Uses a cheaper/faster model to summarize content while
    preserving the most important information.
    """
    
    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialize the compressor.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or ConfigLoader.get_config()
        compressor_config = self.config.get("models", {}).get("compressor", {})
        
        model_name = compressor_config.get("model", "gpt-3.5-turbo")
        temperature = compressor_config.get("temperature", 0.3)
        max_tokens = compressor_config.get("max_tokens", 2048)
        
        api_key = ConfigLoader.get_api_key("openai")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key,
        )
        
        # Load behavior prompt
        behavior_path = compressor_config.get("behavior_prompt", "")
        self.behavior_prompt = self._load_prompt(behavior_path)
        
        # Workflow config for token threshold
        workflow_config = self.config.get("workflow", {})
        self.max_tokens_before_compress = workflow_config.get(
            "max_tokens_before_compress", 8000
        )
    
    def _save_llm_call(self, agent_id: str, call_type: str, content: Any, is_input: bool = True):
        """Save LLM call input or output for debugging."""
        try:
            from ..debug_output import get_debug_manager
            debug = get_debug_manager(self.config)
            
            if not debug.enabled:
                return
            
            # Get LLM debug config
            llm_config = self.config.get("debug_output", {}).get("llm_calls", {})
            if not llm_config.get("enabled", False):
                return
            
            if is_input and not llm_config.get("save_input", False):
                return
            if not is_input and not llm_config.get("save_output", False):
                return
            
            # Format content
            if is_input:
                # messages list
                import json
                if isinstance(content, list):
                    content_str = json.dumps(
                        [{"role": msg.type if hasattr(msg, "type") else "unknown", 
                          "content": msg.content if hasattr(msg, "content") else str(msg)} 
                         for msg in content],
                        indent=2,
                        ensure_ascii=False
                    )
                else:
                    content_str = str(content)
                filename = f"llm_input_{agent_id}_{call_type}"
            else:
                # response string
                content_str = str(content)
                filename = f"llm_output_{agent_id}_{call_type}"
            
            # Save to debug directory
            ext = "md"
            filepath = debug.run_dir / f"{filename}.{ext}"
            filepath.write_text(content_str, encoding="utf-8")
            prefix = "📝" if is_input else "📤"
            print(f"      {prefix} LLM {'input' if is_input else 'output'} saved: {filepath.name}")
            
        except Exception as e:
            # Silently fail if debug output is not available
            pass
    
    def _load_prompt(self, prompt_path: str) -> str:
        """Load prompt from file."""
        if not prompt_path:
            return self._default_prompt()
        
        from pathlib import Path
        base_dir = Path(__file__).parent.parent.parent
        full_path = base_dir / prompt_path
        
        if full_path.exists():
            return full_path.read_text(encoding="utf-8")
        
        return self._default_prompt()
    
    def _default_prompt(self) -> str:
        """Return default compression prompt."""
        return """You are a content compressor. Your task is to compress the following content
while preserving all essential information, key decisions, and important details.

Content to compress:
{content}

Requirements:
1. Preserve all important facts and decisions
2. Keep technical details intact
3. Remove redundant information
4. Maintain the logical structure
5. Target approximately {target_ratio}% of original length

Output only the compressed content, no explanations."""
    
    def should_compress(self, content: str) -> bool:
        """
        Check if content should be compressed based on estimated tokens.
        
        Args:
            content: Content to check
            
        Returns:
            True if compression is recommended
        """
        # Rough estimate: ~4 characters per token
        estimated_tokens = len(content) // 4
        return estimated_tokens > self.max_tokens_before_compress
    
    def compress(
        self,
        content: str,
        target_ratio: float = 0.5,
        preserve_structure: bool = True,
    ) -> str:
        """
        Compress content to fit within token limits.
        
        Args:
            content: Content to compress
            target_ratio: Target size as ratio of original (0.5 = 50%)
            preserve_structure: Whether to maintain document structure
            
        Returns:
            Compressed content
        """
        if not self.should_compress(content):
            return content
        
        prompt = self.behavior_prompt.format(
            content=content,
            target_ratio=int(target_ratio * 100),
        )
        
        if preserve_structure:
            prompt += "\n\nPreserve the hierarchical structure (headings, lists)."
        
        messages = [
            SystemMessage(content="You are a precise content compressor."),
            HumanMessage(content=prompt),
        ]
        
        # Save LLM input
        self._save_llm_call("compressor", "compress_content", messages, is_input=True)
        
        try:
            response = self.llm.invoke(messages)
            
            # Save LLM output
            self._save_llm_call("compressor", "compress_content", response.content, is_input=False)
            
            return response.content
        except Exception as e:
            print(f"Warning: Compression failed: {e}")
            # Fallback: simple truncation
            return self._truncate(content, target_ratio)
    
    def compress_history(
        self,
        history: list[dict[str, Any]],
        max_items: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Compress optimization history to recent items.
        
        Args:
            history: Full optimization history
            max_items: Maximum items to keep
            
        Returns:
            Compressed history list
        """
        if len(history) <= max_items:
            return history
        
        # Keep most recent items
        recent = history[-max_items:]
        
        # Summarize older items
        older = history[:-max_items]
        older_summary = self._summarize_history(older)
        
        # Insert summary at the beginning
        summary_entry = {
            "round": "summary",
            "optimizer_id": "compressor",
            "optimizer_name": "History Summary",
            "suggestions": older_summary,
        }
        
        return [summary_entry] + recent
    
    def _summarize_history(self, history: list[dict[str, Any]]) -> str:
        """Summarize older history entries."""
        if not history:
            return ""
        
        # Extract key points from each entry
        points = []
        for entry in history:
            suggestions = entry.get("suggestions", "")
            # Take first 200 chars of each
            points.append(f"Round {entry.get('round', '?')}: {suggestions[:200]}...")
        
        content = "\n\n".join(points)
        
        prompt = f"""Summarize the following optimization history into key decisions and patterns:

{content}

Provide a concise summary of the main changes and decisions made."""
        
        messages = [
            SystemMessage(content="You summarize optimization history."),
            HumanMessage(content=prompt),
        ]
        
        # Save LLM input
        self._save_llm_call("compressor", "summarize_history", messages, is_input=True)
        
        try:
            response = self.llm.invoke(messages)
            
            # Save LLM output
            self._save_llm_call("compressor", "summarize_history", response.content, is_input=False)
            
            return response.content
        except Exception:
            return f"Summary of {len(history)} earlier rounds."
    
    def _truncate(self, content: str, ratio: float) -> str:
        """Simple truncation fallback."""
        target_len = int(len(content) * ratio)
        if target_len >= len(content):
            return content
        
        # Try to truncate at a paragraph break
        truncated = content[:target_len]
        last_para = truncated.rfind("\n\n")
        
        if last_para > target_len * 0.7:
            truncated = truncated[:last_para]
        
        return truncated + "\n\n[Content truncated for length]"


# Global instance
_compressor: ContentCompressor | None = None


def get_compressor(config: dict[str, Any] | None = None) -> ContentCompressor:
    """Get the global compressor instance."""
    global _compressor
    if _compressor is None:
        _compressor = ContentCompressor(config)
    return _compressor


def compress_if_needed(
    content: str,
    target_ratio: float = 0.5,
) -> str:
    """
    Compress content if it exceeds the token threshold.
    
    Convenience function.
    
    Args:
        content: Content to potentially compress
        target_ratio: Target compression ratio
        
    Returns:
        Original or compressed content
    """
    compressor = get_compressor()
    if compressor.should_compress(content):
        return compressor.compress(content, target_ratio)
    return content


def compress_data_for_agent(
    problems: dict[str, Any],
    agent_type: str = "planner",
    config: dict[str, Any] | None = None,
) -> str:
    """
    Compress problem data for efficient transmission to agents.
    
    V3: Produces minimal problem representations for Structure Spec generation.
    
    Args:
        problems: Full problem metadata dictionary
        agent_type: Type of agent ("planner", "strategist", "writer")
        config: Configuration dictionary
        
    Returns:
        Compressed string representation
    """
    config = config or {}
    compression_config = config.get("data_compression", {})
    
    # Fields to include based on agent type
    if agent_type == "planner":
        # Planner needs: id, title, patterns, difficulty, has_solution
        fields = ["id", "title", "patterns", "difficulty", "has_solution"]
    elif agent_type == "strategist":
        # Strategist only needs problem IDs (already in spec)
        fields = ["id", "patterns"]
    elif agent_type == "writer":
        # Writer needs full metadata for link generation
        fields = ["id", "title", "slug", "patterns", "difficulty", 
                  "solution_file", "has_solution", "time_complexity", "space_complexity"]
    else:
        fields = compression_config.get("problem_fields", ["id", "title", "patterns"])
    
    lines = []
    
    for key, problem in problems.items():
        if not isinstance(problem, dict):
            continue
        
        # Extract only needed fields
        entry = {}
        for field in fields:
            if field in problem:
                entry[field] = problem[field]
            elif field == "has_solution":
                entry[field] = bool(problem.get("solution_file", ""))
        
        if entry:
            # Compact representation
            if agent_type == "planner":
                # Single line format for efficiency
                pid = entry.get("id", key)
                title = entry.get("title", "Unknown")
                diff = entry.get("difficulty", "?")
                patterns = ",".join(entry.get("patterns", [])[:3])
                solved = "✓" if entry.get("has_solution") else "○"
                lines.append(f"{pid} | {title} | {diff} | [{patterns}] | {solved}")
            else:
                # JSON-like for writer
                import json
                lines.append(json.dumps(entry, ensure_ascii=False))
    
    if agent_type == "planner":
        header = "ID | Title | Difficulty | Patterns | Solved"
        separator = "-" * 60
        return f"{header}\n{separator}\n" + "\n".join(lines)
    
    return "\n".join(lines)

