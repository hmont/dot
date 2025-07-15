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

from state.global_state import database

from objects.post import Post

from .user_preferences import UserPreferences

from . import Base

class Posts(Base): # pylint: disable=too-few-public-methods
    __tablename__ = 'posts'

    _id = Column(
        Integer,
        name="id",
        primary_key=True
    )

    poster = Column(
        Integer,
        ForeignKey('users.id')
    )

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        default=func.now() # pylint: disable=not-callable
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        default=func.now(), # pylint: disable=not-callable
        onupdate=func.now() # pylint: disable=not-callable
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


async def fetch_public(
    auth_user_id: int,
    poster: Optional[int] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None
):
    query = (
        select(Posts, UserPreferences)
        .join_from(Posts, UserPreferences, Posts.poster == UserPreferences.user_id)
        .where(
            (UserPreferences.is_private == False) |
            (Posts.poster == auth_user_id) # pylint: disable=singleton-comparison
        )
    )

    query = query.order_by(Posts.created_at.desc())

    if page and page_size:
        query = query.limit(page_size).offset(page_size * (page - 1))

    if poster:
        query = query.where(Posts.poster == poster)

    result = await database.fetch_many(query)

    if not result:
        return []

    return [Post.from_mapping(p) for p in result]
