from aiogram import Router, types
from aiogram.filters import Command
from utils.xano import XanoClient

import os

router = Router()
xano_client = XanoClient()

@router.message(Command("getchatid"))
async def getchatid(message: types.Message):
    user_id = int(os.getenv('SUPERADMIN_TG_ID'))

    if message.from_user.id != user_id:
        await message.answer(f'Access denied for {message.from_user.first_name}')
        return

    await message.answer(f'Chat id: {message.chat.id}\nHave easy setup, {message.from_user.first_name}')

@router.message(Command("test"))
async def getchatid(message: types.Message):
    isTrxExists = xano_client.transaction_id_exists(transaction_id="tarragonnectarine")
    await message.answer(f"{isTrxExists}")
