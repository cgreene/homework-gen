"""Tests for LLM client."""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from homework_generator.llm_client import LLMClient


class TestLLMClient:
    """Tests for LLM client functionality."""
    
    def test_llm_client_initialization(self):
        """Test LLM client initialization."""
        client = LLMClient("gpt-3.5-turbo", cache_enabled=False)
        assert client.model == "gpt-3.5-turbo"
        assert client.cache is None
    
    def test_llm_client_with_cache(self):
        """Test LLM client with caching enabled."""
        client = LLMClient("gpt-4", cache_enabled=True)
        assert client.model == "gpt-4"
        assert client.cache_enabled is True
    
    @patch('homework_generator.llm_client.litellm.completion')
    def test_generate_response_mock(self, mock_completion):
        """Test generate_response with mock data."""
        # Set up mock response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "assignments": [
                {
                    "title": "Mock Assignment 1: Basic Problems",
                    "grade_level": "5th Grade",
                    "subject": "Mathematics",
                    "difficulty": "Medium",
                    "estimated_time": "20 minutes",
                    "instructions": "Complete the following problems.",
                    "questions": ["Problem 1", "Problem 2"],
                    "materials_needed": ["pencil", "paper"],
                    "learning_objectives": ["Basic math skills"]
                }
            ]
        })
        mock_completion.return_value = mock_response
        
        client = LLMClient("gpt-3.5-turbo", cache_enabled=False, api_key="test-key")
        
        response = client.generate_response("Generate math problems")
        
        # Should return valid JSON
        data = json.loads(response)
        assert "assignments" in data
        assert len(data["assignments"]) == 1
        assert data["assignments"][0]["title"] == "Mock Assignment 1: Basic Problems"
    
    def test_cache_key_generation(self):
        """Test cache key generation."""
        client = LLMClient("test-model", cache_enabled=False)
        
        key1 = client._get_cache_key("test prompt", temperature=0.5)
        key2 = client._get_cache_key("test prompt", temperature=0.5)
        key3 = client._get_cache_key("different prompt", temperature=0.5)
        
        # Same input should generate same key
        assert key1 == key2
        # Different input should generate different key
        assert key1 != key3
    
    def test_cache_key_deterministic(self):
        """Test that cache keys are deterministic across parameter order."""
        client = LLMClient("test-model", cache_enabled=False)
        
        key1 = client._get_cache_key("test", temperature=0.5, max_tokens=100)
        key2 = client._get_cache_key("test", max_tokens=100, temperature=0.5)
        
        # Same parameters in different order should generate same key
        assert key1 == key2
    
    @patch('homework_generator.llm_client.DEPENDENCIES_AVAILABLE', True)
    @patch('homework_generator.llm_client.litellm')
    def test_generate_response_with_litellm(self, mock_litellm):
        """Test generate_response with actual litellm (mocked)."""
        # Mock the litellm response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"test": "response"}'
        mock_litellm.completion.return_value = mock_response
        
        client = LLMClient("gpt-3.5-turbo", cache_enabled=False)
        
        # Mock the dependencies check
        with patch.object(client, '_mock_response') as mock_method:
            # Override the dependencies check
            client.__class__.__dict__['generate_response'].__wrapped__(
                client, "test prompt"
            )
            
            # Verify litellm was called
            mock_litellm.completion.assert_called_once()
    
    def test_mock_response_structure(self):
        """Test that mock response has correct structure."""
        client = LLMClient("test-model", cache_enabled=False)
        
        response = client._mock_response("test prompt")
        data = json.loads(response)
        
        # Verify structure matches expected Assignment schema
        assignment = data["assignments"][0]
        required_fields = ["title", "grade_level", "subject", "difficulty", 
                          "estimated_time", "instructions", "questions"]
        
        for field in required_fields:
            assert field in assignment
        
        assert isinstance(assignment["questions"], list)
        assert len(assignment["questions"]) > 0
    
    def test_api_key_handling(self):
        """Test API key is properly stored."""
        client = LLMClient("gpt-3.5-turbo", api_key="test-key-123")
        assert client.api_key == "test-key-123"
