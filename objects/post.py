from datetime import datetime

from typing import Mapping
from typing import Any
from typing import Dict

class Post:
    def __init__(
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
    def from_mapping(cls, mapping: Mapping[str, Any]):
        return cls(
            post_id=mapping['id'],
            poster_id=mapping['poster'],
            created_at=mapping['created_at'],
            updated_at=mapping['updated_at'],
            content=mapping['content']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'poster': self.poster_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'content': self.content
        }