#!/usr/bin/env python3
"""Demo script to show the homework generator in action."""

import sys
from pathlib import Path
from datetime import datetime

# Add the homework_generator to Python path
sys.path.insert(0, str(Path(__file__).parent))

from homework_generator.models import Assignment
from homework_generator.formatter import AssignmentFormatter
from homework_generator.pdf_generator import PDFGenerator


def create_sample_assignments():
    """Create sample assignments for demonstration."""
    
    math_assignment = Assignment(
        title="Fraction Practice",
        subject="Mathematics",
        difficulty="Medium",
        questions=[
            "What is 1/2 + 1/4? (Hint: Find a common denominator)",
            "Simplify the fraction 8/12",
            "Convert 3/4 to a decimal",
            "Which is larger: 2/3 or 3/5?",
            "If you eat 1/3 of a pizza and your friend eats 1/4, how much pizza is left?"
        ],
        instructions="Show all your work. Use diagrams if they help you solve the problems.",
        grade_level="5th Grade",
        estimated_time="20 minutes",
        materials_needed=["pencil", "paper", "calculator (optional)"],
        learning_objectives=[
            "Add fractions with different denominators",
            "Simplify fractions to lowest terms",
            "Convert fractions to decimals",
            "Compare fractions"
        ]
    )
    
    science_assignment = Assignment(
        title="Plant Life Cycle Observation",
        subject="Science",
        difficulty="Easy",
        questions=[
            "What are the four main stages of a plant's life cycle?",
            "Draw and label a seed. What does it need to grow?",
            "What happens during germination?",
            "Name three things plants need to survive and grow",
            "Look outside and find a plant. What stage of life do you think it's in? Why?"
        ],
        instructions="Complete all questions. For drawing questions, use colors and labels.",
        grade_level="3rd Grade",
        estimated_time="15 minutes",
        materials_needed=["colored pencils", "paper", "access to outdoors or window"],
        learning_objectives=[
            "Identify stages of plant life cycle",
            "Understand basic plant needs",
            "Practice scientific observation"
        ]
    )
    
    return [math_assignment, science_assignment]


def generate_sample_homework_packet():
    """Generate a sample homework packet."""
    
    print("📚 Generating sample homework packet...")
    
    # Create assignments
    assignments = create_sample_assignments()
    print(f"   Created {len(assignments)} assignments")
    
    # Format to HTML
    formatter = AssignmentFormatter()
    print("   Formatting assignments to HTML...")
    
    combined_html = formatter.format_packet(assignments)
    print(f"   ✓ HTML generated ({len(combined_html)} characters)")
    
    # Generate PDF
    print("   Generating PDF...")
    pdf_generator = PDFGenerator()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f"demo_homework_packet_{timestamp}.pdf")
    
    try:
        pdf_generator.generate_pdf(combined_html, output_path)
        print(f"   ✓ PDF generated: {output_path}")
        
        if output_path.exists():
            file_size = output_path.stat().st_size
            print(f"   📄 File size: {file_size:,} bytes")
            return output_path
        else:
            print("   ⚠️  PDF file not found after generation")
            return None
            
    except Exception as e:
        print(f"   ❌ PDF generation failed: {e}")
        print("   💡 This might be due to missing system dependencies for WeasyPrint")
        print("   🔍 WeasyPrint requires system libraries for PDF generation")
        
        # Save HTML instead
        html_path = output_path.with_suffix('.html')
        html_path.write_text(combined_html, encoding='utf-8')
        print(f"   💾 Saved HTML version instead: {html_path}")
        return html_path


def show_assignment_preview():
    """Show a preview of formatted assignment."""
    
    print("\n🔍 Assignment Preview:")
    print("=" * 50)
    
    assignment = create_sample_assignments()[0]  # Get the math assignment
    
    formatter = AssignmentFormatter()
    markdown_preview = formatter.format_to_markdown(assignment)
    
    print(markdown_preview)
    print("=" * 50)


if __name__ == "__main__":
    print("🚀 Homework Generator Demo\n")
    
    try:
        # Show what a formatted assignment looks like
        show_assignment_preview()
        
        # Generate actual packet
        output_file = generate_sample_homework_packet()
        
        if output_file:
            print(f"\n✅ Demo completed successfully!")
            print(f"📁 Output file: {output_file.absolute()}")
            
            if output_file.suffix == '.html':
                print("💡 Open the HTML file in your browser to see the formatted homework packet")
            else:
                print("📖 You can open the PDF to see the homework packet")
        else:
            print("\n⚠️  Demo completed with warnings")
            
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
