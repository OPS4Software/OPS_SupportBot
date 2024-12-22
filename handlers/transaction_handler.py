from aiogram import Router
from aiogram.types import Message, ReactionTypeEmoji

from utils.debugger import TIME_DEBUGGER
from utils.validators import validate_transaction_id

import app.request_state_machines.request_state_machine as state_machine

from app.external_connections.xano import XANO_CLIENT, XanoShop

router = Router()

@router.message()
async def detect_message(message: Message):
    TIME_DEBUGGER.debug_time("start")
    # try:
    if message.caption != None:
        raw_text = str(message.caption)
    elif message.text != None:
        raw_text = str(message.text)
    paragraphs = raw_text.split("\n")
    transaction_id = None
    for paragraph in paragraphs:
        texts = paragraph.split(" ")
        for text in texts:
            if validate_transaction_id(text):
                transaction_id = text
                break

    if transaction_id == None:
        return

    # Checker: is chat register
    xano_shops_answer:list[XanoShop] = XANO_CLIENT.get_shops_by_support_chat_id(str(message.chat.id))
    if xano_shops_answer == None:
        await message.reply("@Serggiant @SavaOps, I couldn't solve it")
        print(f"Chat {message.chat.id} is not reqistered as Shop")
        return
    # Run Request state analizator
    state_machine_success = await state_machine.run_state_machine(message, transaction_id, xano_shops_answer)
    if state_machine_success == False:
        print(f"State machine: FALSE. Chat: {message.chat.id}, Trx_id: {transaction_id}")
        return
    TIME_DEBUGGER.debug_time("finish")