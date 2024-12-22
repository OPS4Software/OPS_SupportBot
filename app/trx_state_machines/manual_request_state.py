from app.external_connections.xano import XANO_CLIENT, XanoTrxRequest

from app.external_connections import ops_pa, clickup
from app.external_connections.ops_pa import PG_PAYMENT_TYPE, PG_TRX_STATUS
from app.external_connections.clickup import CU_TaskStatus

async def check_trx(trxrequest_data: XanoTrxRequest, bot) -> None:
    return