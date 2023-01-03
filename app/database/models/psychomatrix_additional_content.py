from __future__ import annotations

from sqlalchemy import Column, BigInteger, String, select, Text, Integer

from ..base import Base
from ..sessionmaker import async_sessionmaker


class PsychomatrixAdditionalContent(Base):
    __tablename__ = 'psychomatrix_additional_contents'

    id = Column(
        BigInteger,
        primary_key=True
    )
    code = Column(
        String(length=55),
        nullable=True,
    )
    title = Column(
        String(length=55),
        nullable=True
    )
    annotation = Column(
        String(length=4098),
        nullable=True
    )
    level = Column(
        Integer,
        nullable=True
    )
    text = Column(
        Text(length=10240),
        nullable=True
    )

    @classmethod
    async def add(cls, **kwargs) -> None:
        async with async_sessionmaker() as session:
            session.add(cls(**kwargs))
            await session.commit()

    @classmethod
    async def get_in(cls, codes: list[str]) -> list[PsychomatrixAdditionalContent]:
        async with async_sessionmaker() as session:
            query = await session.execute(
                select(cls).filter(cls.code.in_(codes)).order_by(cls.id)
            )
            return [i[0] for i in query.all()]
