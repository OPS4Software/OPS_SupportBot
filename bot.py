from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo
import asyncio
import os
from config import TOKEN, WEBAPP_URL, SUPPORTCHAT_PAY2M
from handlers.transaction import router as transaction_router
from utils.clickup import ClickUpClient

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Register routers
dp.include_router(transaction_router)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text="Verify Transaction",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )]
        ]
    )
    await message.answer(
        "Welcome to Transaction Verification Bot!\n"
        "Click the button below to start verification:",
        reply_markup=keyboard
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())