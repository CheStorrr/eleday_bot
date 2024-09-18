from loader import bot, dp 
from aiogram import F

from database.database import Database
from models.user import User

from middlewares.database_middleware import DatabaseMiddleware

from routers import games, admin_commands

from aiogram.filters import CommandStart
from aiogram.types import Message

import asyncio, logging, aiosqlite, time


logging.basicConfig(level=logging.INFO)

@dp.message(CommandStart())
async def start_command(
    message: Message,
    user: User
):
    return await message.answer(f"Здравствуй, {user.link}! Я бот-модератор для чата @eledayhut. Чтобы узнать команды, напиши /help. \nЧтобы ознакомиться с правилами, напиши /rules")



async def main():
    async with aiosqlite.connect('database/database.db') as conn:
        db = Database(conn)
        

        dp.message.middleware(DatabaseMiddleware(db=db))

        dp.include_routers(
            games.router,
            admin_commands.router
        )


        await dp.start_polling(bot)

asyncio.run(main())