from typing import Optional
from typing import List

from urllib.parse import quote

import bleach

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
    cleaned = bleach.clean(content)

    stmt = insert(Posts).values(
        poster=int(poster),
        content=quote(str(cleaned))
    )

    await database.execute(stmt)

async def fetch_many(
    poster: Optional[int] = None,
    username: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None
) -> List[Post]:
    query = select(Posts)

    query = query.order_by(Posts.created_at.desc())

    if page and page_size:
        query = query.limit(page_size).offset(page_size * (page - 1))

    if poster:
        query = query.where(Posts.poster == poster)

    result = await database.fetch_many(query)

    if not result:
        return []

    return [Post.from_mapping(mapping) for mapping in result]
