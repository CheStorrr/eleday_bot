from loader import bot, dp 
from aiogram import F

from database.database import Database
from models.user import User

from middlewares.database_middleware import DatabaseMiddleware
from middlewares.admin_middleware import AdminMiddleware, AdminCallbackMiddleware

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


async def check_restricts(db: Database):
    ...

async def main():
    async with aiosqlite.connect('database/database.db') as conn:
        db = Database(conn)
        await db.create_tables()

        dp.message.middleware(DatabaseMiddleware(db=db))

        admin_commands.router.message.middleware(AdminMiddleware(db=db))
        admin_commands.router.callback_query.middleware(AdminCallbackMiddleware(db=db))

        dp.include_routers(
            games.router,
            admin_commands.router
        )

        await asyncio.gather(dp.start_polling(bot), check_restricts(db))

asyncio.run(main())