import os
from aiogram.types import Message

from utils.ops_pa import PGAnswer
from utils.clickup import ClickUpClient
from utils.xano import XanoClient

clickup_client = ClickUpClient()
xano_client = XanoClient()

async def run_state(message: Message, trx_details:PGAnswer) -> bool:
    if trx_details.paymentType == "DEPOSIT" and trx_details.paymentMethod == "UPI":
        return await state_UPI_Deposit(message, trx_details)

    return False

async def state_UPI_Deposit(message:Message, trx_details:PGAnswer) -> bool:
    #Trx status flow
    match trx_details.state:
        case "COMPLETED":
            return await state_UPI_Deposit_COMPLETED(message, trx_details)
        case "DECLINED":
            return await state_UPI_Deposit_DECLINED(message, trx_details)


async def state_UPI_Deposit_COMPLETED(message:Message, trx_details:PGAnswer) -> bool:
    return False
async def state_UPI_Deposit_DECLINED(message:Message, trx_details:PGAnswer) -> bool:
    # Checker for screenshot_url exists
    if message.content_type != 'photo':
        print('no screenshot')
        return False
    screenshot_url = message.photo[-1].file_id
    if not screenshot_url:
        print('no screenshot')
        return False

    # Send message to provider chat
    terminal_id = trx_details.terminal.split('_')[-1]
    provider = xano_client.getProviderByTerminalName(terminal_id)
    print(provider)
    await message.bot.send_photo(chat_id=provider.support_chat_id_tg, photo=screenshot_url,
                                 caption=f'New ticket by transaction ID: {trx_details.trx_id}')

    # Create ClickUp task using the class instance
    # TASK: Do normal file loader to click up. Is current one ok?
    file = await message.bot.get_file(screenshot_url)
    if not os.path.exists("tmp/img/"):
        os.makedirs("tmp/img/")
    file_local_path = f"tmp/img/{trx_details.trx_id}.jpg"
    await message.bot.download_file(file.file_path, file_local_path)
    clickup_client.create_auto_task(list_id=provider.list_id_clickup, attachment=file_local_path, pg_trx_id=trx_details.trx_id)
    return True
async def state_UPI_Deposit_CANCELED(message:Message, trx_details:PGAnswer) -> bool:
    return False
async def state_UPI_Deposit_CHECKOUT(message:Message, trx_details:PGAnswer) -> bool:
    return False
async def state_UPI_Deposit_COMPLETED(message:Message, trx_details:PGAnswer) -> bool:
    return False