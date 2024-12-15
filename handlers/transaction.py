import os

from aiogram import Router
from aiogram.types import Message, ReactionTypeEmoji
from utils.clickup import ClickUpClient
from utils.validators import validate_transaction_id

import utils.ops_pa as ops

router = Router()
clickup_client = ClickUpClient()

@router.message()
async def detect_message(message: Message):
    # TASK: checker: is chat register?
    # TASK: checker: what type of this chat = Merchant/Provider?
    # TASK: checker: what type of merchant?
    #try:
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

        #TEMP: Checker for transaction_id exists
        if transaction_id == None:
            print('no trx id')
            return

        # TASK: checker: what type terminal?
        ops.check_status("123", transaction_id)

        if message.content_type != 'photo':
            print('no photo')
            return
        screenshot_url = message.photo[-1].file_id
        notes = "NOTES"

        # TEMP: Checker for screenshot_url exists
        if not screenshot_url:
            print('no screenshot')
            return

        # Create ClickUp task using the class instance
        # TASK: Do normal file loader to click up. Is current one ok?
        file = await message.bot.get_file(screenshot_url)
        if not os.path.exists("tmp/img/"):
            os.makedirs("tmp/img/")
        file_local_path = f"tmp/img/{transaction_id}.jpg"
        await message.bot.download_file(file.file_path, file_local_path)
        clickup_client.create_task(file_local_path, transaction_id, notes)

        await message.react(reaction=[ReactionTypeEmoji(emoji="👀")])

    #except Exception as e:
    #    print('pass')