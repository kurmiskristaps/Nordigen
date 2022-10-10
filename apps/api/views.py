import json
from django.shortcuts import render
from django.http import HttpResponse
# from tasks import fetch_banks
import requests

def index(request: str) -> str:
    return render(request, 'index.html', {'banks': get_banks()})

def get_banks() -> json:
    # banks = fetch_banks()
    api_url = 'https://ob.nordigen.com/api/v2/institutions'
    
    response = requests.get(api_url, headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1NTIwMjI4LCJqdGkiOiI5ZjZkYWU2MzNlYTM0MmJhYWIzOWUzYjg0NTgwZGIxNCIsImlkIjoxNjkxNSwic2VjcmV0X2lkIjoiYTQ3MTJmMWQtNTU1Ny00NzU1LWE1OTgtNjA1OTUxYWM5OTY0IiwiYWxsb3dlZF9jaWRycyI6WyIwLjAuMC4wLzAiLCI6Oi8wIl19.wHwudZetMTe_vj9auNkWuv0QKXPbQBXhZkeMNBLl2As'})

    print(response.text)

    return response.content
    # return banks