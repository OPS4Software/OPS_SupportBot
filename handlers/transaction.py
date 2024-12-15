import os
import sys

from aiogram import Router
from aiogram.types import Message, ReactionTypeEmoji
from utils.validators import validate_transaction_id

import utils.state_machines.transactions_state_machine as state_machine

from utils.xano import XanoClient, XanoShopAnswer

router = Router()
xano_client = XanoClient()

@router.message()
async def detect_message(message: Message):
    # Checker: is chat register?
    xano_shops_answer:list[XanoShopAnswer] = xano_client.getShopsByChatId(message.chat.id)
    if xano_shops_answer == None:
        return

    print('shop(s) exists')

    # TASK: checker: what type of merchant? WHAT IS IT??? FOR WHAT??? FIND AN ANSWER FOR IT
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

    #TEMP: Checker for transaction_id exists by FORMAT
    if transaction_id == None:
        return
    # Run Request state analizator

    shops_id = [int]
    for shop in xano_shops_answer:
        shops_id.append(shop.id)
    state_machine_success = await state_machine.run_state_machine(message, transaction_id, shops_id)

    if state_machine_success == False:
        print('state machine FALSE')
        return

    await message.react(reaction=[ReactionTypeEmoji(emoji="👀")])

    # except Exception as e:
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     print(e, exc_type, fname, exc_tb.tb_lineno)