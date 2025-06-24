#!/usr/bin/env python3
"""Simple integration test for the homework generator."""

import sys
from pathlib import Path

# Add the homework_generator to Python path
sys.path.insert(0, str(Path(__file__).parent))

from homework_generator.models import AssignmentRequest, Assignment
from homework_generator.config import load_config
from homework_generator.llm_client import LLMClient
from homework_generator.content_generator import ContentGenerator
from homework_generator.formatter import AssignmentFormatter
from homework_generator.pdf_generator import PDFGenerator


def test_basic_workflow():
    """Test basic homework generation workflow."""
    
    print("🚀 Testing basic homework generation workflow...")
    
    try:
        # 1. Load configuration
        print("1. Loading configuration...")
        config = load_config()
        print("   ✓ Configuration loaded")
        
        # 2. Create a simple assignment manually
        print("2. Creating assignment...")
        assignment = Assignment(
            title="Basic Math Practice",
            subject="Mathematics", 
            difficulty="Easy",
            questions=[
                "What is 2 + 3?",
                "What is 5 - 2?",
                "What is 4 × 2?"
            ],
            instructions="Solve each problem and show your work.",
            grade_level="2nd Grade"
        )
        print("   ✓ Assignment created")
        
        # 3. Format assignment to HTML
        print("3. Formatting to HTML...")
        formatter = AssignmentFormatter()
        html_content = formatter.format_assignment(assignment)
        print("   ✓ HTML formatting complete")
        print(f"   HTML length: {len(html_content)} characters")
        
        # 4. Generate PDF (without actually creating the file)
        print("4. Testing PDF generator...")
        pdf_generator = PDFGenerator()
        
        # Test the helper methods
        questions_html = pdf_generator._format_questions_html(assignment.questions)
        print(f"   ✓ Questions formatted: {len(questions_html)} chars")
        
        # Test styles loading
        styles = pdf_generator._load_styles()
        print(f"   ✓ Styles loaded: {len(styles)} chars")
        
        print("✅ Basic workflow test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cli_detection_functions():
    """Test CLI helper functions."""
    print("\n🔍 Testing CLI helper functions...")
    
    try:
        from homework_generator.cli import _detect_subject, _get_question_count
        
        # Test subject detection
        assert _detect_subject("algebra problems") == "Mathematics"
        assert _detect_subject("biology cells") == "Science"
        assert _detect_subject("random topic") == "General"
        print("   ✓ Subject detection working")
        
        # Test question count
        assert _get_question_count("easy") == 8
        assert _get_question_count("medium") == 10
        assert _get_question_count("hard") == 12
        print("   ✓ Question count logic working")
        
        print("✅ CLI helper functions test completed!")
        return True
        
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Running integration tests for homework generator\n")
    
    success = True
    success &= test_basic_workflow()
    success &= test_cli_detection_functions()
    
    if success:
        print("\n🎉 All integration tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)
