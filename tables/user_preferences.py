from typing import Optional

from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete as _delete

from state.global_state import database

from objects.preferences import Preferences

from . import Base

class UserPreferences(Base): # pylint: disable=too-few-public-methods
    """
    Class representing the `user_preferences` table in the database.
    """
    __tablename__ = 'user_preferences'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    is_private = Column(Boolean, default=False)


async def create(
    user_id: int
) -> Preferences | None:
    """
    Create a user preferences record in the database for the given user ID.

    Args:
        user_id (int): The ID of the user for which to create the record.

    Returns:
        Preferences | None: The Preferences object of the created record, or \
            None if none was created.
    """
    stmt = (insert(UserPreferences)
        .values(user_id=user_id)
        .returning(UserPreferences.user_id)
    )

    await database.execute(stmt)

    return await fetch_one(user_id)


async def fetch_one(
    user_id: int
) -> Preferences | None:
    """
    Fetch the preferences of the user with the given user ID.

    Args:
        user_id (int): The ID of the user whose preferences will be returned.

    Returns:
        Preferences | None: The Preferences object of the user, or None if none was found.
    """
    query = select(UserPreferences).where(UserPreferences.user_id == user_id)

    res = await database.fetch_one(query)

    if not res:
        return None

    return Preferences.from_mapping(res)


async def update_one(
    user_id: int,
    is_private: Optional[bool] = None
):
    """
    Update the preferences of the user with the given ID with the given values.

    Args:
        user_id (int): The ID of the user whose preferences will be updated.
        is_private (Optional[bool], optional): Whether the user's profile will \
            be private. Defaults to None.
    """
    stmt = update(
        UserPreferences
    ).where(
        UserPreferences.user_id == user_id
    )

    if is_private is not None:
        stmt = stmt.values(is_private=is_private)

    await database.execute(stmt)

async def delete_one(
    user_id: int
):
    """
    Delete the preferences of the user with the given ID.
    This is typically run upon user deletion.

    Args:
        user_id (int): The ID of the user whose preferences will be deleted.
    """
    stmt = _delete(UserPreferences).where(UserPreferences.user_id == user_id)

    await database.execute(stmt)
