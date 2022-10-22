from __future__ import absolute_import, unicode_literals
from multiprocessing.pool import AsyncResult
from celery import shared_task
import requests

@shared_task()
def fetch_transactions(account_id: str, token: str) -> AsyncResult:
    url = 'https://ob.nordigen.com/api/v2/accounts/' + account_id + '/transactions'
    headers = {'accept': 'application/json', 'Authorization': 'Bearer ' + token}
    
    return requests.get(url, headers=headers).json()


@shared_task()
def fetch_balances(account_id: str, token: str) -> AsyncResult:
    url = 'https://ob.nordigen.com/api/v2/accounts/' + account_id + '/balances'
    headers = {'accept': 'application/json', 'Authorization': 'Bearer ' + token}
    
    return requests.get(url, headers=headers).json()


@shared_task()
def fetch_details(account_id: str, token: str) -> AsyncResult:
    url = 'https://ob.nordigen.com/api/v2/accounts/' + account_id + '/details'
    headers = {'accept': 'application/json', 'Authorization': 'Bearer ' + token}
    data = {'accept': 'application/json', 'Authorization': 'Bearer ' + token}
    
    return requests.get(url, headers=headers).json()


@shared_task()
def fetch_premium_transactions(account_id: str, token: str) -> AsyncResult:
    url = 'https://ob.nordigen.com/api/v2/accounts/premium/' + account_id + '/transactions'
    headers = {'accept': 'application/json', 'Authorization': 'Bearer ' + token}
    
    return requests.get(url, headers=headers).json()


