from loader import bot, dp 

from database.database import Database
from models.user import User

from middlewares.database_middleware import DatabaseMiddleware

from aiogram.filters import CommandStart
from aiogram.types import Message

import asyncio, logging


logging.basicConfig(level=logging.INFO)

@dp.message(CommandStart)
async def start_command(
    message: Message,
    user: User
):
    return await message.answer(f"Здравствуй, {user.link}! Я бот-модератор для чата Eleday'я. Чтобы узнать команды, напиши /help. \nЧтобы ознакомиться с правилами, напиши /rules")

async def main():

    db = Database()
    await db.init()

    dp.message.middleware(DatabaseMiddleware(db=db))

    await dp.start_polling(bot)

asyncio.run(main())