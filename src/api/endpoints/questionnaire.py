import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from api.config.config import logger
from api.db.postgres_engine import Database, get_db
from api.endpoints.models import OnboardProject, Questionnaire, Segment
from api.llm.openai import questionnaire

router = APIRouter(prefix="/questionnaire", tags=["questionnaire"])


@router.post("/new")
async def create_questionnaire(request: OnboardProject, db: Database = Depends(get_db)) -> Any:
    logger.info(f"Creating new questionnaire for project {request.name}")
    try:
        query = """
        INSERT INTO project (name, description)
        VALUES ($1, $2)
        ON CONFLICT (name) DO UPDATE SET
        description = EXCLUDED.description
        RETURNING id
        """
        project_id = await db.fetch_val(query, request.name, request.questions)
        logger.info(f"Project {request.name} successfully created or updated with id {project_id}")
        q: Questionnaire = await questionnaire(request)

        values_to_insert = []
        for question in q.questions:
            # Convert the list of options to a JSON string
            options_json = json.dumps(question.options) if question.options else None

            # Create a tuple for each question
            question_tuple = (project_id, question.question, question.kind, question.condition, options_json)
            values_to_insert.append(question_tuple)

        # TODO: queries should be transactional
        query2 = """
        INSERT INTO questions (project_id, question, kind, condition, options)
        VALUES ($1, $2, $3, $4, $5)
        """
        await db.execute("DELETE FROM questions WHERE project_id = $1", project_id)
        await db.executemany(query2, values_to_insert)
        logger.info(
            f"Questionnaire for project {request.name} and id {project_id} successfully created or updated. Number of questions: {len(q.questions)}")
    except Exception as e:
        logger.error(f"Failed to create or update questionnaire for project {request.name}: {e}")
        raise HTTPException(status_code=400, detail="Error updating or inserting the project.") from e

    return {"project_id": project_id}


@router.post("/segment")
async def segment(request: Segment, db: Database = Depends(get_db)) -> Any:

    query = """
    INSERT INTO segments (project_id, segment)
    VALUES ($1, $2)
    """
    await db.execute(query, request.project_id, request.segment)
    logger.info(f"""Received segment "{request.segment}" for project {request.project_id}""")
    return {"success": True}