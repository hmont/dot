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

from sqlalchemy.orm import relationship

from state.global_state import database

from objects.user import User

from tables import user_preferences

from . import Base

class Users(Base):
    __tablename__ = "users"

    _id = Column(
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
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
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
    ).returning(Users._id)

    res = (await database.execute(stmt))

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
        query = query.where(Users._id == int(user_id))


    result = await database.fetch_one(query)

    return User.from_mapping(result) if result else None