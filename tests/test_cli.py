"""Tests for CLI module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from click.testing import CliRunner
from pathlib import Path
from homework_generator.cli import main, _detect_subject, _get_question_count
from homework_generator.models import Assignment


class TestCLI:
    """Test cases for CLI functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        
        # Sample assignment for mocking
        self.sample_assignment = Assignment(
            title="Test Assignment",
            subject="Mathematics",
            difficulty="Medium",
            questions=["Question 1", "Question 2"],
            instructions="Complete all problems."
        )
    
    @patch('homework_generator.cli.load_config')
    @patch('homework_generator.cli.LLMClient')
    @patch('homework_generator.cli.ContentGenerator')
    @patch('homework_generator.cli.AssignmentFormatter')
    @patch('homework_generator.cli.PDFGenerator')
    def test_main_command_success(self, mock_pdf_gen, mock_formatter, 
                                 mock_content_gen, mock_llm_client, mock_load_config):
        """Test successful execution of main command."""
        # Setup mocks
        mock_config = Mock()
        mock_config.llm.api_key = "test-key"
        mock_config.llm.base_url = None
        mock_load_config.return_value = mock_config
        
        mock_llm_instance = Mock()
        mock_llm_client.return_value = mock_llm_instance
        
        mock_content_gen_instance = Mock()
        mock_content_gen_instance.generate_assignment.return_value = self.sample_assignment
        mock_content_gen.return_value = mock_content_gen_instance
        
        mock_formatter_instance = Mock()
        mock_formatter_instance.format_packet.return_value = "<html><body><h1>Test</h1></body></html>"
        mock_formatter.return_value = mock_formatter_instance
        
        mock_pdf_gen_instance = Mock()
        mock_pdf_gen.return_value = mock_pdf_gen_instance
        
        # Mock file operations
        with patch('pathlib.Path.stat') as mock_stat:
            mock_stat.return_value.st_size = 1024
            
            result = self.runner.invoke(main, ['algebra problems', '--count', '2', '--verbose'])
            
            assert result.exit_code == 0
            assert "Generating 2 medium assignments on: algebra problems" in result.output
            assert "Generated 2 assignments in PDF" in result.output
    
    @patch('homework_generator.cli.load_config')
    def test_main_command_with_custom_options(self, mock_load_config):
        """Test main command with custom options."""
        mock_config = Mock()
        mock_config.llm.api_key = "test-key"
        mock_config.llm.base_url = None
        mock_load_config.return_value = mock_config
        
        with patch('homework_generator.cli.LLMClient'), \
             patch('homework_generator.cli.ContentGenerator') as mock_content_gen, \
             patch('homework_generator.cli.AssignmentFormatter'), \
             patch('homework_generator.cli.PDFGenerator'), \
             patch('pathlib.Path.stat') as mock_stat:
            
            mock_stat.return_value.st_size = 2048
            
            mock_content_gen_instance = Mock()
            mock_content_gen_instance.generate_assignment.return_value = self.sample_assignment
            mock_content_gen.return_value = mock_content_gen_instance
            
            result = self.runner.invoke(main, [
                'geometry',
                '--count', '3',
                '--difficulty', 'hard',
                '--grade-level', '8th Grade',
                '--output', 'custom_output.pdf',
                '--model', 'gpt-4',
                '--template', 'math',
                '--verbose'
            ])
            
            assert result.exit_code == 0
            assert "Generating 3 hard assignments on: geometry" in result.output
            assert "Using model: gpt-4" in result.output
            assert "Grade level: 8th Grade" in result.output
    
    @patch('homework_generator.cli.load_config')
    @patch('homework_generator.cli.LLMClient')
    @patch('homework_generator.cli.ContentGenerator')
    def test_main_command_generation_failure(self, mock_content_gen, mock_llm_client, mock_load_config):
        """Test handling of assignment generation failure."""
        # Setup mocks
        mock_config = Mock()
        mock_config.llm.api_key = "test-key"
        mock_config.llm.base_url = None
        mock_load_config.return_value = mock_config
        
        mock_content_gen_instance = Mock()
        mock_content_gen_instance.generate_assignment.side_effect = Exception("Generation failed")
        mock_content_gen.return_value = mock_content_gen_instance
        
        result = self.runner.invoke(main, ['test topic', '--count', '1'])
        
        assert result.exit_code == 1
        assert "Failed to generate any assignments" in result.output
    
    @patch('homework_generator.cli.load_config')
    def test_main_command_config_error(self, mock_load_config):
        """Test handling of configuration loading error."""
        mock_load_config.side_effect = Exception("Config file not found")
        
        result = self.runner.invoke(main, ['test topic'])
        
        assert result.exit_code == 1
        assert "Error: Config file not found" in result.output
    
    def test_detect_subject_math(self):
        """Test subject detection for mathematics."""
        assert _detect_subject("algebra problems") == "Mathematics"
        assert _detect_subject("geometry shapes") == "Mathematics"
        assert _detect_subject("calculus derivatives") == "Mathematics"
        assert _detect_subject("arithmetic operations") == "Mathematics"
    
    def test_detect_subject_science(self):
        """Test subject detection for science."""
        assert _detect_subject("biology cells") == "Science"
        assert _detect_subject("chemistry reactions") == "Science"
        assert _detect_subject("physics motion") == "Science"
        assert _detect_subject("science experiment") == "Science"
    
    def test_detect_subject_english(self):
        """Test subject detection for English."""
        assert _detect_subject("english grammar") == "English"
        assert _detect_subject("writing essays") == "English"
        assert _detect_subject("literature analysis") == "English"
        assert _detect_subject("reading comprehension") == "English"
    
    def test_detect_subject_history(self):
        """Test subject detection for history."""
        assert _detect_subject("american history") == "History"
        assert _detect_subject("world geography") == "History"
        assert _detect_subject("government systems") == "History"
        assert _detect_subject("social studies") == "History"
    
    def test_detect_subject_general(self):
        """Test subject detection fallback to general."""
        assert _detect_subject("random topic") == "General"
        assert _detect_subject("computer programming") == "General"
        assert _detect_subject("art appreciation") == "General"
    
    def test_get_question_count(self):
        """Test question count based on difficulty."""
        assert _get_question_count("easy") == 8
        assert _get_question_count("medium") == 10
        assert _get_question_count("hard") == 12
        assert _get_question_count("unknown") == 10  # default
    
    def test_get_question_count_case_insensitive(self):
        """Test question count is case insensitive."""
        assert _get_question_count("EASY") == 8
        assert _get_question_count("Medium") == 10
        assert _get_question_count("HARD") == 12
    
    @patch('homework_generator.cli.load_config')
    @patch('homework_generator.cli.LLMClient')
    @patch('homework_generator.cli.ContentGenerator')
    @patch('homework_generator.cli.AssignmentFormatter')
    @patch('homework_generator.cli.PDFGenerator')
    def test_output_filename_generation(self, mock_pdf_gen, mock_formatter, 
                                      mock_content_gen, mock_llm_client, mock_load_config):
        """Test automatic output filename generation."""
        # Setup mocks
        mock_config = Mock()
        mock_config.llm.api_key = "test-key"
        mock_config.llm.base_url = None
        mock_load_config.return_value = mock_config
        
        mock_content_gen_instance = Mock()
        mock_content_gen_instance.generate_assignment.return_value = self.sample_assignment
        mock_content_gen.return_value = mock_content_gen_instance
        
        mock_formatter_instance = Mock()
        mock_formatter_instance.format_packet.return_value = "<html><body><h1>Test</h1></body></html>"
        mock_formatter.return_value = mock_formatter_instance
        
        # Mock datetime to get predictable filename
        with patch('homework_generator.cli.datetime') as mock_datetime, \
             patch('pathlib.Path.stat') as mock_stat:
            
            mock_datetime.now.return_value.strftime.return_value = "20231201_143000"
            mock_stat.return_value.st_size = 1024
            
            result = self.runner.invoke(main, ['algebra & geometry'])
            
            assert result.exit_code == 0
            # Check that a reasonable filename was generated
            assert "homework_packet_algebra__geometry_20231201_143000.pdf" in result.output
    
    def test_invalid_difficulty_option(self):
        """Test handling of invalid difficulty option."""
        result = self.runner.invoke(main, ['test topic', '--difficulty', 'invalid'])
        
        assert result.exit_code == 2  # Click validation error
        assert "Invalid value for '--difficulty'" in result.output
    
    @patch('homework_generator.cli.load_config')
    @patch('homework_generator.cli.LLMClient')
    @patch('homework_generator.cli.ContentGenerator')
    @patch('homework_generator.cli.AssignmentFormatter')
    @patch('homework_generator.cli.PDFGenerator')
    def test_partial_assignment_generation(self, mock_pdf_gen, mock_formatter, 
                                         mock_content_gen, mock_llm_client, mock_load_config):
        """Test handling when some assignments fail to generate."""
        # Setup mocks
        mock_config = Mock()
        mock_config.llm.api_key = "test-key"
        mock_config.llm.base_url = None
        mock_load_config.return_value = mock_config
        
        # Mock content generator to fail on second call
        mock_content_gen_instance = Mock()
        mock_content_gen_instance.generate_assignment.side_effect = [
            self.sample_assignment,  # First call succeeds
            Exception("Failed"),     # Second call fails
            self.sample_assignment   # Third call succeeds
        ]
        mock_content_gen.return_value = mock_content_gen_instance
        
        mock_formatter_instance = Mock()
        mock_formatter_instance.format_packet.return_value = "<html><body><h1>Test</h1></body></html>"
        mock_formatter.return_value = mock_formatter_instance
        
        with patch('pathlib.Path.stat') as mock_stat:
            mock_stat.return_value.st_size = 1024
            
            result = self.runner.invoke(main, ['test topic', '--count', '3', '--verbose'])
            
            assert result.exit_code == 0
            assert "Warning: Failed to generate assignment 2: Failed" in result.output
            assert "Generated 2 assignments in PDF" in result.output  # Only 2 succeeded
