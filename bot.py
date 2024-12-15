from aiogram import Bot, Dispatcher
import asyncio

import os
from dotenv import load_dotenv

from handlers.transaction import router as transaction_router
from handlers.setup import router as setup_router

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

# Register routers
dp.include_routers(setup_router,
                   transaction_router)

async def main():
    load_dotenv()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())