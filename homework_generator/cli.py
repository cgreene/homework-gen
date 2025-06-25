"""Command-line interface for the homework generator.

This module provides a rich CLI experience using Click and Rich libraries,
with progress bars, error handling, and verbose output options.
"""

import click
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.progress import Progress
from datetime import datetime

from .config import load_config
from .llm_client import LLMClient
from .content_generator import ContentGenerator
from .formatter import AssignmentFormatter
from .pdf_generator import PDFGenerator

# Global console for rich output
console = Console()


@click.command()
@click.argument("topic", type=str, required=False)
@click.option(
    "--count",
    "-c",
    default=5,
    show_default=True,
    help="Number of assignments to generate",
)
@click.option(
    "--difficulty",
    "-d",
    default="medium",
    show_default=True,
    type=click.Choice(["easy", "medium", "hard"], case_sensitive=False),
    help="Difficulty level (affects question count and complexity)",
)
@click.option(
    "--grade-level",
    "-g",
    default="5th Grade",
    show_default=True,
    help="Target grade level for assignments (e.g., '2nd Grade', 'Kindergarten', '8th Grade')",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output PDF file path (auto-generated if not specified)",
)
@click.option(
    "--model",
    "-m",
    default="gpt-3.5-turbo",
    show_default=True,
    help="LLM model to use for content generation",
)
@click.option(
    "--template",
    "-t",
    default="generic",
    show_default=True,
    help="Prompt template to use. Available: math, science, english, social_studies, computer_science, art, music, health, etc. Use --list-templates to see all options.",
)
@click.option(
    "--config", type=click.Path(exists=True), help="Path to configuration file"
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output with detailed progress information",
)
@click.option(
    "--list-templates",
    is_flag=True,
    help="List all available prompt templates and exit",
)
def main(
    topic: Optional[str],
    count: int,
    difficulty: str,
    grade_level: str,
    output: Optional[str],
    model: str,
    template: str,
    config: Optional[str],
    verbose: bool,
    list_templates: bool,
) -> None:
    """Generate homework packets using AI.

    This command generates professional homework assignments based on a topic description.
    The system uses OpenAI's GPT models to create age-appropriate content, then formats
    it into a beautiful PDF suitable for printing.

    TOPIC is the subject or description for the homework assignments.
    Examples: "fractions", "photosynthesis", "World War 2 timeline"

    \b
    Template Usage:
      Use --template to specify a subject-specific template for better results:
      homework-gen "algebra" --template math --grade-level "8th Grade"
      homework-gen "photosynthesis" --template science --grade-level "7th Grade"
      homework-gen "creative writing" --template english --grade-level "6th Grade"

    \b
    Examples:
      homework-gen "algebra basics" --count 3 --difficulty easy --grade-level "8th Grade"
      homework-gen "cell biology" --grade-level "7th Grade" --verbose
      homework-gen "creative writing prompts" --grade-level "3rd Grade" --output stories.pdf
    """
    if list_templates:
        # List available templates and exit
        from .prompt_templates import PromptTemplateManager
        template_manager = PromptTemplateManager()
        templates = template_manager.get_available_templates()
        
        console.print("[bold green]Available Prompt Templates:[/bold green]")
        console.print()
        for template_name in sorted(templates):
            console.print(f"  [blue]{template_name}[/blue]")
        console.print()
        console.print("[dim]Use with: homework-gen \"topic\" --template TEMPLATE_NAME --grade-level \"Grade\"[/dim]")
        return

    if not topic:
        raise click.ClickException("TOPIC is required when not using --list-templates")

    if verbose:
        console.print(
            f"[bold green]📚 Generating {count} {difficulty} assignments on: {topic}"
        )

    try:
        # Load configuration
        config_path = Path(config) if config else None
        app_config = load_config(config_path)

        if verbose:
            console.print(f"Using model: {model}")
            console.print(f"Using template: {template}")
            console.print(f"Grade level: {grade_level}")

        # Determine output path
        if not output:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_topic = "".join(
                c for c in topic if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()
            safe_topic = safe_topic.replace(" ", "_")[:30]  # Limit length
            output = f"homework_packet_{safe_topic}_{timestamp}.pdf"

        output_path = Path(output)

        # Initialize components
        llm_client = LLMClient(
            api_key=app_config.llm.api_key,
            model=model,
            base_url=app_config.llm.base_url,
        )

        content_generator = ContentGenerator(
            llm_client=llm_client
        )

        formatter = AssignmentFormatter(template_dir="templates")
        pdf_generator = PDFGenerator(styles_path=Path("templates/styles.css"))

        # Generate assignments with progress tracking
        with Progress() as progress:
            # Generate content
            task1 = progress.add_task(
                "[green]Generating assignment content...", total=1
            )

            try:
                assignments = content_generator.generate_assignments(
                    topic=topic,
                    count=count,
                    difficulty=difficulty,
                    grade_level=grade_level,
                    template=template,
                )
                progress.update(task1, advance=1)
            except Exception as e:
                raise click.ClickException(f"Failed to generate assignments: {e}")

            if not assignments:
                raise click.ClickException("Failed to generate any assignments")

            # Format assignments to HTML
            task2 = progress.add_task("[green]Formatting assignments...", total=1)

            combined_html = formatter.format_packet(assignments)

            progress.update(task2, advance=1)

            # Generate PDF
            task3 = progress.add_task("[green]Generating PDF...", total=1)

            pdf_generator.generate_pdf(
                html_content=combined_html, output_path=output_path
            )

            progress.update(task3, advance=1)

        # Success message
        console.print(
            f"[bold green]✓ Generated {len(assignments)} assignments in PDF: {output_path}"
        )

        if verbose:
            console.print(f"Output file size: {output_path.stat().st_size} bytes")
            for i, assignment in enumerate(assignments, 1):
                console.print(
                    f"Assignment {i}: {assignment.title} ({len(assignment.questions)} questions)"
                )

    except Exception as e:
        console.print(f"[bold red]Error: {e}")
        if verbose:
            import traceback

            console.print(traceback.format_exc())
        raise click.ClickException(str(e))

if __name__ == "__main__":
    main()