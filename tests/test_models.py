"""Tests for data models."""

import pytest
from pydantic import ValidationError
from homework_generator.models import Assignment, HomeworkPacket, AssignmentRequest


class TestAssignmentRequest:
    """Tests for AssignmentRequest model."""
    
    def test_assignment_request_creation_valid(self):
        """Test creating a valid assignment request."""
        request = AssignmentRequest(
            topic="Fractions",
            subject="Mathematics",
            difficulty="Medium",
            grade_level="5th Grade",
            num_questions=8,
            special_instructions="Focus on adding fractions"
        )
        
        assert request.topic == "Fractions"
        assert request.subject == "Mathematics"
        assert request.difficulty == "Medium"
        assert request.grade_level == "5th Grade"
        assert request.num_questions == 8
    
    def test_assignment_request_defaults(self):
        """Test assignment request with default values."""
        request = AssignmentRequest(
            topic="Geometry",
            subject="Mathematics",
            difficulty="Easy",
            grade_level="4th Grade"
        )
        
        assert request.num_questions == 10  # default value
        assert request.special_instructions is None  # default value
    
    def test_assignment_request_required_fields(self):
        """Test that required fields raise validation error when missing."""
        with pytest.raises(ValidationError):
            AssignmentRequest(
                topic="Test",
                # missing required fields
            )


class TestAssignment:
    """Tests for Assignment model."""
    
    def test_assignment_creation_valid(self):
        """Test creating a valid assignment."""
        assignment = Assignment(
            title="Basic Fractions",
            subject="Mathematics",
            difficulty="Medium",
            questions=["What is 1/2 + 1/4?", "Simplify 6/8"],
            instructions="Complete the fraction problems below.",
            grade_level="5th Grade",
            estimated_time="15 minutes",
            materials_needed=["pencil", "calculator"],
            learning_objectives=["Add fractions", "Simplify fractions"]
        )
        
        assert assignment.title == "Basic Fractions"
        assert assignment.subject == "Mathematics"
        assert assignment.difficulty == "Medium"
        assert len(assignment.questions) == 2
        assert assignment.grade_level == "5th Grade"
    
    def test_assignment_minimal_creation(self):
        """Test creating an assignment with minimal required fields."""
        assignment = Assignment(
            title="Simple Math",
            subject="Mathematics",
            difficulty="Easy",
            questions=["What is 2 + 2?"]
        )
        
        assert assignment.title == "Simple Math"
        assert assignment.subject == "Mathematics"
        assert assignment.difficulty == "Easy"
        assert len(assignment.questions) == 1
        assert assignment.instructions is None  # optional field
        assert assignment.grade_level is None  # optional field
    
    def test_assignment_required_fields(self):
        """Test that required fields are enforced."""
        with pytest.raises(ValidationError):
            Assignment()
    
    def test_assignment_empty_questions_list(self):
        """Test assignment with empty questions list."""
        with pytest.raises(ValidationError):
            Assignment(
                title="Test",
                subject="Math",
                difficulty="Easy",
                questions=[]  # Empty list should fail validation
            )


class TestHomeworkPacket:
    """Tests for HomeworkPacket model."""
    
    def test_homework_packet_creation(self):
        """Test creating a homework packet."""
        assignment = Assignment(
            title="Test Assignment",
            subject="Mathematics",
            difficulty="Easy",
            questions=["1+1=?"]
        )
        
        packet = HomeworkPacket(
            assignments=[assignment],
            topic="Basic Math",
            generated_at="2024-01-01T12:00:00",
            model_used="gpt-3.5-turbo"
        )
        
        assert len(packet.assignments) == 1
        assert packet.assignment_count == 1
        assert packet.topic == "Basic Math"
    
    def test_empty_packet(self):
        """Test packet with no assignments."""
        packet = HomeworkPacket(
            assignments=[],
            topic="Empty Test",
            generated_at="2024-01-01T12:00:00",
            model_used="test-model"
        )
        
        assert packet.assignment_count == 0
    
    def test_multiple_assignments_packet(self):
        """Test packet with multiple assignments."""
        assignment1 = Assignment(
            title="Math Assignment 1",
            subject="Mathematics",
            difficulty="Easy",
            questions=["2+2=?"]
        )
        
        assignment2 = Assignment(
            title="Math Assignment 2",
            subject="Mathematics",
            difficulty="Medium",
            questions=["5*3=?", "10-4=?"]
        )
        
        packet = HomeworkPacket(
            assignments=[assignment1, assignment2],
            topic="Basic Math Operations",
            generated_at="2024-01-01T12:00:00",
            model_used="gpt-4"
        )
        
        assert packet.assignment_count == 2
        assert len(packet.assignments) == 2
        assert packet.assignments[0].title == "Math Assignment 1"
        assert packet.assignments[1].title == "Math Assignment 2"
