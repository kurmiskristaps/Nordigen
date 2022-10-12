import json
from django.shortcuts import render
from django.http import HttpResponse
# from tasks import fetch_banks
from nordigen import NordigenClient
from uuid import uuid4
from django.shortcuts import redirect
import requests

from nordigen_api.settings import USER_SECRET_ID, USER_SECRET_KEY

client = NordigenClient(
    secret_id=USER_SECRET_ID,
    secret_key=USER_SECRET_KEY
)

token_data = client.generate_token()

def index(request: str):
    institutions = client.institution.get_institutions()

    return render(request, 'index.html', {'banks': institutions})

def auth(request: str, institution_id: str):
    init = client.initialize_session(
        institution_id=institution_id,
        redirect_uri="http://127.0.0.1:8000/index/details",
        reference_id=str(uuid4())
    )

    accounts = client.requisition.get_requisition_by_id(
        requisition_id=init.requisition_id
    )

    link = init.link
    requisition_id = init.requisition_id

    return redirect(link)

def details(request: str):

    return()

# def get_token() -> str:
#     api_url = 'https://ob.nordigen.com/api/v2/token/new/'

#     response = requests.post(api_url, data = {'secret_id': USER_SECRET_ID, 'secret_key': USER_SECRET_KEY})
#     response_json = response.json()

#     return response_json['access']

# def get_banks(token: str) -> json:
#     api_url = 'https://ob.nordigen.com/api/v2/institutions/'
    
#     response = requests.get(api_url, headers = {'Authorization': 'Bearer ' + token})
#     response_json = json.dumps(response.text)

#     return response_json