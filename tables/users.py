from typing import Optional

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import LargeBinary
from sqlalchemy import TIMESTAMP
from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete as _delete

from state.global_state import database

from objects.user import User

from . import user_preferences
from . import Base

class Users(Base): # pylint: disable=too-few-public-methods
    """
    Class representing the `users` table in the database.
    """
    __tablename__ = "users"

    user_id = Column(
        Integer,
        name="id",
        autoincrement=True,
        primary_key=True
    )

    username = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now() # pylint: disable=not-callable
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(), # pylint: disable=not-callable
        onupdate=func.now() # pylint: disable=not-callable
    )

    password_bytes = Column(
        LargeBinary,
        nullable=False
    )

    avatar_url = Column(
        Text,
        nullable=True
    )

    bio = Column(
        String(255),
        nullable=True
    )

    privs = Column(
        Integer,
        nullable=False
    )

    display_name = Column(
        Text,
        nullable=False
    )


async def create(
    username: str,
    password_bytes: bytes,
) -> Optional[int]:
    """
    Create a user in the database with the given username and hashed password.

    Args:
        username (str): Username of the user to be created.
        password_bytes (bytes): The hashed password to be used for the user.

    Returns:
        Optional[int]: The user ID of the created user, or None if the user was not created.
    """
    stmt = insert(Users).values(
        username=username,
        display_name=username,
        password_bytes=password_bytes,
        privs=1
    ).returning(Users.user_id) # pylint: disable=protected-access

    res = await database.execute(stmt)

    if not res:
        return

    mapping = res.first()

    assert mapping is not None

    user_id = mapping['id']

    await user_preferences.create(user_id)

    return user_id

async def fetch_one(
    username: Optional[str] = None,
    user_id: Optional[int] = None
) -> Optional[User]:
    """
    Fetch the user from the database with the given username or user ID.

    Args:
        username (Optional[str], optional): The username of the user to fetch.
        user_id (Optional[int], optional): The user ID of the user to fetch.

    Raises:
        ValueError: If neither a username nor user ID were provided.

    Returns:
        Optional[User]: The user with the given username/ID, or None if none was found.
    """
    if not username and not user_id:
        raise ValueError("one of username or user_id must be provided")

    query = select(Users)

    if username:
        query = query.where(Users.username == str(username))

    if user_id:
        query = query.where(Users.user_id == int(user_id)) # pylint: disable=protected-access


    result = await database.fetch_one(query)

    return User.from_mapping(result) if result else None


async def update_one(
    user_id: int,
    username: Optional[str] = None,
    display_name: Optional[str] = None,
    password_hash: Optional[bytes] = None,
    bio: Optional[str] = None
):
    """
    Update the user with the given user ID with the given values.

    Args:
        user_id (int): The ID of the user to update.
        username (Optional[str], optional): The user's \
            new username. If None, the username is not updated.
        display_name (Optional[str], optional): The user's new \
            display name. If None, the display name is not updated.
        password_hash (Optional[bytes], optional): The user's new \
            password hash. If None, the hash is not updated.
        bio (Optional[str], optional): The user's new biography. \
            If None, the biography is not updated.
    """
    stmt = update(Users).where(Users.user_id == user_id)

    if username is not None:
        stmt = stmt.values(username=username)
    if display_name is not None:
        stmt = stmt.values(display_name=display_name)
    if bio is not None:
        stmt = stmt.values(bio=bio)
    if password_hash is not None:
        stmt = stmt.values(password_bytes=password_hash)

    await database.execute(stmt)


async def delete_one(
    user_id: Optional[int] = None,
    username: Optional[str] = None
):
    """
    Delete the user with the given username or user ID.

    Args:
        user_id (Optional[int], optional): The user ID of the user to be deleted.
        username (Optional[str], optional): The username of the user to be deleted.
    """
    stmt = _delete(Users)

    if user_id:
        stmt = stmt.where(Users.user_id == user_id)
    if username:
        stmt = stmt.where(Users.username == username)

    await database.execute(stmt)
