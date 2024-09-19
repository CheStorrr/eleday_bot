from database.database import Database
from aiosqlite import Connection, connect

from typing import Literal, Optional

class User(Database):

    db: Connection
    
    def __init__(
        self,
        db: Connection
    ):
        super().__init__(db)



    async def init(self, user_id: Optional[int] = None):
        self.user_id = user_id if user_id else self.user_id
        cur = await self.db.execute("SELECT * FROM users WHERE id = ?", (self.user_id,))
        user = await cur.fetchone()
        if user:
            self.name = user['name']
            self.username = user['username']
            self.messages = user['messages']
            self.date_reg = user['created_at']
            self.balance = user['balance']
            self.warns = user['warns']
            self.is_mute = user['is_mute']
            self.is_ban = user['is_ban']
            self.is_admin = user['is_admin']
            self.reputation = user['reputation']
            self.link = f"<a href='tg://user?id={self.user_id}'>{self.name}</a>"
            self.link_username = f"<a href='https://t.me/{self.username}'>{self.name}</a>"
            return True
        return False

    async def new(
        self, 
        name: str,
        username: Optional[str] = None,
        is_admin: bool = False
    ):
        self.name = name 
        self.username = username
        self.is_admin = is_admin
        await self.db.execute("INSERT OR IGNORE INTO users (id, name, username, is_admin) VALUES (?,?,?,?)", (self.user_id, self.name, self.username, self.is_admin,))
        await self.db.commit()
        await self.init()

    async def reinit(self):
        args = (self.name, self.username, self.balance, self.messages, self.warns, self.reputation, self.is_admin, self.is_ban, self.is_mute, self.user_id,)
        await self.db.execute(f"UPDATE users SET name = ?, username = ?, balance = ?, messages = ?, warns = ?, reputation = ?, is_admin = ?, is_ban = ?, is_mute = ? WHERE id = ?", args)

        await self.db.commit()


    async def find(self, **kwargs: Literal['username', 'name']):
        username_or_name = 'username' if 'username' in kwargs else 'name'
        value = kwargs['username'].replace('@', '') if 'username' in kwargs else kwargs['name']
        query = f"SELECT * FROM users WHERE {username_or_name} = ?"
        print(query, value)
        cur = await self.db.execute(query, (value,))
        is_user = await cur.fetchone()
        print(is_user)
        if is_user:
            await self.init(is_user['id'])
            return self
        
        return None