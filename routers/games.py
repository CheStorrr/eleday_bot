from aiogram import Router, F 

from aiogram.types import Message 

from models.user import User


router = Router(name=__name__)


@router.message(F.text.lower() == "бал")
async def check_balance(
    message: Message,
    user: User
):
    await message.reply(f"Твой баланс: {user.balance} Eleday COIN")



