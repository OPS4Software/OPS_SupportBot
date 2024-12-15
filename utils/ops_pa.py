import requests
import json


class PGAnswer:
    def __init__(self, isExists, status=None, paymentType=None, terminal=None):
        self.isExists = isExists
        self.status = status
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
    data = json.load(data_raw)
    status = data.get('status')
    print(status)
