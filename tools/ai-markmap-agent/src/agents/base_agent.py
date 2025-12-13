# =============================================================================
# Base Agent Class
# =============================================================================
# Abstract base class for all AI agents in the Markmap generation system.
# =============================================================================

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from ..config_loader import ConfigLoader


class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    
    Provides common functionality:
    - LLM initialization
    - Prompt loading
    - Message formatting
    - Response handling
    """
    
    def __init__(
        self,
        agent_id: str,
        model_config: dict[str, Any],
        config: dict[str, Any] | None = None,
    ):
        """
        Initialize the agent.
        
        Args:
            agent_id: Unique identifier for this agent
            model_config: Model configuration from config.yaml
            config: Full configuration dict (optional)
        """
        self.agent_id = agent_id
        self.model_config = model_config
        self.config = config or ConfigLoader.get_config()
        
        # Initialize LLM
        self.llm = self._create_llm()
        
        # Load prompts
        self.persona_prompt = self._load_prompt(model_config.get("persona_prompt"))
        self.behavior_prompt = self._load_prompt(model_config.get("behavior_prompt"))
    
    def _create_llm(self) -> BaseChatModel:
        """
        Create the LLM instance based on configuration.
        
        Returns:
            Configured LLM instance
        """
        model_name = self.model_config.get("model", "gpt-4")
        temperature = self.model_config.get("temperature", 0.7)
        max_tokens = self.model_config.get("max_tokens", 4096)
        
        # Determine provider from model name
        if model_name.startswith("claude"):
            api_key = ConfigLoader.get_api_key("anthropic")
            return ChatAnthropic(
                model=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=api_key,
            )
        else:
            # Default to OpenAI
            api_key = ConfigLoader.get_api_key("openai")
            return ChatOpenAI(
                model=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=api_key,
            )
    
    def _load_prompt(self, prompt_path: str | None) -> str:
        """
        Load a prompt from file.
        
        Args:
            prompt_path: Relative path to prompt file
            
        Returns:
            Prompt content as string
        """
        if not prompt_path:
            return ""
        
        # Resolve path relative to the ai-markmap-agent directory
        base_dir = Path(__file__).parent.parent.parent
        full_path = base_dir / prompt_path
        
        if full_path.exists():
            return full_path.read_text(encoding="utf-8")
        
        print(f"Warning: Prompt file not found: {full_path}")
        return ""
    
    def _format_prompt(self, template: str, **kwargs) -> str:
        """
        Format a prompt template with variables.
        
        Args:
            template: Prompt template with {variable} placeholders
            **kwargs: Variables to substitute
            
        Returns:
            Formatted prompt string
        """
        try:
            return template.format(**kwargs)
        except KeyError as e:
            print(f"Warning: Missing prompt variable: {e}")
            return template
    
    def _build_messages(
        self,
        user_content: str,
        system_content: str | None = None,
    ) -> list:
        """
        Build message list for LLM call.
        
        Args:
            user_content: User/human message content
            system_content: Optional system message (defaults to persona)
            
        Returns:
            List of messages
        """
        messages = []
        
        # Add system message
        if system_content:
            messages.append(SystemMessage(content=system_content))
        elif self.persona_prompt:
            messages.append(SystemMessage(content=self.persona_prompt))
        
        # Add user message
        messages.append(HumanMessage(content=user_content))
        
        return messages
    
    def _get_llm_debug_config(self) -> dict[str, Any]:
        """Get LLM debug configuration."""
        debug_config = self.config.get("debug_output", {})
        return debug_config.get("llm_calls", {})
    
    def _save_llm_call_input(self, messages: list, call_type: str = "invoke"):
        """
        Save LLM input (prompt) to debug file.
        
        Args:
            messages: List of messages sent to LLM
            call_type: Type of call (invoke, evaluate, etc.)
        """
        llm_config = self._get_llm_debug_config()
        if not llm_config.get("enabled", False) or not llm_config.get("save_input", False):
            return
        
        try:
            from ..debug_output import get_debug_manager
            debug = get_debug_manager(self.config)
            
            if not debug.enabled:
                return
            
            # Format messages for saving
            fmt = llm_config.get("format", "md")
            
            if fmt == "md":
                content = self._format_messages_as_markdown(messages)
            else:
                content = self._format_messages_as_json(messages)
            
            # Determine filename
            if llm_config.get("save_as_single_file", False):
                from datetime import datetime
                timestamp = datetime.now().strftime("%H%M%S_%f")
                filename = f"llm_input_{self.agent_id}_{call_type}_{timestamp}"
            else:
                filename = f"llm_input_{self.agent_id}_{call_type}"
            
            # Save to debug directory
            ext = "md" if fmt == "md" else "json"
            filepath = debug.run_dir / f"{filename}.{ext}"
            filepath.write_text(content, encoding="utf-8")
            print(f"      📝 LLM input saved: {filepath.name}")
            
        except Exception as e:
            print(f"      ⚠ Failed to save LLM input: {e}")
    
    def _save_llm_call_output(self, response: str, call_type: str = "invoke"):
        """
        Save LLM output (response) to debug file.
        
        Args:
            response: LLM response content
            call_type: Type of call (invoke, evaluate, etc.)
        """
        llm_config = self._get_llm_debug_config()
        if not llm_config.get("enabled", False) or not llm_config.get("save_output", False):
            return
        
        try:
            from ..debug_output import get_debug_manager
            debug = get_debug_manager(self.config)
            
            if not debug.enabled:
                return
            
            # Determine filename
            if llm_config.get("save_as_single_file", False):
                from datetime import datetime
                timestamp = datetime.now().strftime("%H%M%S_%f")
                filename = f"llm_output_{self.agent_id}_{call_type}_{timestamp}"
            else:
                filename = f"llm_output_{self.agent_id}_{call_type}"
            
            # Save to debug directory
            filepath = debug.run_dir / f"{filename}.md"
            filepath.write_text(response, encoding="utf-8")
            print(f"      📤 LLM output saved: {filepath.name}")
            
        except Exception as e:
            print(f"      ⚠ Failed to save LLM output: {e}")
    
    def _format_messages_as_markdown(self, messages: list) -> str:
        """Format messages as readable markdown."""
        from datetime import datetime
        
        lines = [
            f"# LLM Input: {self.agent_id}",
            f"**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Model**: {self.model_config.get('model', 'unknown')}",
            f"**Temperature**: {self.model_config.get('temperature', 'unknown')}",
            f"**Max Tokens**: {self.model_config.get('max_tokens', 'unknown')}",
            "",
            "---",
            "",
        ]
        
        total_chars = 0
        for i, msg in enumerate(messages):
            if hasattr(msg, 'type'):
                msg_type = msg.type
            else:
                msg_type = type(msg).__name__
            
            content = msg.content if hasattr(msg, 'content') else str(msg)
            total_chars += len(content)
            
            lines.append(f"## Message {i+1}: {msg_type.upper()}")
            lines.append(f"**Length**: {len(content)} characters")
            lines.append("")
            lines.append(content)
            lines.append("")
            lines.append("---")
            lines.append("")
        
        lines.insert(6, f"**Total Content Length**: ~{total_chars:,} characters")
        
        return "\n".join(lines)
    
    def _format_messages_as_json(self, messages: list) -> str:
        """Format messages as JSON."""
        import json
        
        data = {
            "agent_id": self.agent_id,
            "model": self.model_config.get("model", "unknown"),
            "temperature": self.model_config.get("temperature", "unknown"),
            "messages": []
        }
        
        for msg in messages:
            msg_type = msg.type if hasattr(msg, 'type') else type(msg).__name__
            content = msg.content if hasattr(msg, 'content') else str(msg)
            data["messages"].append({
                "role": msg_type,
                "content": content
            })
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def invoke(self, input_data: dict[str, Any]) -> str:
        """
        Invoke the agent with input data.
        
        Args:
            input_data: Input data dictionary
            
        Returns:
            Agent's response as string
        """
        # Format the behavior prompt with input data
        formatted_prompt = self._format_prompt(
            self.behavior_prompt,
            **input_data
        )
        
        # Build messages
        messages = self._build_messages(formatted_prompt)
        
        # Save LLM input if debug enabled
        self._save_llm_call_input(messages, "invoke")
        
        # Call LLM
        response = self.llm.invoke(messages)
        
        # Save LLM output if debug enabled
        self._save_llm_call_output(response.content, "invoke")
        
        return response.content
    
    async def ainvoke(self, input_data: dict[str, Any]) -> str:
        """
        Asynchronously invoke the agent with input data.
        
        Args:
            input_data: Input data dictionary
            
        Returns:
            Agent's response as string
        """
        formatted_prompt = self._format_prompt(
            self.behavior_prompt,
            **input_data
        )
        
        messages = self._build_messages(formatted_prompt)
        response = await self.llm.ainvoke(messages)
        
        return response.content
    
    @abstractmethod
    def process(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Process state and return updated state.
        
        This is the main method called by the LangGraph workflow.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state dictionary
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.agent_id})"

