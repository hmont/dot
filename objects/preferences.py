from typing import Mapping
from typing import Any
from typing import Dict

from datetime import datetime

from sqlalchemy import RowMapping

class Preferences:
    def __init__(
        self,
        user_id: int,
        is_private: bool
    ):
        self.user_id = user_id
        self.is_private = is_private


    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any] | RowMapping):
        return cls(
            user_id=mapping['user_id'],
            is_private=mapping['is_private']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'is_private': self.is_private
        }