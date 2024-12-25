from aiogram.types import Message
import app.external_connections.ops_pa as ops_pa
from app.external_connections.postgres import POSTGRES, PostgresShop, PostgresApiKey

import app.request_state_machines.create_task.India.UPI_IMPS_701 as apm701
import app.request_state_machines.create_task.India.UPI_IMPS_666 as apm000


# Check trx exists
async def run_state_machine(message: Message, transaction_id: str, shops: list[PostgresShop], message_full_text) -> bool:
    pg_answer = None
    shop = None
    for possible_shop in shops:
        shop_api_key = POSTGRES.get_shop_api_key(possible_shop.pg_api_key_id).pg_api_key
        pg_answer = ops_pa.check_status(shop_api_key, transaction_id)
        if pg_answer is not None:
            shop = possible_shop
            break
    if shop is None:
        await message.reply("This transaction ID doesn't exists\nTry again with correct OPS transaction ID inside")
        return False

    terminal_id = pg_answer.terminal.split('_')[-1]
    match int(terminal_id):
        case 666:
            success = await apm000.run_state(message, pg_answer, shop, message_full_text)
            return success
        case 701:
            success = await apm701.run_state(message, pg_answer, shop, message_full_text)
            return success
    print(f"Terminal: {terminal_id}. Not found in states")
    return False
