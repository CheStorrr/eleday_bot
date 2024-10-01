from datetime import datetime, timedelta
from aiogram import Bot
from aiogram.types import ChatPermissions, InlineKeyboardButton
from database.database import Database

from typing import Literal, Optional, Self, Union

from aiogram.utils.keyboard import InlineKeyboardBuilder

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
        self.main_admin_id = 6574898357
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
            reason: Optional[str] = None,
            until_date: Optional[datetime] = None
    ):
        await self.db.execute("INSERT INTO restricted (admin_id, type_restricks, user_restricted_id, reason, until_date) VALUES (?,?,?,?,?)", (self.user.user_id, type_restrict, user_resrickted_id, reason, until_date,))
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
            await user_mute.init(arg_name)
           

        elif arg_name[0] == '@':
            user_mute = await user_mute.find(username=arg_name)

        member = await self.bot.get_chat_member(chat_id=chat_id, user_id=user_mute.user_id)
        if member.status in ['administrator', 'creator']:
            return 0
        permissions = ChatPermissions(can_send_messages=False)
        await self.__restrict(type_restrict='mute', user_resrickted_id=user_mute.user_id, reason=reason, until_date=datetime.now()+timedelta(minutes=duration))
        await self.bot.restrict_chat_member(chat_id=chat_id, user_id=user_mute.user_id, permissions=permissions, until_date=timedelta(minutes=duration))

        return user_mute
    
    async def unmute(
        self,
        arg_name: Union[str, int],
        chat_id: int
    ):
        user_unmute = User(self.db)

        if isinstance(arg_name, int):
            await user_unmute.init(arg_name)
           

        elif arg_name[0] == '@':
            user_unmute = await user_unmute.find(username=arg_name)

        member = await self.bot.get_chat_member(chat_id=chat_id, user_id=user_unmute.user_id)
        if member.status in ['administrator', 'creator']:
            return 0
        permissions = ChatPermissions(
            can_send_audios=True,
            can_send_documents=True,
            can_send_messages=True,
            can_send_other_messages=True,
            can_send_photos=True,
            can_send_polls=True,
            can_send_video_notes=True,
            can_send_videos=True,
            can_send_voice_notes=True,
            can_add_web_page_previews=True,
            can_invite_users=True
        )
        await self.bot.restrict_chat_member(chat_id=chat_id, user_id=user_unmute.user_id, permissions=permissions)

        return user_unmute
    

    async def warn(
        self,
        chat_id: int,
        user_id,
        reason: Optional[str]
    ):
        
        user_warn = User(self.db)
        await user_warn.init(user_id=user_id)
        
        
        member = await self.bot.get_chat_member(chat_id=chat_id, user_id=user_warn.user_id)
        if member.status in ['administrator', 'creator']:
            return 0
        user_warn.warns += 1
        await self.__restrict('warn', user_id, reason, datetime.now()+timedelta(days=7))

        return user_warn
    

    async def request_ban(
        self,
        user_ban_id: int,
        message_id: int,
        reason: Optional[str] = None
    ):
        

        ban_user = User(self.db)
        await ban_user.init(user_id=user_ban_id)

        text = f"""Новый запрос на бан от админа {self.user.link}

Запрос на пользователя {ban_user.link}
Дата: {datetime.now()}
Причина: {reason if reason else 'нет'}
"""
        
        kb = InlineKeyboardBuilder([
            [InlineKeyboardButton(text="Принять", callback_data=f"accept_ban_{message_id}_{user_ban_id}"),
             InlineKeyboardButton(text="Отклонить", callback_data=f"reject_ban_{message_id}")]
        ]).as_markup()
        await self.bot.send_message(chat_id=self.main_admin_id, text=text, reply_markup=kb)


        

        

        
        


