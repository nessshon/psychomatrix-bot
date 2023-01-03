from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

from . import config


def loader() -> tuple[AsyncEngine, sessionmaker]:
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{config.DB_PATH}",
        pool_pre_ping=True
    )
    async_sessionmaker = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    return engine, async_sessionmaker


async def run(engine: AsyncEngine):
    async with engine.begin() as conn:
        from .base import Base
        await conn.run_sync(Base.metadata.create_all)
