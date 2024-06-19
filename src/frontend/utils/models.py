from pydantic import BaseModel


class NewProjectResponse(BaseModel):
    project_id: int
