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


class Questionnaire(BaseModel):
    questions: List[Question]
