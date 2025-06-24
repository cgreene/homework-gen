"""Configuration management using Pydantic settings."""

import os
import yaml
from typing import List, Optional, Dict, Any
from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class LLMConfig(BaseModel):
    """LLM-related configuration."""

    default_model: str = Field(default="gpt-4o-mini", description="Default LLM model")
    api_key: Optional[str] = Field(default=None, description="API key for LLM service")
    base_url: Optional[str] = Field(default=None, description="Custom API base URL")
    local_models: List[str] = Field(
        default_factory=list, description="Available local models"
    )
    
    def __init__(self, **data):
        # Handle environment variable substitution for api_key
        if 'api_key' not in data or not data['api_key']:
            data['api_key'] = os.getenv('OPENAI_API_KEY')
        super().__init__(**data)


class PDFConfig(BaseModel):
    """PDF generation configuration."""

    theme: str = Field(default="classroom", description="PDF theme")
    font_family: str = Field(default="Arial", description="Font family")
    page_size: str = Field(default="letter", description="Page size")


class GenerationConfig(BaseModel):
    """Assignment generation configuration."""

    default_count: int = Field(default=5, description="Default number of assignments")
    default_difficulty: str = Field(
        default="medium", description="Default difficulty level"
    )


class AppConfig(BaseSettings):
    """Main application configuration."""

    llm: LLMConfig = Field(default_factory=LLMConfig)
    pdf: PDFConfig = Field(default_factory=PDFConfig)
    generation: GenerationConfig = Field(default_factory=GenerationConfig)

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        case_sensitive = False


def load_config(config_path: Optional[Path] = None) -> AppConfig:
    """Load configuration from file and environment variables."""
    config_data = {}
    
    # Try to load from YAML file
    yaml_paths = []
    if config_path:
        yaml_paths.append(config_path)
    else:
        # Default config file locations
        yaml_paths.extend([
            Path("config.yaml"),
            Path("config.yml"),
            Path.home() / ".homework-gen" / "config.yaml"
        ])
    
    for yaml_path in yaml_paths:
        if yaml_path.exists():
            try:
                with open(yaml_path, 'r') as f:
                    yaml_config = yaml.safe_load(f) or {}
                config_data.update(yaml_config)
                break
            except (yaml.YAMLError, IOError) as e:
                print(f"Warning: Could not load config from {yaml_path}: {e}")
    
    # Create config object (will automatically pick up environment variables)
    return AppConfig(**config_data)
