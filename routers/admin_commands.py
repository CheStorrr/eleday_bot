from aiogram import Bot, Router, F 

from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from models.admin import Admin
from models.user import User
from config import main_chat

import time


router = Router(name=__name__)



@router.message(Command('mute'))
async def mute_command(
    message: Message,
    user: User,
    admin: Admin
):
    args = message.text.splitlines()[0].split('/mute')[1]


    reason = "Отсутствует"
    duration = 480
    arg_name = None

    reply = message.reply_to_message

    try:

        if len(message.text.splitlines()) > 1:
            reason = message.text.splitlines()[1]



        if reply is not None:
            arg_name = reply.from_user.id
            if len(args) == 1:
                duration = int(args.split()[0])

        else:
            if len(args) > 0:
                arg_name = args.split()[0]

                if message.entities[1].user is not None:
                    arg_name = message.entities[1].user.id

                duration = int(args.split()[1])
            else:
                return await message.reply(f"Это команда должна использоваться с @user или реплай на пользователя")

        user_muted = await admin.mute(arg_name=arg_name, chat_id=message.chat.id, duration=duration, reason=reason)

        if user_muted == 0: return await message.answer(f"Невозможно замутить администратора")

        await message.answer(f"Пользователь {user_muted.link} был переключен в беззвучный режим на {duration} минут. \nМут выдан админом: {user.link}\nПричина: {reason}")

    except ValueError as e: return await message.answer(f"Произошла ошибка при попытке получить время мута: {e}")


@router.message(Command('unmute'))
async def mute_command(
    message: Message,
    user: User,
    admin: Admin
):
    args = message.text.splitlines()[0].split('/unmute')[1]


    arg_name = None

    reply = message.reply_to_message

    try:



        if reply is not None:
            arg_name = reply.from_user.id

        else:
            if len(args) > 0:
                arg_name = args.split()[0]

                if message.entities[1].user is not None:
                    arg_name = message.entities[1].user.id

            else:
                return await message.reply(f"Это команда должна использоваться с @user или реплай на пользователя")

        user_unmuted = await admin.unmute(arg_name=arg_name, chat_id=message.chat.id,)

        if user_unmuted == 0: return await message.answer(f"Администратор никогда не может быть замучен")

        await message.answer(f"Пользователю {user_unmuted.link} было разрешено говорить.")

    except ValueError as e: return await message.answer(f"Произошла ошибка при попытке получить время мута: {e}")

@router.message(Command('warn'))
async def warn_command(
    message: Message,
    user: User,
    admin: Admin
):
    reason = message.text.lower().split('/warn')[1]

    reply = message.reply_to_message
    if not reply:
        return await message.reply(f"Необходимо ответить на сообщение нарушителя")

    result = await admin.warn(
        chat_id=message.chat.id,
        user_id=reply.from_user.id,
        reason=reason
    )

    if result == 0: return await message.reply(f"Невозможно выдать предупреждение администратору")

    my_message = await message.answer(f"Пользователю {result.link} было выдано {result.warns} предупреждение из 3")
    if result.warns >= 3:
        await admin.mute(
            arg_name=result.user_id,
            chat_id=message.chat.id,
            duration=(result.warns*60),
            reason=f'Превышено количество предупреждений: {result.warns}'
        )
        await my_message.edit_text(f"Пользователю {result.link} было выдано {result.warns} предупреждение из 3\n\nОн был обеззвучен на {result.warns} часов")
    

@router.message(Command('ban'))
async def ban_handler(
    message: Message,
    user: User,
    admin: Admin

    
):
    
    args = message.text.splitlines()[0].split('/ban')[1]


    arg_name = None

    reply = message.reply_to_message

    if reply is not None:
        arg_name = reply.from_user.id

    else:
        if len(args) > 0:
            arg_name = args.split()[0]

            if message.entities[1].user is not None:
                arg_name = message.entities[1].user.id

        else:
            return await message.reply(f"Это команда должна использоваться с @user или реплай на пользователя")



    my_message = await message.answer(f"Главному советнику был отправлен запрос на бан пользователя. Ожидайте")
    await admin.request_ban(arg_name, my_message.message_id)

@router.callback_query(lambda call: "ban" in call.data)
async def request_ban_handler(
    call: CallbackQuery,
    admin: Admin,
    bot: Bot
):
    if call.from_user.id != admin.main_admin_id:
        return 
    
    
    message_id = int(call.data.split("_")[2]) 
    if "reject" in call.data:

        await bot.edit_message_text("Главный советник отклонил запрос на бан.", main_chat, message_id)
        await call.message.edit_text("Вы отклонили запрос на бан")
        return 
    

    user_ban_id = int(call.data.split("_")[3]) 
    ban_user = User(admin.db)
    await ban_user.init(user_ban_id)
    await bot.ban_chat_member(main_chat, user_ban_id)
    await bot.edit_message_text(f"Главный советник принял запрос на бан.\n{ban_user.link} был забанен", main_chat, message_id)
    await call.message.edit_text(f"Вы забанили {ban_user.link}")
