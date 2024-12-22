import asyncio

from aiogram.types import ReactionTypeEmoji

from app.external_connections.xano import XANO_CLIENT, XanoTrxRequest

from app.external_connections import ops_pa
from app.external_connections.ops_pa import PG_PAYMENT_TYPE, PG_TRX_STATUS
from app.external_connections.clickup import CLICKUP_CLIENT, CU_TaskStatus

async def check_trx(trxrequest_data: XanoTrxRequest, bot) -> None:
    pg_data = ops_pa.check_status(shop_id=str(trxrequest_data.shop_id), trx_id=trxrequest_data.trx_id)
    if pg_data == None:
        print(f"Couldn't check trx request: {trxrequest_data.id}")
        return
    if pg_data.state == PG_TRX_STATUS.COMPLETED.value:
        # Change DB Request status to CLOSE
        trxrequest_data.closed = True
        db_patch_result = XANO_CLIENT.patch_trx_request(trxrequest_data)
        if db_patch_result == False:
            print(f"AUTO_REQUEST_STATE: became completed, but didn't change in DB: {trxrequest_data.id}")

        # Answer in merchant chat
        await bot.set_message_reaction.SetMessageReaction(chat_id=trxrequest_data.shop_support_chat_id, message_id=trxrequest_data.shop_message_id, reaction=[ReactionTypeEmoji(emoji="👍")])
        await bot.send_message(chat_id=trxrequest_data.shop_support_chat_id, text='New transaction status: COMPLETED', reply_to_message_id=trxrequest_data.shop_message_id)
        # TASK: close clickup
        await CLICKUP_CLIENT.update_task_status(trxrequest_data.task_id_click_up, CU_TaskStatus.COMPLETE)
        await asyncio.sleep(10)
        return
    return