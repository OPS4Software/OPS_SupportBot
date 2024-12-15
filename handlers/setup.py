from aiogram import Router, types
from aiogram.filters import Command
from utils.xano import XanoClient

import os
from dotenv import load_dotenv

router = Router()
xano_client = XanoClient()

@router.message(Command("xanologin"))
async def xano_login(message: types.Message):
    xano_client.auth()
@router.message(Command("xanogetallmerchants"))
async def xano_getmerchantslist(message: types.Message):
    xano_client.getMerchantsList()
@router.message(Command("xanogetshopbychatid"))
async def xano_getshopbychatid(message: types.Message):
    print(message.chat.id)
    xano_client.getShopsByChatId(message.chat.id)
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    load_dotenv()
    user_id = int(os.getenv('SUPERADMIN_TG_ID'))

    if message.from_user.id != user_id:
        await message.answer(f'Access denied for {message.from_user.id}')
        return

    await message.answer('Access granted')