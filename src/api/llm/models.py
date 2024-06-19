from openai import BaseModel


class Prompt(BaseModel):
    type: str = "text"
    text: str


class Answer(BaseModel):
    id: int
    question: str
    project_id: int
    answer: str
