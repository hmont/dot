from datetime import datetime

from typing import Any
from typing import Mapping

from sqlalchemy import RowMapping

class User: # pylint: disable=too-many-instance-attributes
    def __init__( # pylint: disable=too-many-arguments, too-many-positional-arguments
        self,
        username: str,
        display_name: str,
        user_id: int,
        created_at: datetime | None,
        updated_at: datetime | None,
        password_bytes: bytearray,
        avatar_url: str,
        bio: str,
        privs: int
    ):
        self.username = username
        self.display_name = display_name
        self.created_at = created_at
        self.updated_at = updated_at
        self.password_bytes = password_bytes
        self.avatar_url = avatar_url
        self.bio = bio
        self.privs = privs
        self.id = user_id


    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any] | RowMapping):
        """
        Convert a mapping into a User object.

        Requires that the given mapping is a valid mapping (e.g. a dictionary or \
        RowMapping).
        """
        return cls(
            username=mapping['username'],
            user_id=mapping['id'],
            created_at=mapping['created_at'],
            updated_at=mapping['updated_at'],
            display_name = mapping['display_name'],
            password_bytes=mapping['password_bytes'],
            avatar_url=mapping['avatar_url'],
            bio=mapping['bio'],
            privs=mapping['privs']
        )


    def __repr__(self) -> str:
        return f"User(id={self.id}, username='{self.username}')"

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of the Preferences object.
        """
        return {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name,
            'created_at': self.created_at,
            #'updated_at': self.updated_at,
            #'password_bytes': self.password_bytes,
            'avatar_url': self.avatar_url,
            'bio': self.bio,
            #'privs': self.privs
        }
