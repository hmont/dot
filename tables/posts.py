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
from sqlalchemy import delete as _delete

from sqlalchemy.sql import func

from state.global_state import database

from objects.post import Post

from .user_preferences import UserPreferences

from . import Base

class Posts(Base): # pylint: disable=too-few-public-methods
    """
    Class representing the `posts` table in the database.
    """
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
    """
    Insert a post into the database with the given poster ID and content.

    Args:
        poster (int): The user ID of the poster of the post.
        content (str): The content of the post.
    """
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
    """
    Deprecated.
    """
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
    auth_user_id: Optional[int] = None,
    poster: Optional[int] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None
) -> List[Post]:
    """
    Fetch public posts (or posts matching the given user ID) from the database.

    Args:
        auth_user_id (Optional[int], optional): The user ID of the currently logged in user.
        poster (Optional[int], optional): The user ID of the poster of posts to be fetched.
        page (Optional[int], optional): The page to be fetched.
        page_size (Optional[int], optional): The size of respective pages.

    Returns:
        List[Post]: The list of Posts fetched.
    """
    query = (
        select(Posts, UserPreferences)
        .join_from(Posts, UserPreferences, Posts.poster == UserPreferences.user_id)
    )

    if auth_user_id:
        query = query.where(
            (UserPreferences.is_private == False) |  # pylint: disable=singleton-comparison
            (Posts.poster == auth_user_id)
        )
    else:
        query = query.where(UserPreferences.is_private == False) # pylint: disable=singleton-comparison

    query = query.order_by(Posts.created_at.desc())

    if page and page_size:
        query = query.limit(page_size).offset(page_size * (page - 1))

    if poster:
        query = query.where(Posts.poster == poster)

    result = await database.fetch_many(query)

    if not result:
        return []

    return [Post.from_mapping(p) for p in result]


async def delete(
    poster_id: int
):
    """
    Delete all posts matching the given poster ID.

    Args:
        poster_id (int): The user ID of the poster of posts to be deleted.
    """
    stmt = _delete(Posts).where(Posts.poster == poster_id)

    await database.execute(stmt)


async def delete_one(
    post_id: int
) -> None:
    """
    Delete the post with the given post ID.
    """
    stmt = _delete(Posts).where(Posts._id == post_id)

    await database.execute(stmt)


async def fetch_one(
    post_id: int
) -> Post | None:
    """
    Fetch a single post from the database with the given ID.

    Returns the Post object, or None if no post was found with the given ID.
    """

    stmt = select(Posts).where(Posts._id == post_id) # pylint: disable=protected-access

    res = await database.fetch_one(stmt)

    return Post.from_mapping(res) if res else None

