from datetime import datetime, timedelta
from aiogram import Bot
from aiogram.types import ChatPermissions
from database.database import Database

from typing import Literal, Optional, Self, Union

from aiosqlite import Connection

from models.user import User

class Admin(Database):

    db: Connection

    def __init__(
            self,
            db: Connection
    ):
        super().__init__(db)
        self.user: User = None
        self.bot: Bot = None

    async def init(
            self,
            user: User,
            bot: Optional[Bot] = None
    ):
        
        self.user = user
        self.bot = bot if not self.bot else self.bot
        


        cur = await self.db.execute("SELECT * FROM users WHERE is_admin = True AND id = ?", (self.user.user_id,))
        admin = await cur.fetchone()

        if not admin:
            
            return False 
        
        return True
   
    
    async def new(
            self,
            user: Optional[User] = None
    ):
        self.user = user if not self.user else self.user

        self.user.is_admin = True
        await self.user.reinit()



    async def __restrict(
            self,
            type_restrict: Literal['mute', 'ban', 'warn', 'rep', 'tick'],
            user_resrickted_id: int,
            reason: Optional[str] = None
    ):
        await self.db.execute("INSERT INTO restricted (admin_id, type_restricks, user_restricted_id, reason) VALUES (?,?,?,?)", (self.user.user_id, type_restrict, user_resrickted_id, reason,))
        await self.db.commit()


    async def mute(
            self,
            arg_name: Union[str, int],
            chat_id: int,
            duration: Optional[int] = 480,
            reason: Optional[str] = None
    ):
        user_mute = User(self.db)

        if isinstance(arg_name, int):
            user_mute = User(self.db)
            await user_mute.init(arg_name)
           

        elif arg_name[0] == '@':
            user_mute = await user_mute.find(username=arg_name)

        else:
            user_mute = await self.user.find(name=arg_name)

        member = await self.bot.get_chat_member(chat_id=chat_id, user_id=user_mute.user_id)
        if member.status in ['administrator', 'creator']:
            return 0
        permissions = ChatPermissions(can_send_messages=False)
        await self.__restrict(type_restrict='mute', user_resrickted_id=user_mute.user_id, reason=reason)
        await self.bot.restrict_chat_member(chat_id=chat_id, user_id=user_mute.user_id, permissions=permissions, until_date=timedelta(minutes=duration))

        return user_mute

        

        

        
        


