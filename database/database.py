from aiosqlite import Connection, Cursor
from aiosqlite import connect



class Database:

    db: Connection
    cur: Cursor


 
    async def __create_tables(self) -> None:
        ...

    async def init(self) -> None:

        async with connect('database/database.db') as db:
            self.db = db
            await self.__create_tables()
