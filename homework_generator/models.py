"""Data models for homework assignments and packets."""

from typing import List, Optional
from pydantic import BaseModel, Field


class AssignmentRequest(BaseModel):
    """Request model for generating an assignment."""

    topic: str = Field(..., description="The topic or subject for the assignment")
    subject: str = Field(..., description="Subject area (e.g., Mathematics, Science)")
    difficulty: str = Field(..., description="Difficulty level (Easy, Medium, Hard)")
    grade_level: str = Field(..., description="Target grade level")
    num_questions: int = Field(
        default=10, description="Number of questions to generate"
    )
    special_instructions: Optional[str] = Field(
        default=None, description="Special instructions"
    )


class Assignment(BaseModel):
    """Represents a single homework assignment."""

    title: str = Field(..., description="Assignment title")
    subject: str = Field(..., description="Subject area")
    difficulty: str = Field(..., description="Difficulty level")
    questions: List[str] = Field(
        ..., min_length=1, description="List of questions/problems"
    )
    instructions: Optional[str] = Field(
        default=None, description="Assignment instructions"
    )
    grade_level: Optional[str] = Field(default=None, description="Target grade level")
    estimated_time: Optional[str] = Field(
        default=None, description="Estimated completion time"
    )
    materials_needed: Optional[List[str]] = Field(
        default=None, description="Required materials"
    )
    learning_objectives: Optional[List[str]] = Field(
        default=None, description="Learning objectives"
    )


class HomeworkPacket(BaseModel):
    """Represents a complete homework packet containing multiple assignments."""

    assignments: List[Assignment] = Field(..., description="List of assignments")
    topic: str = Field(..., description="Overall topic/theme")
    generated_at: str = Field(..., description="Generation timestamp")
    model_used: str = Field(..., description="LLM model used for generation")

    @property
    def assignment_count(self) -> int:
        """Return the number of assignments in the packet."""
        return len(self.assignments)
