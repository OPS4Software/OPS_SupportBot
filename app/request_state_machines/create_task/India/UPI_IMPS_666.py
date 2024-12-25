import os
from aiogram.types import Message, ReactionTypeEmoji

from app.external_connections.ops_pa import PGAnswer, PG_PAYMENT_TYPE, PG_TRX_STATUS
from app.external_connections.clickup import CLICKUP_CLIENT
from app.external_connections.postgres import POSTGRES, PostgresShop

async def run_state(message: Message, trx_details: PGAnswer, shop: PostgresShop, message_full_text:str) -> bool:
    if trx_details.paymentType == PG_PAYMENT_TYPE.DEPOSIT.value and trx_details.paymentMethod == "UPI":
        return await state_UPI_Deposit(message=message, trx_details=trx_details, shop=shop, message_full_text=message_full_text)
    print(f"State 666: Trx {trx_details.trx_id}. Not such flow")
    return False


async def state_UPI_Deposit(message: Message, trx_details: PGAnswer, shop: PostgresShop, message_full_text:str) -> bool:
    # Trx status flow
    match trx_details.state:
        case PG_TRX_STATUS.COMPLETED.value:
            return await state_UPI_Deposit_COMPLETED(message=message, trx_details=trx_details, shop=shop, message_full_text=message_full_text)
        case PG_TRX_STATUS.DECLINED.value:
            return await state_UPI_Deposit_DECLINED(message=message, trx_details=trx_details, shop=shop, message_full_text=message_full_text)
        case PG_TRX_STATUS.CANCELLED.value:
            return await state_UPI_Deposit_CANCELLED(message=message, trx_details=trx_details, shop=shop, message_full_text=message_full_text)
        case PG_TRX_STATUS.CHECKOUT.value:
            return await state_UPI_Deposit_CHECKOUT(message=message, trx_details=trx_details, shop=shop, message_full_text=message_full_text)
        case PG_TRX_STATUS.AWAITING_WEBHOOK.value:
            return await state_UPI_Deposit_AWAITING_WEBHOOK(message=message, trx_details=trx_details, shop=shop, message_full_text=message_full_text)
        case PG_TRX_STATUS.AWAITING_REDIRECT.value:
            return await state_UPI_Deposit_AWAITING_REDIRECT(message=message, trx_details=trx_details, shop=shop, message_full_text=message_full_text)
    print(f"State 666, UPI Deposits. Trx {trx_details.trx_id} has undetectable state: {trx_details.state}")
    return False

async def state_UPI_Deposit_COMPLETED(message: Message, trx_details: PGAnswer, shop: PostgresShop, message_full_text:str) -> bool:
    await message.react(reaction=[ReactionTypeEmoji(emoji="👍")])
    await message.reply("This trx has status COMPLETED")
    return True
async def state_UPI_Deposit_DECLINED(message: Message, trx_details: PGAnswer, shop: PostgresShop, message_full_text:str) -> bool:
    return await beh_send_auto_ticket(message, trx_details, shop, message_full_text)
async def state_UPI_Deposit_CANCELLED(message: Message, trx_details: PGAnswer, shop: PostgresShop, message_full_text:str) -> bool:
    await message.reply("May you doublecheck transaction id, pls. The specified transaction id has not gone to the bank")
    return True
async def state_UPI_Deposit_CHECKOUT(message: Message, trx_details: PGAnswer, shop: PostgresShop, message_full_text:str) -> bool:
    await message.reply("May you doublecheck transaction id, pls. The specified transaction id has not gone to the bank")
    return True
async def state_UPI_Deposit_AWAITING_WEBHOOK(message: Message, trx_details: PGAnswer, shop: PostgresShop, message_full_text:str) -> bool:
    return await beh_send_auto_ticket(message, trx_details, shop, message_full_text)
async def state_UPI_Deposit_AWAITING_REDIRECT(message: Message, trx_details: PGAnswer, shop: PostgresShop, message_full_text:str) -> bool:
    print(f"State 666. UPI, Deposits. Trx {trx_details.trx_id} came with unsolved state: {trx_details.state}")
    return True

async def beh_send_auto_ticket(message: Message, trx_details: PGAnswer, shop: PostgresShop, message_full_text:str) -> bool:
    # Checker for screenshot_url exists
    if message.content_type != 'photo':
        await message.reply("@Serggiant @SavaOps, have a look")
        print('no screenshot')
        return False
    screenshot_url = message.photo[-1].file_id
    if not screenshot_url:
        await message.reply("@Serggiant @SavaOps, have a look")
        print('no screenshot')
        return False

    # Send message to provider chat
    terminal_index = int(trx_details.terminal.split('_')[-1])
    provider = POSTGRES.get_provider_by_terminal_index(terminal_index)
    if provider == None:
        await message.reply("@Serggiant @SavaOps, I couldn't solve it")
        print(f"State 666. Trx {trx_details.trx_id}, didn't find provider by terminal_id: {terminal_index}")
        return False
    prov_mes = await message.bot.send_photo(chat_id=provider.support_chat_id, photo=screenshot_url,
                                 caption=f'New ticket by transaction ID: {trx_details.trx_id}')

    # Create ClickUp task using the class instance
    # TASK: Do normal file loader to click up. Is current one ok?
    file = await message.bot.get_file(screenshot_url)
    if not os.path.exists("tmp/img/"):
        os.makedirs("tmp/img/")
    file_local_path = f"tmp/img/{trx_details.trx_id}.jpg"
    await message.bot.download_file(file.file_path, file_local_path)

    cu_data = await CLICKUP_CLIENT.create_auto_task(list_id=provider.cu_list_id, attachment=file_local_path,
                                                 pg_trx_id=trx_details.trx_id)

    db_ticket_request_success = POSTGRES.create_new_ticket_request(trx_id=trx_details.trx_id, shop_data=shop,
                                                                   shop_mes_id=message.message_id,
                                                                   provider_data=provider,
                                                                   provider_mes_id=prov_mes.message_id,
                                                                   cu_task_id=cu_data['id'], is_manual_ticket=False,
                                                                   message_full_text=message_full_text)
    await message.react(reaction=[ReactionTypeEmoji(emoji="👀")])
    return db_ticket_request_success