import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from api.config.config import logger
from api.db.postgres_engine import Database
from api.endpoints.models import Segment


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



    should_continue = True
    if not should_continue:
        logger.info("No more processing needed. Exiting and removing job...")
        scheduler.remove_job(job_id=str(project_id))
        return  # Exit and remove the job from the scheduler

    logger.info("Processing segments...")
    # Process segments logic here
