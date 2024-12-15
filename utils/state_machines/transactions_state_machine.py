from aiogram.types import Message
import utils.ops_pa as ops_pa

import utils.state_machines.create_task.India.UPI_IMPS_701 as apm701


# TASK: RECEIVE terminal name IF == *_UPI/IMPS_701 ->go to local terminal state machine and write all behavior there

# Check trx exists
async def run_state_machine(message: Message, transaction_id: str, shops_id: list[int]) -> bool:
    trx_found = False
    for shop in shops_id:
        answer = ops_pa.check_status(shop, transaction_id)
        print(answer.isExists)
        if answer.isExists:
            trx_found = True
            break
    if trx_found == False:
        await message.reply("This transaction ID doesn't exists\nTry again with correct OPS transaction ID inside")
        return False

    terminal_id = answer.terminal.split('_')[-1]
    match int(terminal_id):
        case 701:
            success = await apm701.run_state(message, answer)
            return success

    return False
