import json
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from api.config.config import logger
from api.db.postgres_engine import Database
from api.endpoints.models import Segment
from api.llm.models import Answer
from api.llm.openai import answer_questions


async def process_segments_job(project_id: int, db: Database, scheduler: AsyncIOScheduler):
    logger.info(f"Processing segments for project {project_id}")
    query = """
        SELECT * FROM segments 
        WHERE project_id = $1
        ORDER BY created_at
    """
    segments = await db.fetch_all(query, project_id)
    segments = [Segment(**segment) for segment in segments]
    all_processed = all(segment.processed for segment in segments)
    if all_processed:
        logger.info("No new segments to process. Waiting for new segments...")
        return

    query2 = """
        SELECT * FROM questions WHERE project_id = $1
        ORDER BY id
    """
    questions = [dict(q) for q in await db.fetch_all(query2, project_id)]
    should_continue = any(q["answer"] == "n/a" for q in questions)
    if not should_continue:
        logger.info("No more processing needed. Exiting and removing job...")
        scheduler.remove_job(job_id=str(project_id))
        return  # Exit and remove the job from the scheduler

    logger.info("Processing segments...")
    transcript = '\n'.join([segment.segment for segment in segments])
    questionnaire = json.dumps(questions, indent=4)
    answers: [Answer] = [a for a in await answer_questions(transcript, questionnaire) if a.answer != "n/a"]
    logger.info(f"Received {len(answers)} answers")
    query3 = """
    UPDATE questions SET answer = $1 WHERE project_id = $2 AND id = $3
    """
    for a in answers:
        logger.info(f"Answering question {a}")
    await db.executemany(query3, [(a.answer, project_id, a.id) for a in answers])

    # query4 = """
    # UPDATE segments SET processed = true WHERE id = $1
    # """
    # await db.executemany(query4, [(s.id,) for s in segments])
