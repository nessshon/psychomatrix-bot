from __future__ import annotations

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, select, func

from ..base import Base
from ..sessionmaker import async_sessionmaker


class User(Base):
    __tablename__ = "users"

    pk = Column(
        Integer,
        primary_key=True,
    )
    id = Column(
        BigInteger,
        unique=True,
        nullable=False
    )
    name = Column(
        String(length=64),
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True),
        default=func.now()
    )

    @classmethod
    async def add(cls, **kwargs) -> None:
        async with async_sessionmaker() as session:
            session.add(cls(**kwargs))
            await session.commit()

    @classmethod
    async def is_exists(cls, user_id: str | str) -> bool:
        async with async_sessionmaker() as session:
            query = await session.execute(
                select(cls.id).where(cls.id == user_id)
            )
            return query.scalar() is not None
