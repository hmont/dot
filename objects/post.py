from datetime import datetime
from datetime import timezone

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
        def _iso(dt: datetime | None):
            if dt is None:
                return None

            local_tz = datetime.now().astimezone().tzinfo
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=local_tz)

            return dt.astimezone(timezone.utc).isoformat()

        return {
            'id': self.id,
            'poster': self.poster_id,
            'created_at': _iso(self.created_at),
            'updated_at': _iso(self.updated_at),
            'content': self.content
        }
