import os
from aiogram.types import Message, ReactionTypeEmoji

from app.external_connections.ops_pa import PGAnswer, PG_PAYMENT_TYPE, PG_TRX_STATUS
from app.external_connections.clickup import CLICKUP_CLIENT
from app.external_connections.xano import XANO_CLIENT, XanoShop

async def run_state(message: Message, trx_details: PGAnswer, shop: XanoShop) -> bool:
    if trx_details.paymentType == PG_PAYMENT_TYPE.DEPOSIT.value and trx_details.paymentMethod == "UPI":
        return await state_UPI_Deposit(message=message, trx_details=trx_details, shop=shop)
    print(f"State 666: Trx {trx_details.trx_id}. Not such flow")
    return False


async def state_UPI_Deposit(message: Message, trx_details: PGAnswer, shop: XanoShop) -> bool:
    # Trx status flow
    match trx_details.state:
        case PG_TRX_STATUS.COMPLETED.value:
            return await state_UPI_Deposit_COMPLETED(message=message, trx_details=trx_details, shop=shop)
        case PG_TRX_STATUS.DECLINED.value:
            return await state_UPI_Deposit_DECLINED(message=message, trx_details=trx_details, shop=shop)
        case PG_TRX_STATUS.CANCELLED.value:
            return await state_UPI_Deposit_CANCELLED(message=message, trx_details=trx_details, shop=shop)
        case PG_TRX_STATUS.CHECKOUT.value:
            return await state_UPI_Deposit_CHECKOUT(message=message, trx_details=trx_details, shop=shop)
        case PG_TRX_STATUS.AWAITING_WEBHOOK.value:
            return await state_UPI_Deposit_AWAITING_WEBHOOK(message=message, trx_details=trx_details, shop=shop)
        case PG_TRX_STATUS.AWAITING_REDIRECT.value:
            return await state_UPI_Deposit_AWAITING_REDIRECT(message=message, trx_details=trx_details, shop=shop)
    print(f"State 666, UPI Deposits. Trx {trx_details.trx_id} has undetectable state: {trx_details.state}")
    return False

async def state_UPI_Deposit_COMPLETED(message: Message, trx_details: PGAnswer, shop: XanoShop) -> bool:
    await message.react(reaction=[ReactionTypeEmoji(emoji="👍")])
    await message.reply("This trx has status COMPLETED")
    return True
async def state_UPI_Deposit_DECLINED(message: Message, trx_details: PGAnswer, shop: XanoShop) -> bool:
    return await beh_send_auto_ticket(message, trx_details, shop)
async def state_UPI_Deposit_CANCELLED(message: Message, trx_details: PGAnswer, shop: XanoShop) -> bool:
    await message.reply("May you doublecheck transaction id, pls. The specified transaction id has not gone to the bank")
    return True
async def state_UPI_Deposit_CHECKOUT(message: Message, trx_details: PGAnswer, shop: XanoShop) -> bool:
    await message.reply("May you doublecheck transaction id, pls. The specified transaction id has not gone to the bank")
    return True
async def state_UPI_Deposit_AWAITING_WEBHOOK(message: Message, trx_details: PGAnswer, shop: XanoShop) -> bool:
    return await beh_send_auto_ticket(message, trx_details, shop)
async def state_UPI_Deposit_AWAITING_REDIRECT(message: Message, trx_details: PGAnswer, shop: XanoShop) -> bool:
    print(f"State 666. UPI, Deposits. Trx {trx_details.trx_id} came with unsolved state: {trx_details.state}")
    return True

async def beh_send_auto_ticket(message: Message, trx_details: PGAnswer, shop: XanoShop) -> bool:
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
    terminal_id = int(trx_details.terminal.split('_')[-1])
    provider = XANO_CLIENT.get_provider_by_terminal_name(terminal_id)
    if provider == None:
        await message.reply("@Serggiant @SavaOps, I couldn't solve it")
        print(f"State 666. Trx {trx_details.trx_id}, didn't find provider by terminal_id: {terminal_id}")
        return False
    prov_mes = await message.bot.send_photo(chat_id=provider.support_chat_id_tg, photo=screenshot_url,
                                 caption=f'New ticket by transaction ID: {trx_details.trx_id}')

    # Create ClickUp task using the class instance
    # TASK: Do normal file loader to click up. Is current one ok?
    file = await message.bot.get_file(screenshot_url)
    if not os.path.exists("tmp/img/"):
        os.makedirs("tmp/img/")
    file_local_path = f"tmp/img/{trx_details.trx_id}.jpg"
    await message.bot.download_file(file.file_path, file_local_path)

    ca_data = await CLICKUP_CLIENT.create_auto_task(list_id=provider.list_id_clickup, attachment=file_local_path,
                                                 pg_trx_id=trx_details.trx_id)

    db_trx_request_success = XANO_CLIENT.post_new_trx_request(trx_id=trx_details.trx_id, shop_data=shop, merch_mes_id=message.message_id,
                                                              provider_data=provider, provider_mes_id=prov_mes.message_id,
                                                              task_id_ca=ca_data['id'], is_manual_ticket=False)
    await message.react(reaction=[ReactionTypeEmoji(emoji="👀")])
    return db_trx_request_success