from typing import Optional

from sqlalchemy import Executable
from sqlalchemy import MappingResult

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncConnection

class Database:
    """
    Class representing the database connection.
    """
    def __init__(self, uri: str):
        self.engine = create_async_engine(uri)
        self.session: Optional[AsyncConnection] = None


    async def connect(self) -> None:
        """
        Connect to the database.
        """
        self.session = await self.engine.connect()


    async def disconnect(self) -> None:
        """
        Disconnect from the database.
        """
        await self.engine.dispose()

        if self.session:
            await self.session.close()


    async def execute(self, query: Executable) -> MappingResult | None:
        """
        Execute the given query.

        Requires that the database be initialized (i.e. connect() has been called.)

        Returns a MappingResult if the execution was successful, or None if an \
        error is raised.
        """
        if not self.session:
            raise ValueError("You must connect() to the database first")

        try:
            res = await self.session.execute(query)

            await self.session.commit()

            return res.mappings()

        except Exception as e: # pylint: disable=broad-exception-caught
            print(e)
            await self.session.rollback()


    async def fetch_one(self, query: Executable):
        """
        Fetch a row from the database with the given query.

        Requires that the database be initialized (i.e. connect() has been called.)

        Returns a RowMapping if a record was found, or None if no record is found or if \
        an error is raised.
        """

        result = await self.execute(query)

        if result is None:
            return None

        return result.fetchone()


    async def fetch_many(
        self,
        query: Executable,
        page_size: int = 5
    ):
        """
        Fetch the specified number of rows from the database with the given query.

        Requires that the database be initialized (i.e. connect() has been called.)

        Returns a sequence of RowMappings containing each record, or None if an error is raised.
        """

        result = await self.execute(query)

        if result is None:
            return None

        return result.fetchmany(size=page_size)
