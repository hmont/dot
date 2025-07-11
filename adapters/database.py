from sqlalchemy import Executable
from sqlalchemy import MappingResult

from sqlalchemy.ext.asyncio import create_async_engine

class Database:
    def __init__(self, uri: str):
        self.engine = create_async_engine(uri)
        self.session = None


    async def connect(self) -> None:
        self.session = await self.engine.connect()


    async def disconnect(self) -> None:
        await self.engine.dispose()

        if self.session:
            await self.session.close()


    async def execute(self, query: Executable) -> MappingResult | None:
        if not self.session:
            raise ValueError("You must connect() to the database first")

        try:
            res = await self.session.execute(query)

            await self.session.commit()

            return res.mappings()

        except Exception as e:
            await self.session.rollback()
            raise e


    async def fetch_one(self, query: Executable):
        result = await self.execute(query)

        if result is None:
            return None

        return result.fetchone()


    async def fetch_many(
        self,
        query: Executable,
        page: int = 1,
        page_size: int = 5
    ):
        result = await self.execute(query)

        if result is None:
            return None

        return result.fetchmany(size=page_size)