from __future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task
def add(x: int, y: int) -> int:
    return x + y

@shared_task
def fetch_banks() -> dict:
    banks = {'lol': 'haha'}
    
    return banks