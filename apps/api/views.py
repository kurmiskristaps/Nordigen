import json
from django.shortcuts import render
from django.http import HttpResponse
# from tasks import fetch_banks
import requests

from nordigen_api.settings import USER_SECRET_ID, USER_SECRET_KEY

def index(request: str) -> str:
    token = get_token()

    return render(request, 'index.html', {'banks': get_banks(token)})

def get_banks(token: str) -> json:
    api_url = 'https://ob.nordigen.com/api/v2/institutions/'
    
    response = requests.get(api_url, headers = {'Authorization': 'Bearer ' + token})
    response_json = json.dumps(response.text)

    return response_json

def get_token() -> str:
    api_url = 'https://ob.nordigen.com/api/v2/token/new/'

    response = requests.post(api_url, data = {'secret_id': USER_SECRET_ID, 'secret_key': USER_SECRET_KEY})
    response_json = response.json()

    return response_json['access']