
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

import os

from dotenv import load_dotenv

load_dotenv(override=True)


class Base(DeclarativeBase):
    pass


engine=create_async_engine(
    url=os.getenv("DATABASE_URI", "").strip(),
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
    # Important: Disable connection pooling for asyncpg to avoid concurrency issues
    pool_use_lifo=True,
)


def make_session():
    sess = AsyncSession(
        engine,
        expire_on_commit=False,
        autoflush=True
    )
    
    return sess