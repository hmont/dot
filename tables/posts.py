from typing import Optional
from typing import List

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import TIMESTAMP
from sqlalchemy import ForeignKey
from sqlalchemy import insert
from sqlalchemy import select

from sqlalchemy.sql import func

from . import Base

from state.global_state import database

from objects.post import Post

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
) -> None:
    stmt = insert(Posts).values(
        poster=poster,
        content=content
    )

    await database.execute(stmt)

async def fetch_many(
    poster: Optional[int] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None
) -> List[Post]:
    query = select(Posts)

    if page and page_size:
        query = query.limit(page_size).offset(page_size * page)

    if poster:
        query = query.where(Posts.poster == poster)

    result = await database.fetch_many(query)

    return [Post.from_mapping(mapping) for mapping in result]
