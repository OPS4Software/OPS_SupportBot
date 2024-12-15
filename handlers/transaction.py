from aiogram import Router
from aiogram.types import Message, ReactionTypeEmoji
from utils.clickup import ClickUpClient
from utils.validators import validate_transaction_id

import utils.state_machines.transactions_state_machine as state_machine

router = Router()
clickup_client = ClickUpClient()

@router.message()
async def detect_message(message: Message):
    # TASK: checker: is chat register?
    # TASK: checker: what type of this chat = Merchant/Provider?
    # TASK: checker: what type of merchant?
    try:
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
            print('no trx id')
            return
        # TASK: SEND terminal name to  transaction_state_machine.py -> local terminal and write all behavior there
        state_machine_success = await state_machine.run_state_machine(message, transaction_id, "123")

        if state_machine_success == False:
            print('state machine FALSE')

        await message.react(reaction=[ReactionTypeEmoji(emoji="👀")])

    except Exception as e:
        print('pass')