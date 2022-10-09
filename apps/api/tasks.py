from __future__ import absolute_import, unicode_literals
from urllib import request
from celery import shared_task

@shared_task
def fetch_banks() -> dict:
    api_url = 'https//www.ob.nordigen.com/api/v2/institutions/'
    
    response = request.get(api_url)
    return response.json