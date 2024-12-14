from aiogram import Router, types
from aiogram.filters import Command

import os
from dotenv import load_dotenv

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    load_dotenv()
    user_id = int(os.getenv('SUPERADMIN_TG_ID'))

    if message.from_user.id != user_id:
        await message.answer(f'Access denied for {message.from_user.id}')
        return

    await message.answer('Access granted')