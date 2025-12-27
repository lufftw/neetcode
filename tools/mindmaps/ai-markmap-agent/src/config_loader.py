# =============================================================================
# Configuration Loader
# =============================================================================
# Loads YAML configuration and handles secure runtime API key input.
# API keys are NEVER stored - they exist only in memory during execution.
# =============================================================================

from __future__ import annotations

import os
import getpass
from pathlib import Path
from typing import Any

import yaml


class ConfigLoader:
    """
    Loads and manages configuration with secure runtime API key handling.
    
    API keys are collected at runtime via secure input (getpass) and stored
    only in memory. They are automatically cleared when the program exits.
    """
    
    _instance: ConfigLoader | None = None
    _config: dict[str, Any] | None = None
    _api_keys: dict[str, str] = {}  # Runtime-only storage
    
    def __new__(cls) -> ConfigLoader:
        """Singleton pattern to ensure consistent config access."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """Initialize the config loader."""
        pass
    
    @classmethod
    def load(cls, config_path: str | Path | None = None) -> dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Args:
            config_path: Path to config file. Defaults to config/config.yaml
            
        Returns:
            Configuration dictionary
        """
        if cls._config is not None:
            return cls._config
        
        if config_path is None:
            # Default path relative to this file's location
            config_path = Path(__file__).parent.parent / "config" / "config.yaml"
        
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, "r", encoding="utf-8") as f:
            cls._config = yaml.safe_load(f)
        
        return cls._config
    
    @classmethod
    def get_config(cls) -> dict[str, Any]:
        """
        Get the loaded configuration.
        
        Returns:
            Configuration dictionary
            
        Raises:
            RuntimeError: If config hasn't been loaded yet
        """
        if cls._config is None:
            raise RuntimeError("Configuration not loaded. Call ConfigLoader.load() first.")
        return cls._config
    
    @classmethod
    def request_api_keys(cls, providers: list[str] | None = None) -> None:
        """
        Request API keys from user at runtime via secure input.
        
        Keys are stored in memory only and cleared when program exits.
        This method should be called once at program startup.
        
        Args:
            providers: List of provider names to request keys for.
                      Defaults to ["openai"] if None.
        """
        if providers is None:
            providers = ["openai"]
        
        print("\n" + "=" * 60)
        print("API Key Input")
        print("=" * 60)
        print("Enter your API keys below.")
        print("Keys are NOT stored and will be cleared when program exits.")
        print("=" * 60 + "\n")
        
        for provider in providers:
            provider_upper = provider.upper()
            existing_env = os.environ.get(f"{provider_upper}_API_KEY")
            
            if existing_env and existing_env.startswith("sk-"):
                # Key exists in environment but we still ask for confirmation
                print(f"[{provider_upper}] Environment variable found.")
                use_env = input(f"Use existing {provider_upper}_API_KEY from environment? [Y/n]: ").strip().lower()
                if use_env in ("", "y", "yes"):
                    cls._api_keys[provider] = existing_env
                    print(f"  ✓ Using environment variable for {provider_upper}\n")
                    continue
            
            # Securely request the API key
            key = getpass.getpass(f"Enter {provider_upper} API Key: ")
            
            if key:
                cls._api_keys[provider] = key
                print(f"  ✓ {provider_upper} API key accepted\n")
            else:
                print(f"  ⚠ No key provided for {provider_upper}\n")
        
        print("=" * 60)
        print("API key input complete. Proceeding...\n")
    
    @classmethod
    def get_api_key(cls, provider: str) -> str | None:
        """
        Get API key for a provider.
        
        Args:
            provider: Provider name (e.g., "openai", "anthropic")
            
        Returns:
            API key string or None if not available
        """
        return cls._api_keys.get(provider)
    
    @classmethod
    def has_api_key(cls, provider: str) -> bool:
        """
        Check if API key is available for a provider.
        
        Args:
            provider: Provider name
            
        Returns:
            True if key is available
        """
        return provider in cls._api_keys and bool(cls._api_keys[provider])
    
    @classmethod
    def clear_api_keys(cls) -> None:
        """
        Clear all API keys from memory.
        
        This is called automatically on program exit, but can be called
        manually for additional security.
        """
        # Overwrite with empty strings before clearing (security measure)
        for key in cls._api_keys:
            cls._api_keys[key] = ""
        cls._api_keys.clear()
    
    @classmethod
    def reset(cls) -> None:
        """
        Reset the configuration loader state.
        
        Clears both configuration and API keys.
        """
        cls._config = None
        cls.clear_api_keys()


# Register cleanup on program exit
import atexit
atexit.register(ConfigLoader.clear_api_keys)


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """
    Convenience function to load configuration.
    
    Args:
        config_path: Optional path to config file
        
    Returns:
        Configuration dictionary
    """
    return ConfigLoader.load(config_path)


def request_api_keys(providers: list[str] | None = None) -> None:
    """
    Convenience function to request API keys at runtime.
    
    Args:
        providers: List of provider names
    """
    ConfigLoader.request_api_keys(providers)


def get_api_key(provider: str) -> str | None:
    """
    Convenience function to get an API key.
    
    Args:
        provider: Provider name
        
    Returns:
        API key or None
    """
    return ConfigLoader.get_api_key(provider)

