"""Tests for configuration management."""

import pytest
from pathlib import Path
from homework_generator.config import AppConfig, LLMConfig, PDFConfig, GenerationConfig, load_config


class TestLLMConfig:
    """Tests for LLM configuration."""
    
    def test_llm_config_defaults(self):
        """Test default LLM configuration."""
        config = LLMConfig()
        assert config.default_model == "gpt-3.5-turbo"
        assert config.api_key is None
        assert config.local_models == []
    
    def test_llm_config_custom(self):
        """Test custom LLM configuration."""
        config = LLMConfig(
            default_model="gpt-4",
            api_key="test-key",
            local_models=["ollama/llama2"]
        )
        assert config.default_model == "gpt-4"
        assert config.api_key == "test-key"
        assert len(config.local_models) == 1


class TestPDFConfig:
    """Tests for PDF configuration."""
    
    def test_pdf_config_defaults(self):
        """Test default PDF configuration."""
        config = PDFConfig()
        assert config.theme == "classroom"
        assert config.font_family == "Arial"
        assert config.page_size == "letter"


class TestGenerationConfig:
    """Tests for generation configuration."""
    
    def test_generation_config_defaults(self):
        """Test default generation configuration."""
        config = GenerationConfig()
        assert config.default_count == 5
        assert config.default_difficulty == "medium"


class TestAppConfig:
    """Tests for main application configuration."""
    
    def test_app_config_defaults(self):
        """Test default application configuration."""
        config = AppConfig()
        assert isinstance(config.llm, LLMConfig)
        assert isinstance(config.pdf, PDFConfig)
        assert isinstance(config.generation, GenerationConfig)
    
    def test_load_config_no_file(self):
        """Test loading config when no file exists."""
        config = load_config(Path("nonexistent.yaml"))
        assert isinstance(config, AppConfig)
