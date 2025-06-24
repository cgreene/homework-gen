"""PDF generation from HTML content."""

from pathlib import Path
from typing import List
from weasyprint import HTML, CSS
from .models import Assignment


class PDFGenerator:
    """Generates PDFs from HTML content."""

    def __init__(self, styles_path: Path = Path("templates/styles.css")):
        self.styles_path = styles_path

    def generate_pdf(self, html_content: str, output_path: Path) -> None:
        """Generate PDF from HTML content.

        Args:
            html_content: HTML content to convert to PDF
            output_path: Path where PDF should be saved
        """
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Load CSS styles
        css_content = self._load_styles()

        # Create HTML document
        html_doc = HTML(string=html_content)

        # Apply CSS if available
        if css_content:
            css_doc = CSS(string=css_content)
            html_doc.write_pdf(str(output_path), stylesheets=[css_doc])
        else:
            html_doc.write_pdf(str(output_path))

    def generate_packet_pdf(
        self, assignments: List[Assignment], output_path: Path, template_content: str
    ) -> None:
        """Generate a PDF packet from multiple assignments.

        Args:
            assignments: List of assignments to include
            output_path: Path where PDF should be saved
            template_content: HTML template for formatting assignments
        """
        # Combine all assignments into a single HTML document
        all_assignments_html = ""

        for i, assignment in enumerate(assignments):
            # Add page break before each assignment (except the first)
            if i > 0:
                all_assignments_html += '<div style="page-break-before: always;"></div>'

            # Format assignment using template
            assignment_html = template_content.format(
                title=assignment.title,
                subject=assignment.subject,
                difficulty=assignment.difficulty,
                questions=self._format_questions_html(assignment.questions),
                instructions=assignment.instructions or "",
            )
            all_assignments_html += assignment_html

        # Generate PDF from combined HTML
        self.generate_pdf(all_assignments_html, output_path)

    def _format_questions_html(self, questions: List[str]) -> str:
        """Format questions as HTML list.

        Args:
            questions: List of question strings

        Returns:
            HTML formatted questions
        """
        if not questions:
            return "<p>No questions available.</p>"

        html_questions = "<ol>"
        for question in questions:
            html_questions += f"<li>{question}</li>"
        html_questions += "</ol>"

        return html_questions

    def _load_styles(self) -> str:
        """Load CSS styles for PDF generation.

        Returns:
            CSS content as string, empty if file doesn't exist
        """
        try:
            if self.styles_path.exists():
                return self.styles_path.read_text(encoding="utf-8")
        except Exception as e:
            # Log warning but don't fail
            print(f"Warning: Could not load styles from {self.styles_path}: {e}")
        return ""
