from django.shortcuts import render
from django.http import HttpResponse
# from tasks import fe

def index(request: str) -> str:
    return render(request, 'index.html')

def get_banks() -> dict:
    banks = {}
    # banks = tasks.fetch_banks()
    
    return banks