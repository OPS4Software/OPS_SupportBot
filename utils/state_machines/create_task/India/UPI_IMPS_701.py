import os
from aiogram.types import Message

from utils.ops_pa import PGAnswer
from utils.clickup import ClickUpClient

clickup_client = ClickUpClient()

async def run_state(message: Message, trx_details:PGAnswer) -> bool:
    if trx_details.paymentType == "DEPOSIT" and trx_details.paymentMethod == "UPI":
        return await state_UPI_Deposit(message, trx_details)

    return False

async def state_UPI_Deposit(message:Message, trx_details:PGAnswer) -> bool:
    # TEMP: Checker for screenshot_url exists
    if message.content_type != 'photo':
        print('no screenshot')
        return False
    screenshot_url = message.photo[-1].file_id
    if not screenshot_url:
        print('no screenshot')
        return False
    # Send message to provider chat
    # TEMP: Hardcoded provider CHAT ID
    await message.bot.send_photo(chat_id=os.getenv('SUPPORTCHAT_PAY2M'), photo=screenshot_url,
                                 caption=f'New ticket by transaction ID: {trx_details.trx_id}')

    # Create ClickUp task using the class instance
    # TASK: Do normal file loader to click up. Is current one ok?
    file = await message.bot.get_file(screenshot_url)
    if not os.path.exists("tmp/img/"):
        os.makedirs("tmp/img/")
    file_local_path = f"tmp/img/{trx_details.trx_id}.jpg"
    await message.bot.download_file(file.file_path, file_local_path)
    clickup_client.create_task(file_local_path, trx_details.trx_id)
    return True