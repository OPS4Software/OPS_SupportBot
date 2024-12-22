from aiogram.types import Message
import app.external_connections.ops_pa as ops_pa
from app.external_connections.xano import XanoShop

import app.request_state_machines.create_task.India.UPI_IMPS_701 as apm701
import app.request_state_machines.create_task.India.UPI_IMPS_666 as apm000


# Check trx exists
async def run_state_machine(message: Message, transaction_id: str, shops: list[XanoShop]) -> bool:
    pg_answer = None
    shop = None
    for possible_shop in shops:
        pg_answer = ops_pa.check_status(possible_shop.api_key, transaction_id)
        if pg_answer is not None:
            shop = possible_shop
            break
    if shop is None:
        await message.reply("This transaction ID doesn't exists\nTry again with correct OPS transaction ID inside")
        return False

    terminal_id = pg_answer.terminal.split('_')[-1]
    match int(terminal_id):
        case 666:
            success = await apm000.run_state(message, pg_answer, shop)
            return success
        case 701:
            success = await apm701.run_state(message, pg_answer, shop)
            return success
    print(f"Terminal: {terminal_id}. Not found in states")
    return False
