from aiogram import Router, types
from aiogram.filters import Command
from utils.clickup import ClickUpClient
from utils.validators import validate_transaction_id

router = Router()
clickup_client = ClickUpClient()

@router.message()
async def handle_webapp_data(message: types.Message):
    if not message.web_app_data:
        return
    
    try:
        data = message.web_app_data.data
        transaction_id = data.get("transaction_id")
        screenshot_url = data.get("screenshot_url")
        notes = data.get("notes", "")

        if not validate_transaction_id(transaction_id):
            await message.answer("Invalid transaction ID format!")
            return

        if not screenshot_url:
            await message.answer("Screenshot is required!")
            return

        # Create ClickUp task using the class instance
        clickup_client.create_task(screenshot_url, transaction_id, notes)

        await message.answer(
            "✅ Transaction verification submitted successfully!"
        )

    except Exception as e:
        await message.answer(
            "❌ An error occurred while processing your request.\n"
            "Please try again later."
        )