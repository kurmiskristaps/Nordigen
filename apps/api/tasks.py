from __future__ import absolute_import, unicode_literals
from multiprocessing.pool import AsyncResult
from celery import shared_task
import requests
from uuid import uuid4
from nordigen import NordigenClient
from nordigen_api.settings import USER_SECRET_ID, USER_SECRET_KEY


client = NordigenClient(
    secret_id=USER_SECRET_ID,
    secret_key=USER_SECRET_KEY
)
token_data = client.generate_token()

accounts = []

def initialize_session(institution_id):
    return client.initialize_session(
        institution_id=institution_id,
        redirect_uri="http://localhost:8000/index/details",
        reference_id=str(uuid4())
    )

def get_institutions():
    return client.institution.get_institutions()

def get_accounts(requisition_id):
    return client.requisition.get_requisition_by_id(
        requisition_id = requisition_id
    )

def get_account_data(account_id):
    account = client.account_api(account_id)
    metadata = account.get_metadata()
    details = account.get_details()

    accounts[account_id] = account

    return  {
        "id": account_id,
        "metadata": metadata,
        "details": details,
    }

@shared_task(bind=True)
def fetch_transactions(self, account_id: str):
    account = client.account_api(account_id)
    
    return account.get_transactions()

