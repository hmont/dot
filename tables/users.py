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
    stmt = _delete(Users)

    if user_id:
        stmt = stmt.where(Users.user_id == user_id)
    if username:
        stmt = stmt.where(Users.username == username)

    await database.execute(stmt)