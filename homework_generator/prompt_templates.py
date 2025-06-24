"""Template system for LLM prompts."""

from pathlib import Path
import jinja2


class PromptTemplateManager:
    """Manages prompt templates and rendering."""

    def __init__(self, templates_dir: Path = Path("templates/prompts")):
        self.templates_dir = templates_dir
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_dir),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
        )

    def get_available_templates(self) -> list[str]:
        """Get list of available template names."""
        if not self.templates_dir.exists():
            return []
        return [f.stem for f in self.templates_dir.glob("*.md")]

    def render_template(self, template_name: str, **kwargs) -> str:
        """Render a template with given parameters."""
        try:
            template = self.env.get_template(f"{template_name}.md")
            return template.render(**kwargs)
        except jinja2.TemplateNotFound:
            # Fall back to generic template
            template = self.env.get_template("generic.md")
            return template.render(**kwargs)
