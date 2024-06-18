from typing import Any, List, Union
from urllib.parse import quote_plus
import asyncpg

from fastapi import Request
from api.config.config import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
logger
)


def connection_string(
    *,
    user: str = POSTGRES_USER,
    password: str = POSTGRES_PASSWORD,
    host: str = POSTGRES_HOST,
    port: str = POSTGRES_PORT,
    db: str = POSTGRES_DB,
) -> str:
    logger.info(f"Connecting with {user}:{password}@{host}:{port}/{db}")
    return f"postgresql://{user}:{quote_plus(password)}@{host}:{port}/{db}"


class Database:
    def __init__(self, dsn: str, min_size: int = 5, max_size: int = 100) -> None:
        self.dsn = dsn
        self.pool: asyncpg.Pool | None
        self.min_size = min_size
        self.max_size = max_size

    async def connect(self) -> None:
        self.pool = await asyncpg.create_pool(
            self.dsn, min_size=self.min_size, max_size=self.max_size
        )

    async def disconnect(self) -> None:
        if self.pool:
            await self.pool.close()

    async def execute(self, query: str, *args: Any, **kwargs: Any) -> None:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query, *args, **kwargs)

    async def executemany(self, query: str, *args: Any, **kwargs: Any) -> None:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.executemany(query, *args, **kwargs)

    async def fetch_all(
        self, query: str, *args: Any, **kwargs: Any
    ) -> List[asyncpg.Record]:
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args, **kwargs)

    async def fetch_one(
        self, query: str, *args: Any, **kwargs: Any
    ) -> asyncpg.Record | None:
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args, **kwargs)

    async def fetch_val(
        self, query: str, *args: Any, **kwargs: Any
    ) -> Union[Any, None]:
        result = await self.fetch_one(query, *args, **kwargs)
        if result:
            return result[0]
        else:
            return None


def get_db(request: Request) -> Database:
    logger.debug("Getting db connection")
    return request.app.state.db  # type: ignore[unused-ignore, no-any-return]
