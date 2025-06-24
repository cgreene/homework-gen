"""Tests for assignment formatter."""

import pytest
from pathlib import Path
from homework_generator.formatter import AssignmentFormatter
from homework_generator.models import Assignment


class TestAssignmentFormatter:
    """Tests for assignment formatter functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.formatter = AssignmentFormatter("templates")
        
        # Create a sample assignment
        self.sample_assignment = Assignment(
            title="Basic Math Problems",
            grade_level="3rd Grade",
            subject="Mathematics",
            difficulty="Easy",
            estimated_time="15 minutes",
            instructions="Solve the following math problems. Show your work.",
            questions=[
                "What is 5 + 3?",
                "Calculate 10 - 4",
                "Find the result of 2 × 6"
            ],
            materials_needed=["pencil", "paper"],
            learning_objectives=[
                "Practice basic arithmetic",
                "Develop problem-solving skills"
            ]
        )
    
    def test_formatter_initialization(self):
        """Test formatter initialization."""
        assert self.formatter.template_dir == Path("templates")
    
    def test_format_assignment_basic(self):
        """Test basic assignment formatting."""
        html = self.formatter.format_assignment(self.sample_assignment)
        
        # Check that key content is present
        assert "Basic Math Problems" in html
        assert "3rd Grade" in html
        assert "Mathematics" in html
        assert "Easy" in html
        assert "15 minutes" in html
        assert "Solve the following math problems" in html
        assert "What is 5 + 3?" in html
        assert "pencil" in html
        assert "Practice basic arithmetic" in html
    
    def test_format_assignment_minimal(self):
        """Test formatting assignment with only required fields."""
        minimal_assignment = Assignment(
            title="Simple Assignment",
            grade_level="1st Grade",
            subject="Reading",
            difficulty="Easy",
            estimated_time="10 minutes",
            instructions="Read the passage.",
            questions=["What is the main idea?"]
        )
        
        html = self.formatter.format_assignment(minimal_assignment)
        
        assert "Simple Assignment" in html
        assert "1st Grade" in html
        assert "Reading" in html
        assert "What is the main idea?" in html
    
    def test_format_packet_single_assignment(self):
        """Test formatting packet with single assignment."""
        html = self.formatter.format_packet([self.sample_assignment])
        
        # Should be complete HTML document
        assert "<!DOCTYPE html>" in html
        assert "<html" in html
        assert "</html>" in html
        assert "Basic Math Problems" in html
    
    def test_format_packet_multiple_assignments(self):
        """Test formatting packet with multiple assignments."""
        assignment2 = Assignment(
            title="Reading Comprehension",
            grade_level="3rd Grade",
            subject="English",
            difficulty="Medium",
            estimated_time="20 minutes",
            instructions="Read and answer questions.",
            questions=["What happened first?", "Who is the main character?"]
        )
        
        html = self.formatter.format_packet([self.sample_assignment, assignment2])
        
        assert "Basic Math Problems" in html
        assert "Reading Comprehension" in html
        assert "<!DOCTYPE html>" in html
    
    def test_format_packet_empty(self):
        """Test formatting empty packet."""
        html = self.formatter.format_packet([])
        
        assert "No assignments to display" in html
        assert "<html>" in html
    
    def test_format_to_markdown(self):
        """Test formatting assignment as Markdown."""
        md = self.formatter.format_to_markdown(self.sample_assignment)
        
        assert "# Basic Math Problems" in md
        assert "**Grade Level:** 3rd Grade" in md
        assert "**Subject:** Mathematics" in md
        assert "## Instructions" in md
        assert "## Problems" in md
        assert "1. What is 5 + 3?" in md
        assert "2. Calculate 10 - 4" in md
        assert "## Learning Objectives" in md
        assert "## Materials Needed" in md
    
    def test_format_to_markdown_minimal(self):
        """Test Markdown formatting with minimal assignment."""
        minimal_assignment = Assignment(
            title="Simple Test",
            grade_level="2nd Grade", 
            subject="Math",
            difficulty="Easy",
            estimated_time="5 minutes",
            instructions="Do the work.",
            questions=["1+1=?"]
        )
        
        md = self.formatter.format_to_markdown(minimal_assignment)
        
        assert "# Simple Test" in md
        assert "## Instructions" in md
        assert "## Problems" in md
        assert "1. 1+1=?" in md
        # Should not have sections for optional fields
        assert "## Learning Objectives" not in md
        assert "## Materials Needed" not in md
    
    def test_load_styles_fallback(self):
        """Test style loading with fallback."""
        # Test with non-existent template directory
        formatter = AssignmentFormatter("nonexistent")
        styles = formatter._load_styles()
        
        # Should return fallback styles
        assert "font-family" in styles
        assert "Arial" in styles
        assert ".assignment" in styles
    
    def test_format_assignment_basic_without_dependencies(self):
        """Test basic formatting method directly."""
        html = self.formatter._format_assignment_basic(self.sample_assignment)
        
        assert '<div class="assignment">' in html
        assert "<h1>Basic Math Problems</h1>" in html
        assert "<h2>Instructions</h2>" in html
        assert "<h2>Problems</h2>" in html
        assert "<ol>" in html
        assert "</ol>" in html
    
    def test_combine_assignments_basic(self):
        """Test basic assignment combination."""
        assignment_htmls = [
            '<div class="assignment"><h1>Test 1</h1></div>',
            '<div class="assignment"><h1>Test 2</h1></div>'
        ]
        
        html = self.formatter._combine_assignments_basic(assignment_htmls)
        
        assert "<!DOCTYPE html>" in html
        assert "Test 1" in html
        assert "Test 2" in html
        assert "<style>" in html
