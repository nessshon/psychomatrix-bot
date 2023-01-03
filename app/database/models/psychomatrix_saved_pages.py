from __future__ import annotations

from sqlalchemy import Column, Integer, String, select

from ..base import Base
from ..sessionmaker import async_sessionmaker


class PsychomatrixSavedPage(Base):
    __tablename__ = 'psychomatrix_saved_pages'

    id = Column(
        Integer,
        primary_key=True
    )
    date = Column(
        String(length=8),
        nullable=False
    )
    title = Column(
        String(length=1024),
        nullable=False
    )
    url = Column(
        String(length=1024),
        nullable=False
    )

    @classmethod
    async def add(cls, **kwargs) -> None:
        async with async_sessionmaker() as session:
            session.add(cls(**kwargs))
            await session.commit()

    @classmethod
    async def get(cls, date: str) -> PsychomatrixSavedPage:
        async with async_sessionmaker() as session:
            query = await session.execute(
                select(cls).where(cls.date == date)
            )
            return query.scalar()

    @classmethod
    async def is_exists(cls, date: str) -> bool:
        async with async_sessionmaker() as session:
            query = await session.execute(
                select(cls.id).where(cls.date == date)
            )
            return query.scalar() is not None
