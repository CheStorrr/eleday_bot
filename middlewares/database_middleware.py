from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from database.database import Database

from models.user import User

class DatabaseMiddleware(BaseMiddleware):

    def __init__(self, db: Database) -> None:
        self.db = db

    async def __call__(
        self, 
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], 
        event: Message, 
        data: Dict[str, Any]
    ) -> Any:
        
        user = User(event.from_user.id)

        is_user = await user.init()
        print(is_user)

        if not is_user:
            print("Добавления пользователя в базу данных")
            await user.new(event.from_user.full_name, event.from_user.username)
            
        data['user'] = user 

        return await handler(event, data)