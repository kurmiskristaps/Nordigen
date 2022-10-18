from __future__ import absolute_import, unicode_literals
from nordigen.api import AccountApi
from nordigen import NordigenClient
from celery import shared_task


from nordigen_api.settings import USER_SECRET_ID, USER_SECRET_KEY

client = NordigenClient(secret_id = USER_SECRET_ID, secret_key = USER_SECRET_KEY)

@shared_task(bind=True)
async def get_transactions(self, account_id: int, token: str):
    client.token = token
    account = AccountApi(client, account_id)
    response = account.get_transactions()
    return response

@shared_task(bind=True)
async def get_balances(self, account_id: int, token: str):
    client.token = token
    account = AccountApi(client, account_id)
    response = account.get_balances()
    return response