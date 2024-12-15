import requests
import json
from utils.xano import XanoClient

xano_client = XanoClient()

class PGAnswer:
    def __init__(self, isExists:bool, trx_id:str=None, ref_id:str=None,
                 state:str=None, paymentType:str=None, paymentMethod:str=None,
                 terminal:str=None):
        self.isExists = isExists
        self.ref_id = ref_id
        self.trx_id = trx_id
        self.state = state
        self.paymentType = paymentType
        self.paymentMethod = paymentMethod
        self.terminal = terminal


def check_status(shop_chat_id:int, trx_id:str) -> PGAnswer:
    API_Key = xano_client.getShopApiKey(shop_chat_id)
    if API_Key == None:
        return PGAnswer(isExists=False)

    url = f"https://app.inops.net/api/v1/payments/{trx_id}"
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_Key}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data_raw = response.text

    data = json.loads(data_raw)
    status = int(data['status'])

    if status == 200:
        answer = PGAnswer(isExists=True,
                          trx_id=data['result']['id'],
                          ref_id=data['result']['referenceId'],
                          state=data['result']['state'],
                          paymentType=data['result']['paymentType'],
                          paymentMethod=data['result']['paymentMethod'],
                          terminal=data['result']['terminalName'])
    else:
        answer = PGAnswer(False)
    return answer