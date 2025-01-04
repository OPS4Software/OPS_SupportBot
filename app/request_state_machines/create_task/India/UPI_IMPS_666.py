import os
from aiogram.types import Message, ReactionTypeEmoji

from app.external_connections.ops_pa import PGAnswer, PG_PAYMENT_TYPE, PG_TRX_STATUS
from app.external_connections.clickup import CLICKUP_CLIENT
from app.external_connections.postgres import POSTGRES, PostgresShop
async def beh_send_auto_ticket(message: Message, trx_details: PGAnswer, shop: PostgresShop, message_full_text:str) -> bool:
    # Checker for screenshot_url exists
    if message.content_type not in ['photo', 'document']:
        await message.reply("@Serggiant, have a look")
        print('no screenshot')
        return False
    screenshot_url = message.photo[-1].file_id
    if not screenshot_url:
        await message.reply("@Serggiant, have a look")
        print('no screenshot')
        return False
    
    # Get all attachments from the message
    attachments = []
    if message.content_type == 'photo':
        attachments = message.photo
    elif message.content_type == 'document':
        attachments = [message.document]

    # Send message to provider chat
    terminal_index = int(trx_details.terminal.split('_')[-1])
    provider = POSTGRES.get_provider_by_terminal_index(terminal_index)
    if provider == None:
        await message.reply("@Serggiant, I couldn't solve it")
        print(f"State 666. Trx {trx_details.trx_id}, didn't find provider by terminal_id: {terminal_index}")
        return False
    
    media_group = []
    for attachment in attachments:
        if attachment.mime_type.startswith('image/'):
            media_group.append(InputMediaPhoto(media=attachment.file_id))
        else:
            media_group.append(InputMediaDocument(media=attachment.file_id))

    prov_mes = await message.send_media_group(chat_id=provider.support_chat_id, media=media_group,
                                 caption=f'New ticket by transaction ID: {trx_details.trx_id}')

    # Create ClickUp task using the class instance
    # TASK: Do normal file loader to click up. Is current one ok?
    attachments_for_clickup = []
    for attachment in attachments:
        try:    
            file = await message.bot.get_file(attachment.file_id)
            if not os.path.exists("tmp/img/"):
                os.makedirs("tmp/img/")
            file_local_path = f"tmp/img/{trx_details.trx_id}_{attachment.file_id}.jpg"
            await message.bot.download_file(file.file_path, file_local_path)
            attachments_for_clickup.append(file_local_path)
        except Exception as e:
            print(f"Error downloading file: {e}")
            return False

    
    try:
        cu_data = await CLICKUP_CLIENT.create_auto_task(list_id=provider.cu_list_id, attachments=attachments_for_clickup,
                                                 pg_trx_id=trx_details.trx_id)
    except Exception as e:
        print(f"Error creating task: {e}")
        return False    

    db_ticket_request_success = POSTGRES.create_new_ticket_request(trx_id=trx_details.trx_id, shop_data=shop,
                                                                shop_mes_id=message.message_id,
                                                                provider_data=provider,
                                                                provider_mes_id=prov_mes.message_id,
                                                                cu_task_id=cu_data['id'], is_manual_ticket=False,
                                                                message_full_text=message_full_text)
    await message.react(reaction=[ReactionTypeEmoji(emoji="👀")])
    return db_ticket_request_success