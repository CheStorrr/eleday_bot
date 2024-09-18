from aiogram import Router, F 

from aiogram.types import Message 

from models.user import User

import time


router = Router(name=__name__)


last_give_money = {}

@router.message(F.text.lower() == "получить деньги")
async def give_self_balance(
    message: Message,
    user: User
):
    if not user.user_id in last_give_money:
        last_give_money[user.user_id] = 0

    if time.time() - last_give_money[user.user_id] < 600:
        return await message.reply(f"10 минут ещё не прошли!")
    
    user.balance += 500
    await user.reinit()
    last_give_money[user.user_id] = time.time()
    await message.reply(f"Отлично! Ты получил 500 Eleday COIN. Следующая попытка через 10 минут.")
