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
        
        # Call LLM
        response = self.llm.invoke(messages)
        
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

