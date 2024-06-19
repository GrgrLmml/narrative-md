from typing import List, Optional

from pydantic import BaseModel


class OnboardProject(BaseModel):
    name: str
    questions: str


class Question(BaseModel):
    question: str
    kind: str
    condition: Optional[str] = None
    options: Optional[List[str]] = None


class Answer(BaseModel):
    question: str
    answer: str
    project_id: int


class Questionnaire(BaseModel):
    questions: List[Question]


class Segment(BaseModel):
    id: Optional[int] = None
    segment: str
    project_id: int
    processed: Optional[bool] = False
