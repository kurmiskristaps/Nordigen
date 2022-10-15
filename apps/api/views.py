import json
from django.shortcuts import render
from django.http import HttpResponse
from nordigen import NordigenClient
from uuid import uuid4
from django.shortcuts import redirect
from nordigen_api.settings import USER_SECRET_ID, USER_SECRET_KEY

client = NordigenClient(
    secret_id=USER_SECRET_ID,
    secret_key=USER_SECRET_KEY
)

token_data = client.generate_token()


def index(request: str):
    try:
        institutions = client.institution.get_institutions()
    except Exception:
        return render(request, 'error.html')
        
    return render(request, 'index.html', {'banks': institutions})


def auth(request: str, institution_id: str):
    if (institution_id):
        try:
            init = client.initialize_session(
                institution_id=institution_id,
                redirect_uri="http://localhost:8000/index/details",
                reference_id=str(uuid4())
            )

            link = init.link
            request.session['req_id'] = init.requisition_id
        except Exception:
            return render(request, 'error.html')

        return redirect(link)
    return redirect('/index')

def details(request: str):
    if len(request.session['req_id']) == 0:
        return redirect('/index')

    try:
        accounts = client.requisition.get_requisition_by_id(
            requisition_id = request.session['req_id']
        )

        request.session['ref'] = request.GET.get('ref')

        accounts_data = []

        for id in accounts['accounts']:
            account = client.account_api(id)
            metadata = account.get_metadata()
            transactions = account.get_transactions()
            details = account.get_details()
            balances = account.get_balances()

            accounts_data.append(
                {
                    "metadata": metadata,
                    "details": details,
                    "balances": balances,
                    "transactions": transactions,
                }
            )
    except Exception:
        return render(request, 'error.html')

    return HttpResponse(accounts_data)