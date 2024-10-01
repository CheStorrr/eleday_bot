from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiosqlite import Connection
from aiogram.types import Message, CallbackQuery
from database.database import Database
from loader import bot
from models.admin import Admin, User


class AdminMiddleware(BaseMiddleware):

    def __init__(self, db: Database) -> None:
        self.db = db

    async def __call__(
            self, 
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], 
            event: Message, 
            data: Dict[str, Any]
    ):
        
        member = await bot.get_chat_member(event.chat.id, event.from_user.id)

        if member.status not in ['administrator', 'creator']:
            return event.answer("Данная команда доступна лишь команде администрации")
        
        admin = Admin(self.db.db)
        user = User(self.db.db)

        await user.init(event.from_user.id)

        await admin.init(user=user, bot=bot)

        data['admin'] = admin
        
        await handler(event, data)
        
class AdminCallbackMiddleware(BaseMiddleware):

    def __init__(self, db: Database) -> None:
        self.db = db

    async def __call__(
            self, 
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]], 
            event: CallbackQuery, 
            data: Dict[str, Any]
    ):
        
        admin = Admin(self.db.db)
        user = User(self.db.db)

        await user.init(event.from_user.id)

        await admin.init(user=user, bot=bot)

        data['admin'] = admin
        
        await handler(event, data)
        