from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text, create_engine
from config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False
)

sync_engine = create_engine(
    url=settings.DATABASE_URL_syncpg,
    echo=True
)