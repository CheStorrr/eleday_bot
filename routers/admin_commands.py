from aiogram import Router, F 

from aiogram.types import Message 
from aiogram.filters import Command

from models.admin import Admin
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


@router.message(Command('mute'))
async def mute_command(
    message: Message,
    user: User,
    admin: Admin
):
    args = message.text.splitlines()[0].split('/mute')[1]


    reason = "Отсутствует"
    duration = None 
    arg_name = None

    reply = message.reply_to_message

    try:

        if len(message.text.splitlines()) > 1:
            reason = message.text.splitlines()[1]



        if reply is not None:
            arg_name = reply.from_user.id
            duration = 480
            if len(args) == 1:
                duration = int(args.split()[0])

        else:
            duration = 480
            if len(args) > 0:
                arg_name = args.split()[0]
                print(message.entities[1].user)
                if message.entities[1].user is not None:
                    arg_name = message.entities[1].user.id
                    print(arg_name)
                duration = int(args.split()[1])
            else:
                return await message.reply(f"Это команда должна использоваться с @user или реплай на пользователя")

        user_muted = await admin.mute(arg_name=arg_name, chat_id=message.chat.id, duration=duration, reason=reason)

        if user_muted == 0: return await message.answer(f"Невозможно замутить администратора")

        await message.answer(f"Пользователь {user_muted.link} был переключен в беззвучный режим на {duration} минут. \nМут выдан админом: {user.link}\nПричина: {reason}")

    except ValueError as e: return await message.answer(f"Произошла ошибка при попытке получить время мута: {e}")


