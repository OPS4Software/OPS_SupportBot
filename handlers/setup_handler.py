from aiogram import Router, types
from aiogram.filters import Command

import os

from app.external_connections.xano import XANO_CLIENT

router = Router()

@router.message(Command("getchatid"))
async def get_chat_id(message: types.Message):
    user_id = int(os.getenv('SUPERADMIN_TG_ID'))

    if message.from_user.id != user_id:
        await message.answer(f'Access denied for {message.from_user.first_name}')
        return

    await message.answer(f'Chat id: {message.chat.id}\nHave easy setup, {message.from_user.first_name}')
