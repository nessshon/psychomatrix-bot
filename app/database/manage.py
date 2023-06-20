from environs import Env
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker


def loader() -> tuple[AsyncEngine, async_sessionmaker]:
    env = Env()
    env.read_env()

    engine = create_async_engine(
        f"mysql+aiomysql://"
        f"{env.str('DB_USER')}:"
        f"{env.str('DB_PASS')}@"
        f"{env.str('DB_HOST')}:"
        f"{env.int('DB_PORT')}/"
        f"{env.str('DB_NAME')}",
        pool_pre_ping=True,
    )
    sessionmaker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    return engine, sessionmaker


async def run(engine: AsyncEngine):
    async with engine.begin() as conn:
        from .base import Base
        await conn.run_sync(Base.metadata.create_all)
