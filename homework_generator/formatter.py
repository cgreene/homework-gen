"""Markdown to HTML formatting for assignments."""

from typing import List
from pathlib import Path

try:
    import markdown
    import jinja2

    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False

from .models import Assignment


class AssignmentFormatter:
    """Formats assignments into HTML for PDF generation."""

    def __init__(self, template_dir: str = "templates"):
        self.template_dir = Path(template_dir)

        if DEPENDENCIES_AVAILABLE:
            self.md = markdown.Markdown(
                extensions=[
                    "extra",  # Tables, fenced code blocks, etc.
                    "codehilite",  # Syntax highlighting
                    "toc",  # Table of contents
                ]
            )

            # Load HTML template for assignments
            try:
                env = jinja2.Environment(
                    loader=jinja2.FileSystemLoader(template_dir),
                    autoescape=jinja2.select_autoescape(["html", "xml"]),
                )
                self.html_template = env.get_template("assignment.html")
            except (jinja2.TemplateNotFound, jinja2.loaders.TemplateNotFound):
                # Fallback to basic template
                self.html_template = None
        else:
            self.md = None
            self.html_template = None

    def format_assignment(self, assignment: Assignment) -> str:
        """Format a single assignment as HTML."""
        if not DEPENDENCIES_AVAILABLE or not self.html_template:
            return self._format_assignment_basic(assignment)

        # Load CSS styles
        styles = self._load_styles()

        # Render the assignment using the template
        html = self.html_template.render(
            title=assignment.title,
            grade_level=assignment.grade_level,
            subject=assignment.subject,
            difficulty=assignment.difficulty,
            estimated_time=assignment.estimated_time,
            instructions=assignment.instructions,
            problems=assignment.questions,  # Use questions field
            materials_needed=assignment.materials_needed or [],
            learning_objectives=assignment.learning_objectives or [],
            styles=styles,
        )

        return html

    def format_packet(self, assignments: List[Assignment]) -> str:
        """Format multiple assignments into a complete HTML document."""
        if not assignments:
            return "<html><body><p>No assignments to display.</p></body></html>"

        # Format each assignment
        assignment_htmls = []
        for assignment in assignments:
            assignment_html = self.format_assignment(assignment)
            assignment_htmls.append(assignment_html)

        # Combine into complete document
        if DEPENDENCIES_AVAILABLE:
            return self._combine_assignments_advanced(assignment_htmls)
        else:
            return self._combine_assignments_basic(assignment_htmls)

    def _format_assignment_basic(self, assignment: Assignment) -> str:
        """Basic assignment formatting without dependencies."""
        html = f"""
        <div class="assignment">
            <h1>{assignment.title}</h1>
            <div class="metadata">
                <p><strong>Grade Level:</strong> {assignment.grade_level}</p>
                <p><strong>Subject:</strong> {assignment.subject}</p>
                <p><strong>Difficulty:</strong> {assignment.difficulty}</p>
                <p><strong>Estimated Time:</strong> {assignment.estimated_time}</p>
            </div>
            
            <h2>Instructions</h2>
            <p>{assignment.instructions}</p>
            
            <h2>Problems</h2>
            <ol>
        """

        for problem in assignment.questions:  # Use questions field
            html += f"<li>{problem}</li>\n"

        html += "</ol>"

        if assignment.materials_needed:
            html += "<h2>Materials Needed</h2><ul>"
            for material in assignment.materials_needed:
                html += f"<li>{material}</li>"
            html += "</ul>"

        if assignment.learning_objectives:
            html += "<h2>Learning Objectives</h2><ul>"
            for objective in assignment.learning_objectives:
                html += f"<li>{objective}</li>"
            html += "</ul>"

        html += "</div>"
        return html

    def _combine_assignments_advanced(self, assignment_htmls: List[str]) -> str:
        """Combine assignments by concatenating HTML content."""
        # Create a complete HTML document
        base_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Homework Packet</title>
            <style>{styles}</style>
        </head>
        <body>
            {assignments}
        </body>
        </html>
        """

        styles = self._load_styles()
        assignments_content = "\n".join(assignment_htmls)

        return base_html.format(styles=styles, assignments=assignments_content)

    def _combine_assignments_basic(self, assignment_htmls: List[str]) -> str:
        """Basic assignment combination."""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Homework Packet</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .assignment { page-break-after: always; margin-bottom: 40px; }
                .assignment:last-child { page-break-after: avoid; }
                h1 { color: #333; border-bottom: 2px solid #ccc; }
                .metadata { background: #f5f5f5; padding: 10px; margin: 10px 0; }
                ol, ul { margin: 10px 0; }
            </style>
        </head>
        <body>
        """

        html += "\n".join(assignment_htmls)
        html += "</body></html>"

        return html

    def _load_styles(self) -> str:
        """Load CSS styles for assignment formatting."""
        styles_path = self.template_dir / "styles.css"

        if styles_path.exists():
            return styles_path.read_text()

        # Fallback styles
        return """
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            color: #333;
        }
        .assignment {
            page-break-after: always;
            margin-bottom: 40px;
        }
        .assignment:last-child {
            page-break-after: avoid;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        .metadata {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        h2 {
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }
        """

    def format_to_markdown(self, assignment: Assignment) -> str:
        """Format assignment as Markdown (useful for debugging/testing)."""
        md = f"# {assignment.title}\n\n"
        md += f"**Grade Level:** {assignment.grade_level}  \n"
        md += f"**Subject:** {assignment.subject}  \n"
        md += f"**Difficulty:** {assignment.difficulty}  \n"
        md += f"**Estimated Time:** {assignment.estimated_time}  \n\n"

        if assignment.learning_objectives:
            md += "## Learning Objectives\n\n"
            for objective in assignment.learning_objectives:
                md += f"- {objective}\n"
            md += "\n"

        md += "## Instructions\n\n"
        md += f"{assignment.instructions}\n\n"

        if assignment.materials_needed:
            md += "## Materials Needed\n\n"
            for material in assignment.materials_needed:
                md += f"- {material}\n"
            md += "\n"

        md += "## Problems\n\n"
        for i, problem in enumerate(assignment.questions, 1):  # Use questions field
            md += f"{i}. {problem}\n"

        return md
