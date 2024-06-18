from openai import BaseModel


class Prompt(BaseModel):
    type: str = "text"
    text: str
