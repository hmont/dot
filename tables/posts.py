from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import TIMESTAMP
from sqlalchemy import ForeignKey
from sqlalchemy import insert

from sqlalchemy.sql import func

from . import Base

from state.global_state import database

class Posts(Base):
    __tablename__ = 'posts'

    _id = Column(
        Integer,
        name="id",
        primary_key=True
    )

    poster = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        default=func.now()
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        default=func.now(),
        onupdate=func.now()
    )

    content = Column(
        Text,
        nullable=False
    )

async def create(
    poster: int,
    content: str
):
    stmt = insert(Posts).values(
        poster=poster,
        content=content
    )

    await database.execute(stmt)