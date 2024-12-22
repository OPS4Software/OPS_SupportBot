import asyncio
from app.trx_state_machines import manual_request_state, auto_request_state
from app.external_connections.xano import XANO_CLIENT
class Trx_State_Machine:
    def __init__(self):
        self.polling_timeout = None
        self.active_session = True
        self.bot = None
    async def start_polling(self, bot, polling_timeout: int = 10) -> None:
        self.bot = bot
        xano_exists = XANO_CLIENT is not None

        if xano_exists:
            self.polling_timeout = polling_timeout
            await self.run_polling()
        return None
    async def stop_polling(self) -> None:
        self.active_session = False

    async def run_polling(self) -> None:
        try:
            while self.active_session:
                await self.update()
                await asyncio.sleep(self.polling_timeout)
        finally:
            print("Trx state machine Polling stopped by error")
            await self.emit_shutdown()
        return

    async def emit_shutdown(self) -> None:
        return

    async def update(self) -> None:
        active_trx_requests = XANO_CLIENT.get_trx_requests()
        if active_trx_requests is None: return
        if len(active_trx_requests) < 1: return
        for trx_request in active_trx_requests:
            if trx_request.manual == False:
                await auto_request_state.check_trx(trxrequest_data=trx_request, bot=self.bot)
                continue
            elif trx_request.manual == True:
                await manual_request_state.check_trx(trxrequest_data=trx_request, bot=self.bot)
                continue


TRX_STATE_MACHINE = None