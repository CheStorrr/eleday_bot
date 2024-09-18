from aiosqlite import Connection, Cursor
from aiosqlite import connect, Row



class Database:

    db: Connection = None
    cur: Cursor

    def __init__(self, db: Connection):
        self.db = db
        self.db.row_factory = Row


 
    async def __create_tables(self) -> None:
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS users(
            id BIGINT PRIMARY KEY,
            name TEXT,
            username TEXT DEFAULT NULL,
            messages INT DEFAULT 0,
            warns INT DEFAULT 0,
            balance BIGINT DEFAULT 0,
            reputation INT DEFAULT 0,
            is_mute BOOLEAN DEFAULT FALSE,
            is_ban BOOLEAN DEFAULT FALSE,
            is_admin BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        await self.db.commit()

  