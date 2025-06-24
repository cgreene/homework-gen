"""Content generation and assignment creation."""

import json
from typing import List, Dict, Any
from datetime import datetime

try:
    import jsonschema

    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

from .models import Assignment, HomeworkPacket
from .llm_client import LLMClient
from .prompt_templates import PromptTemplateManager


# JSON Schema for validating LLM responses
ASSIGNMENT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "assignments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "grade_level": {"type": "string"},
                    "subject": {"type": "string"},
                    "difficulty": {
                        "type": "string",
                        "enum": ["Easy", "Medium", "Hard"],
                    },
                    "estimated_time": {"type": "string"},
                    "instructions": {"type": "string"},
                    "questions": {"type": "array", "items": {"type": "string"}},
                    "materials_needed": {"type": "array", "items": {"type": "string"}},
                    "learning_objectives": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": [
                    "title",
                    "grade_level",
                    "subject",
                    "difficulty",
                    "instructions",
                    "questions",
                ],
            },
        }
    },
    "required": ["assignments"],
}


class ContentGenerator:
    """Generates homework content using LLM."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.template_manager = PromptTemplateManager()

    def generate_assignments(
        self,
        topic: str,
        count: int,
        difficulty: str,
        grade_level: str,
        template: str = "generic",
    ) -> List[Assignment]:
        """Generate assignments based on parameters."""

        # Create the prompt using template
        prompt = self._build_prompt(
            template=template,
            topic=topic,
            count=count,
            difficulty=difficulty,
            grade_level=grade_level,
        )

        # Get response from LLM
        response = self.llm_client.generate_response(prompt)

        # Validate and parse response
        validated_data = self._validate_response(response)

        # Convert to Assignment objects
        assignments = []
        for assignment_data in validated_data["assignments"]:
            assignment = Assignment(**assignment_data)
            assignments.append(assignment)

        return assignments

    def generate_homework_packet(
        self,
        topic: str,
        count: int,
        difficulty: str,
        grade_level: str,
        template: str = "generic",
    ) -> HomeworkPacket:
        """Generate a complete homework packet."""

        assignments = self.generate_assignments(
            topic=topic,
            count=count,
            difficulty=difficulty,
            grade_level=grade_level,
            template=template,
        )

        packet = HomeworkPacket(
            assignments=assignments,
            topic=topic,
            generated_at=datetime.now().isoformat(),
            model_used=self.llm_client.model,
        )

        return packet

    def _build_prompt(
        self, template: str, topic: str, count: int, difficulty: str, grade_level: str
    ) -> str:
        """Build the complete prompt for the LLM."""

        # Render the template content
        template_content = self.template_manager.render_template(
            template,
            topic=topic,
            count=count,
            difficulty=difficulty,
            grade_level=grade_level,
        )

        # Build the complete prompt
        system_message = "You are an expert educator creating homework assignments."

        json_schema = json.dumps(ASSIGNMENT_SCHEMA, indent=2)

        # TODO: Load few-shot examples from templates/examples/{template}.json
        examples = self._get_examples(template)

        prompt = f"""
{system_message}

{template_content}

OUTPUT FORMAT:
You must respond with valid JSON containing an array of assignments.
Each assignment must follow this exact structure:

{json_schema}

EXAMPLES:
{examples}

USER REQUEST: {topic}

Remember: Respond ONLY with valid JSON. No additional text or explanations.
"""

        return prompt.strip()

    def _validate_response(self, response: str) -> Dict[str, Any]:
        """Validate LLM response against JSON schema."""
        try:
            # Parse JSON
            data = json.loads(response)
        except json.JSONDecodeError as e:
            # Try to extract JSON from response if it's wrapped in text
            data = self._extract_json_from_text(response)
            if not data:
                raise ValueError(f"Invalid JSON response: {e}")

        # Validate against schema if jsonschema is available
        if JSONSCHEMA_AVAILABLE:
            try:
                jsonschema.validate(data, ASSIGNMENT_SCHEMA)
            except jsonschema.ValidationError as e:
                raise ValueError(f"Response doesn't match schema: {e}")

        # Basic validation if jsonschema not available
        if "assignments" not in data:
            raise ValueError("Response missing 'assignments' field")

        if not isinstance(data["assignments"], list):
            raise ValueError("'assignments' must be a list")

        # Validate each assignment has required fields
        for i, assignment in enumerate(data["assignments"]):
            required_fields = [
                "title",
                "grade_level",
                "subject",
                "difficulty",
                "instructions",
                "questions",
            ]
            for field in required_fields:
                if field not in assignment:
                    raise ValueError(f"Assignment {i} missing required field: {field}")

        return data

    def _extract_json_from_text(self, text: str) -> Dict[str, Any]:
        """Try to extract JSON from text that might contain extra content."""
        import re

        # Look for JSON-like structure
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        return None

    def _get_examples(self, template: str) -> str:
        """Get few-shot examples for the template."""
        # TODO: Load from templates/examples/{template}.json
        # For now, return basic example
        return json.dumps(
            {
                "assignments": [
                    {
                        "title": "Example Assignment",
                        "grade_level": "5th Grade",
                        "subject": "Mathematics",
                        "difficulty": "Medium",
                        "estimated_time": "15 minutes",
                        "instructions": "Complete the following problems.",
                        "questions": ["Example problem 1", "Example problem 2"],
                        "materials_needed": ["pencil"],
                        "learning_objectives": ["Example objective"],
                    }
                ]
            },
            indent=2,
        )
