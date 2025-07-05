from typing import Any

from databases import Database as _Database

from sqlalchemy import ClauseElement

from sqlalchemy.dialects import postgresql

DIALECT = postgresql.dialect()

class Database:
    def __init__(self, url: str):
        self._db = _Database(url)

    async def connect(self):
        await self._db.connect()

    async def disconnect(self):
        await self._db.disconnect()

    def _compile(self, query: ClauseElement | str) -> str:
        if not isinstance(query, ClauseElement):
            return query

        return str(query.compile(
            dialect=DIALECT,
            compile_kwargs={"literal_binds": True}
        ))


    async def execute(
        self,
        query: ClauseElement | str
    ) -> None:
        return await self._db.execute(self._compile(query))


    async def fetch_one(
        self,
        query: ClauseElement | str
    ) -> dict[str, Any] | None:
        res = await self._db.fetch_one(self._compile(query))

        if res is None:
            return None

        return dict(res._mapping)