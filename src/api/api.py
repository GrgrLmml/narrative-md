from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Request

from api.config.config import logger
from api.db.postgres_engine import (
    connection_string,
    Database,
)
from api.endpoints.questionnaire import router as q_router


def app_factory() -> FastAPI:
    app = FastAPI(title="Moveflow Analytics Backend", debug=True, version="0.1.0")
    app.include_router(q_router)
    return app


app = app_factory()



@app.on_event("startup")  # type: ignore[unused-ignore]
async def startup_event() -> None:
    await app_startup(app)


@app.on_event("shutdown")  # type: ignore[unused-ignore]
async def shutdown_event() -> None:
    await app_shutdown(app)



async def app_startup(app: FastAPI) -> None:
    logger.info("Starting up application")
    logger.info("Loading database")
    app.state.db = Database(connection_string(), min_size=5, max_size=200)
    await app.state.db.connect()
    scheduler = AsyncIOScheduler()
    scheduler.start()
    app.state.scheduler = scheduler
    logger.info("Application is ready")


async def app_shutdown(app: FastAPI) -> None:
    app.state.scheduler.shutdown()


