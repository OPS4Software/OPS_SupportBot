import os, json
from datetime import datetime

import requests
from dotenv import load_dotenv

class XanoShopAnswer:
    def __init__(self, id:int=None, merchant_id:str=None, management_chat:str=None, support_chat:str=None):
        self.id = id
        self.management_chat = management_chat
        self.support_chat = support_chat
        self.merchant_id = merchant_id
class XanoProviderAnswer:
    def __init__(self, provider_name:int=None, terminal_name:str=None, list_id_clickup:str=None, support_chat_id_tg:str=None):
        self.provider_name = provider_name
        self.terminal_name = terminal_name
        self.list_id_clickup = list_id_clickup
        self.support_chat_id_tg = support_chat_id_tg
class XanoTrxRequestAnswer:
    def __init__(self, id:int=None, shop_id:int=None, provider_id:int=None, pg_id:int=None, trx_id:str=None,
                 task_id_click_up:str=None, provider_support_chat_message_id_tg:str=None, merchant_support_chat_message_id_tg:str=None,
                 closed:bool=None, manual:bool=None, created_at:datetime=None):
        self.id = id
        self.shop_id = shop_id
        self.provider_id = provider_id
        self.pg_id = pg_id
        self.trx_id = trx_id
        self.task_id_click_up = task_id_click_up
        self.provider_support_chat_message_id_tg = provider_support_chat_message_id_tg
        self.merchant_support_chat_message_id_tg = merchant_support_chat_message_id_tg
        self.closed = closed
        self.manual = manual
        self.created_at = created_at
class XanoClient:
    def __init__(self):
        load_dotenv()
        self.email = os.getenv('XANO_EMAIL')
        self.password = os.getenv('XANO_PASS')
        self.base_url = os.getenv('XANO_ENDPOINT')

    def getShopApiKey(self, shop_id:int) -> str:
        token = self.auth()
        if token == None:
            return None
        print(f"shop id before request: {shop_id}")
        url = f"{self.base_url}/shops/{shop_id}/apikey"

        headers = {
            "Content-Type": "application/json",
            "Authorization": token
        }
        payload = {
            "shops_id": shop_id
        }

        response = requests.get(url, json=payload, headers=headers)
        if response.status_code != 200:
            return None
        else:
            data = response.json()
            return data['api_key']
    def getShopsByChatId(self, chat_id:str) -> list[XanoShopAnswer]:
        token = self.auth()
        if token == None:
            return None

        url = f"{self.base_url}/shops/{chat_id}/"

        headers = {
            "Content-Type": "application/json",
            "Authorization": token
        }
        payload = {
            "support_chat_id": chat_id
        }

        response = requests.get(url, json=payload, headers=headers)
        if response.status_code != 200:
            return None
        else:
            data = response.json()
            answer_array = []
            for item in data:
                try:
                    shop = XanoShopAnswer(id=item.get('id'),
                                          merchant_id=item.get('merchant_id'),
                                          support_chat=item.get('support_chat'),
                                          management_chat=item.get('management_chat')
                                          )
                    answer_array.append(shop)
                except Exception as e:
                    print(f"Xano shops list Parsing answer error: {e}")
            print(len(answer_array))
            return answer_array

    def getProviderByTerminalName(self, terminal_name:str) -> XanoProviderAnswer:
        token = self.auth()
        if token == None:
            return None

        url = f"{self.base_url}/provider/{terminal_name}/"

        headers = {
            "Content-Type": "application/json",
            "Authorization": token
        }
        payload = {
            "provider_terminal_name": terminal_name
        }

        response = requests.get(url, json=payload, headers=headers)
        print(response.status_code)
        print(response.text)
        if response.status_code != 200:
            return None
        else:
            data = response.json()
            answer = XanoProviderAnswer(provider_name=data['provider_name'],
                                        terminal_name=data['terminal_name'],
                                        list_id_clickup=data['list_id_clickup'],
                                        support_chat_id_tg=data['support_chat_id_tg'],)
            return answer
    def getMerchantsList(self):
        token = self.auth()
        url = f"{self.base_url}/merchant"

        headers = {
            "Content-Type": "application/json",
            "Authorization": token
        }
        payload = {
        }

        response = requests.get(url, json=payload, headers=headers)
        data_raw = response.text
        print(data_raw)
        data = json.loads(data_raw)
        return

    def transaction_id_exists(self, transaction_id: str) -> bool:
        """Proverava da li transaction_id postoji u bazi."""
        token = self.auth()
        if token is None:
            return False

        url = f"{self.base_url}/trxrequests/{transaction_id}/check"
        headers = {
            "Content-Type": "application/json",
            "Authorization": token
        }
        payload = {"pg_id": '0',
                   "trx_id": transaction_id
                   }

        response = requests.get(url, json=payload, headers=headers)
        print(response.status_code)
        if response.status_code != 200:
            return False
        else:
            data = response.json()
            return len(data) > 0

        return False
    def add_trxrequest(self, trx_id:str, shop_data:XanoShopAnswer, provider_data:XanoProviderAnswer, task_id_ca:str, isManualTask:bool) -> bool:
        token = self.auth()
        if token == None:
            return False
        url = f"{self.base_url}/trxrequests"

        headers = {
            "Content-Type": "application/json",
            "Authorization": token
        }
        payload = {
                    "shop_id": shop_data.id,
                    "provider_id": provider_data.id,
                    "pg_id": 0,
                    "trx_id": trx_id,
                    "task_id_click_up": task_id_ca,
                    "provider_support_chat_message_id_tg": provider_data.support_chat_id_tg,
                    "shop_support_chat_message_id_tg": shop_data.support_chat,
                    "Closed": False,
                    "Manual": isManualTask
                }

        response = requests.post(url, json=payload, headers=headers)

        return response.status_code == 200
    def auth(self) -> str:
        url = f"{self.base_url}/auth/login"

        headers = {
            "Content-Type": "application/json",
        }
        payload = {
                    "email": self.email,
                    "password": self.password
                }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data_raw = response.text
            data = json.loads(data_raw)
            token = data['authToken']
        else:
            token = None
        return token