from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from core.config import Config

db_url = Config.DB_URL

def get_engine():
    db_engine = create_async_engine(db_url, pool_pre_ping=True, connect_args={"ssl": True})
    return db_engine

async_engine = get_engine()

AsyncSessionFactory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as db:
        yield db
