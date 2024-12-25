import asyncio, datetime

from aiogram.types import ReactionTypeEmoji

from app.external_connections.postgres import POSTGRES, PostgresTicketRequest

from app.external_connections import ops_pa
from app.external_connections.ops_pa import PG_PAYMENT_TYPE, PG_TRX_STATUS
from app.external_connections.clickup import CLICKUP_CLIENT, CU_TaskStatus

async def check_trx(ticket_data: PostgresTicketRequest, bot) -> None:
    shop_data = POSTGRES.get_shop_by_id(ticket_data.shop_id)
    shop_api_key = POSTGRES.get_shop_api_key(shop_data.pg_api_key_id).pg_api_key
    pg_data = ops_pa.check_status(shop_api_key=shop_api_key, trx_id=ticket_data.trx_id)
    if pg_data == None:
        print(f"Couldn't check trx request: {ticket_data.id}")
        return
    if pg_data.state == PG_TRX_STATUS.COMPLETED.value:
        # Change DB Request status to CLOSE
        ticket_data.closed = True
        db_patch_result = POSTGRES.close_ticket(ticket_data.id, True)
        #if db_patch_result == False:
        #    print(f"AUTO_REQUEST_STATE: became completed, but didn't change in DB: {ticket_data.id}")

        # Answer in merchant chat
        await bot.set_message_reaction(chat_id=shop_data.support_chat_id, message_id=ticket_data.shop_message_id, reaction=[ReactionTypeEmoji(emoji="👍")])
        await bot.send_message(chat_id=shop_data.support_chat_id, text=f'New transaction status: COMPLETED\n\n{ticket_data.message_full_text}', reply_to_message_id=ticket_data.shop_message_id)
        # TASK: close clickup
        await CLICKUP_CLIENT.update_task_status(ticket_data.cu_task_id, CU_TaskStatus.COMPLETE)
        return
    return