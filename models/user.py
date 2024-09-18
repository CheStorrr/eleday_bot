from database.database import Database
from aiosqlite import Connection

from typing import Optional

class User(Database):
    
    def __init__(
        self,
        user_id: int
    ):
        self.user_id = user_id 


    async def init(self):
        
        try: print(self.name)
        except: return False
        self.link = f"<a href='tg://user?id={self.user_id}'>{self.name}</a>"
        return True

    async def new(
        self, 
        name: str,
        username: Optional[str] = None
    ):
        self.name = name 
        self.username = username
        await self.init()
