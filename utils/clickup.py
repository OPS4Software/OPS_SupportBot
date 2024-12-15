import os

import requests

class ClickUpClient:
    def __init__(self):
        self.token = os.getenv('CLICKUP_TOKEN')
        self.list_id = os.getenv('CLICKUP_LIST_ID')
        self.team_id = os.getenv('CLICKUP_TEAM_ID')
        self.base_url = "https://api.clickup.com/api/v2"

    def create_task(self, attachment, id, description:str=None):
        url = f"{self.base_url}/list/{self.list_id}/task"

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.token
        }
        query = {
            "custom_task_ids": "true",
            "team_id": self.team_id
        }
        payload = {
            "name": f"Ticket_{id}",
            "description": f"ID: {id}\n\nDescription: {description}",
            "assignees": [
                #89657945
            ],
        }

        response = requests.post(url, json=payload, headers=headers, params=query)
        data = response.json()

        if attachment and attachment != "":
            self.add_attachment(data['id'], attachment, True)
        
        return data

    def add_attachment(self, task_id, attachment, delete_attachment=False):
        url = f"{self.base_url}/task/{task_id}/attachment"
        headers = {
            "Authorization": self.token
        }
        file = {
            "attachment": (attachment, open(attachment, 'rb'))
        }

        response = requests.post(url, files=file, headers=headers)

        if delete_attachment:
            os.remove(attachment)
        
        return response.json()