from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from database.database import Database

from models.user import User

from loader import bot

class DatabaseMiddleware(BaseMiddleware):

    def __init__(self, db: Database) -> None:
        self.db = db

    async def __call__(
        self, 
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], 
        event: Message, 
        data: Dict[str, Any]
    ) -> Any:
        
        user = User(self.db.db)

        is_user = await user.init(event.from_user.id)
        print(is_user)

        if not is_user:
            print("Добавления пользователя в базу данных")
            member = await bot.get_chat_member(event.chat.id, event.from_user.id)

            is_admin = True if member.status in ['administrator', 'creator'] else False
            await user.new(event.from_user.full_name, event.from_user.username, is_admin)
        
        user.name = event.from_user.full_name
        user.username = event.from_user.username
        await user.reinit()
            
        data['user'] = user 
        print(event.text)
        return await handler(event, data)