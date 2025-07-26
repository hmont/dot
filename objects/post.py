from datetime import datetime

from typing import Mapping
from typing import Any
from typing import Dict

from sqlalchemy import RowMapping

class Post:
    """
    Class representing a post.
    """
    def __init__( # pylint: disable=too-many-arguments, too-many-positional-arguments
        self,
        post_id: int,
        poster_id: int,
        created_at: datetime | None,
        updated_at: datetime | None,
        content: str
    ):
        self.id = post_id
        self.poster_id = poster_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.content = content


    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any] | RowMapping):
        """
        Convert a mapping into a Post object.

        Requires that the given mapping is a valid mapping (e.g. a dictionary or \
        RowMapping).
        """
        return cls(
            post_id=mapping['id'],
            poster_id=mapping['poster'],
            created_at=mapping['created_at'],
            updated_at=mapping['updated_at'],
            content=mapping['content']
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Return a dictionary representation of the Post object.
        """
        return {
            'id': self.id,
            'poster': self.poster_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'content': self.content
        }
