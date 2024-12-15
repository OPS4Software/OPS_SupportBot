import requests
import json


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


def check_status(merchant_chat_id:str, trx_id:str) -> PGAnswer:
    ## TEMP: HARDCORE ZONE
    # TASK: Take API key from DB based on merchant_chat_id. IF no API key - return PGAnswer FALSE
    API_Key = "zMimE4ZayUDaR4z3QgFeb6FnPHx5gSV2"

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