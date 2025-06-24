"""Tests for content generator."""

import pytest
import json
from unittest.mock import Mock, patch
from homework_generator.content_generator import ContentGenerator, ASSIGNMENT_SCHEMA
from homework_generator.llm_client import LLMClient
from homework_generator.models import Assignment, HomeworkPacket


class TestContentGenerator:
    """Tests for content generator functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.llm_client = Mock(spec=LLMClient)
        self.llm_client.model = "test-model"  # Add model attribute to mock
        self.generator = ContentGenerator(self.llm_client)
        
        # Mock LLM response
        self.mock_llm_response = json.dumps({
            "assignments": [
                {
                    "title": "Sample Math Assignment",
                    "grade_level": "5th Grade",
                    "subject": "Mathematics",
                    "difficulty": "Medium",
                    "estimated_time": "20 minutes",
                    "instructions": "Complete all problems showing your work.",
                    "questions": ["What is 5 + 3?", "What is 10 - 4?"],
                    "materials_needed": ["pencil", "paper"],
                    "learning_objectives": ["Addition", "Subtraction"]
                }
            ]
        })
        self.llm_client.generate_response.return_value = self.mock_llm_response
    
    def test_content_generator_initialization(self):
        """Test content generator initialization."""
        assert self.generator.llm_client == self.llm_client
        assert self.generator.template_manager is not None
    
    def test_generate_assignments_basic(self):
        """Test basic assignment generation."""
        assignments = self.generator.generate_assignments(
            topic="Basic Addition",
            count=2,
            difficulty="Easy",
            grade_level="2nd Grade",
            template="math"
        )
        
        assert len(assignments) == 1  # Mock returns 1 assignment
        assert isinstance(assignments[0], Assignment)
        assert assignments[0].subject == "Mathematics"
        assert assignments[0].difficulty == "Medium"  # From mock data
        assert assignments[0].title == "Sample Math Assignment"
    
    def test_generate_homework_packet(self):
        """Test homework packet generation."""
        packet = self.generator.generate_homework_packet(
            topic="Fractions",
            count=3,
            difficulty="Medium", 
            grade_level="5th Grade",
            template="math"
        )
        
        assert isinstance(packet, HomeworkPacket)
        assert packet.topic == "Fractions"
        assert packet.model_used == "test-model"
        assert len(packet.assignments) == 1  # Mock returns 1 assignment
        assert packet.assignment_count == 1
    
    def test_build_prompt(self):
        """Test prompt building."""
        prompt = self.generator._build_prompt(
            template="generic",
            topic="Test Topic",
            count=2,
            difficulty="Easy",
            grade_level="3rd Grade"
        )
        
        assert "You are an expert educator" in prompt
        assert "Test Topic" in prompt
        assert "3rd Grade" in prompt
        assert "Easy" in prompt
        assert "OUTPUT FORMAT:" in prompt
        assert "JSON" in prompt
    
    def test_validate_response_valid(self):
        """Test validation of valid response."""
        valid_response = json.dumps({
            "assignments": [
                {
                    "title": "Test Assignment",
                    "grade_level": "4th Grade",
                    "subject": "Math",
                    "difficulty": "Easy",
                    "estimated_time": "10 min",
                    "instructions": "Solve problems",
                    "questions": ["1+1=?", "2+2=?"],
                    "materials_needed": ["pencil"],
                    "learning_objectives": ["Basic addition"]
                }
            ]
        })
        
        result = self.generator._validate_response(valid_response)
        assert "assignments" in result
        assert len(result["assignments"]) == 1
    
    def test_validate_response_invalid_json(self):
        """Test validation of invalid JSON."""
        invalid_response = "This is not JSON"
        
        with pytest.raises(ValueError, match="Invalid JSON response"):
            self.generator._validate_response(invalid_response)
    
    def test_validate_response_missing_assignments(self):
        """Test validation of response missing assignments field."""
        invalid_response = json.dumps({"wrong_field": "data"})
        
        with pytest.raises(ValueError, match="Response doesn't match schema"):
            self.generator._validate_response(invalid_response)
    
    def test_validate_response_missing_required_field(self):
        """Test validation of assignment missing required field."""
        invalid_response = json.dumps({
            "assignments": [
                {
                    "title": "Test",
                    # Missing other required fields
                }
            ]
        })
        
        with pytest.raises(ValueError, match="Response doesn't match schema"):
            self.generator._validate_response(invalid_response)
    
    def test_extract_json_from_text(self):
        """Test extracting JSON from text with extra content."""
        text_with_json = '''Here is some text before
        {"assignments": [{"title": "test"}]}
        And some text after'''
        
        result = self.generator._extract_json_from_text(text_with_json)
        assert result is not None
        assert "assignments" in result
    
    def test_extract_json_from_text_no_json(self):
        """Test extracting JSON when no valid JSON exists."""
        text_without_json = "This is just plain text with no JSON"
        
        result = self.generator._extract_json_from_text(text_without_json)
        assert result is None
    
    def test_get_examples(self):
        """Test getting few-shot examples."""
        examples = self.generator._get_examples("math")
        
        # Should return valid JSON string
        examples_data = json.loads(examples)
        assert "assignments" in examples_data
        assert len(examples_data["assignments"]) >= 1
    
    @patch('homework_generator.content_generator.datetime')
    def test_homework_packet_timestamp(self, mock_datetime):
        """Test that homework packet includes timestamp."""
        mock_datetime.now.return_value.isoformat.return_value = "2024-01-01T12:00:00"
        
        packet = self.generator.generate_homework_packet(
            topic="Test",
            count=1,
            difficulty="Easy",
            grade_level="1st Grade"
        )
        
        assert packet.generated_at == "2024-01-01T12:00:00"
