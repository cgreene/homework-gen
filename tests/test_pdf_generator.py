"""Tests for PDF generator module."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from homework_generator.pdf_generator import PDFGenerator
from homework_generator.models import Assignment


class TestPDFGenerator:
    """Test cases for PDFGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.styles_path = Path("test_styles.css")
        self.generator = PDFGenerator(styles_path=self.styles_path)
        
        # Sample assignment for testing
        self.sample_assignment = Assignment(
            title="Sample Math Assignment",
            subject="Mathematics",
            difficulty="Beginner",
            questions=[
                "What is 2 + 2?",
                "Solve for x: x + 5 = 10",
                "What is the area of a rectangle with length 4 and width 3?"
            ],
            instructions="Complete all problems. Show your work."
        )
    
    @patch('homework_generator.pdf_generator.HTML')
    @patch('homework_generator.pdf_generator.CSS')
    def test_generate_pdf_with_styles(self, mock_css, mock_html):
        """Test PDF generation with CSS styles."""
        # Setup mocks
        mock_html_instance = Mock()
        mock_html.return_value = mock_html_instance
        mock_css_instance = Mock()
        mock_css.return_value = mock_css_instance
        
        # Mock file reading
        css_content = "body { font-family: Arial; }"
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.read_text', return_value=css_content):
            
            html_content = "<html><body><h1>Test</h1></body></html>"
            output_path = Path("/tmp/test_output.pdf")
            
            self.generator.generate_pdf(html_content, output_path)
            
            # Verify HTML and CSS were created
            mock_html.assert_called_once_with(string=html_content)
            mock_css.assert_called_once_with(string=css_content)
            
            # Verify PDF was generated with styles
            mock_html_instance.write_pdf.assert_called_once_with(
                str(output_path), 
                stylesheets=[mock_css_instance]
            )
    
    @patch('homework_generator.pdf_generator.HTML')
    def test_generate_pdf_without_styles(self, mock_html):
        """Test PDF generation without CSS styles."""
        # Setup mock
        mock_html_instance = Mock()
        mock_html.return_value = mock_html_instance
        
        # Mock no styles file
        with patch('pathlib.Path.exists', return_value=False):
            
            html_content = "<html><body><h1>Test</h1></body></html>"
            output_path = Path("/tmp/test_output.pdf")
            
            self.generator.generate_pdf(html_content, output_path)
            
            # Verify HTML was created
            mock_html.assert_called_once_with(string=html_content)
            
            # Verify PDF was generated without styles
            mock_html_instance.write_pdf.assert_called_once_with(str(output_path))
    
    @patch('homework_generator.pdf_generator.HTML')
    @patch('homework_generator.pdf_generator.CSS')
    def test_generate_packet_pdf_single_assignment(self, mock_css, mock_html):
        """Test generating PDF packet with single assignment."""
        # Setup mocks
        mock_html_instance = Mock()
        mock_html.return_value = mock_html_instance
        mock_css_instance = Mock()
        mock_css.return_value = mock_css_instance
        
        # Mock styles
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.read_text', return_value="body {}"):
            
            template_content = """
            <div class="assignment">
                <h1>{title}</h1>
                <p>Subject: {subject}</p>
                <p>Difficulty: {difficulty}</p>
                <p>Instructions: {instructions}</p>
                <div class="questions">{questions}</div>
            </div>
            """
            
            output_path = Path("/tmp/test_packet.pdf")
            
            self.generator.generate_packet_pdf(
                [self.sample_assignment], 
                output_path, 
                template_content
            )
            
            # Verify PDF generation was called
            mock_html.assert_called_once()
            mock_html_instance.write_pdf.assert_called_once()
            
            # Get the HTML content that was passed
            call_args = mock_html.call_args[1]  # keyword args
            html_content = call_args['string']
            
            # Verify assignment content is in the HTML
            assert "Sample Math Assignment" in html_content
            assert "Mathematics" in html_content
            assert "Beginner" in html_content
            assert "What is 2 + 2?" in html_content
    
    @patch('homework_generator.pdf_generator.HTML')
    def test_generate_packet_pdf_multiple_assignments(self, mock_html):
        """Test generating PDF packet with multiple assignments."""
        # Setup mock
        mock_html_instance = Mock()
        mock_html.return_value = mock_html_instance
        
        # Create second assignment
        assignment2 = Assignment(
            title="Science Quiz",
            subject="Science",
            difficulty="Intermediate",
            questions=["What is photosynthesis?", "Name three states of matter."],
            instructions="Answer in complete sentences."
        )
        
        # Mock no styles
        with patch('pathlib.Path.exists', return_value=False):
            
            template_content = "<div>{title}: {questions}</div>"
            output_path = Path("/tmp/test_multi_packet.pdf")
            
            self.generator.generate_packet_pdf(
                [self.sample_assignment, assignment2], 
                output_path, 
                template_content
            )
            
            # Get the HTML content
            call_args = mock_html.call_args[1]
            html_content = call_args['string']
            
            # Verify both assignments are present
            assert "Sample Math Assignment" in html_content
            assert "Science Quiz" in html_content
            
            # Verify page break is added between assignments
            assert 'page-break-before: always' in html_content
    
    def test_format_questions_html_with_questions(self):
        """Test formatting questions as HTML list."""
        questions = ["Question 1", "Question 2", "Question 3"]
        result = self.generator._format_questions_html(questions)
        
        assert result.startswith("<ol>")
        assert result.endswith("</ol>")
        assert "<li>Question 1</li>" in result
        assert "<li>Question 2</li>" in result
        assert "<li>Question 3</li>" in result
    
    def test_format_questions_html_empty_list(self):
        """Test formatting empty questions list."""
        questions = []
        result = self.generator._format_questions_html(questions)
        
        assert result == "<p>No questions available.</p>"
    
    def test_load_styles_file_exists(self):
        """Test loading styles when file exists."""
        css_content = "body { margin: 0; }"
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.read_text', return_value=css_content):
            
            result = self.generator._load_styles()
            assert result == css_content
    
    def test_load_styles_file_not_exists(self):
        """Test loading styles when file doesn't exist."""
        with patch('pathlib.Path.exists', return_value=False):
            result = self.generator._load_styles()
            assert result == ""
    
    def test_load_styles_read_error(self):
        """Test handling error when reading styles file."""
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.read_text', side_effect=OSError("Permission denied")):
            
            # Should not raise exception, just return empty string
            result = self.generator._load_styles()
            assert result == ""
    
    def test_pdf_generator_initialization(self):
        """Test PDFGenerator initialization."""
        # Test with default styles path
        generator = PDFGenerator()
        assert generator.styles_path == Path("templates/styles.css")
        
        # Test with custom styles path
        custom_path = Path("custom/styles.css")
        generator = PDFGenerator(styles_path=custom_path)
        assert generator.styles_path == custom_path
