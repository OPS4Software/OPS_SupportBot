import requests
import json


class PGAnswer:
    def __init__(self, isExists, state=None, paymentType=None, terminal=None):
        self.isExists = isExists
        self.state = state
        self.paymentType = paymentType
        self.terminal = terminal


def check_status(merchant_chat_id: str, trx_id: str) -> PGAnswer:
    ## TEMP: HARDCORE ZONE
    # TASK: Take API key from DB based on merchant_chat_id
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

    if status == 404:
        answer = PGAnswer(False)
        return answer
    elif status == 200:
        answer = PGAnswer(isExists=True,
                          state=data['result']['state'],
                          paymentType=data['result']['paymentType'],
                          terminal=data['result']['terminalName'])
        return answer

