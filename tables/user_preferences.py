from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy import insert
from sqlalchemy import select

from sqlalchemy.orm import relationship

from state.global_state import database

from objects.preferences import Preferences

from . import Base

class UserPreferences(Base):
    __tablename__ = 'user_preferences'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    is_private = Column(Boolean, default=False)


async def create(
    user_id: int
):
    stmt = insert(UserPreferences).values(user_id=user_id)

    await database.execute(stmt)


async def fetch_one(
    user_id: int
):
    query = select(UserPreferences).where(UserPreferences.user_id == user_id)

    res = await database.fetch_one(query)

    if not res:
        return None

    return Preferences.from_mapping(res)