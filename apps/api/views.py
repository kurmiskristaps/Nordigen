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
    institutions = client.institution.get_institutions()

    return render(request, 'index.html', {'banks': institutions})


def auth(request: str, institution_id: str):
    if (institution_id):
        init = client.initialize_session(
            institution_id=institution_id,
            redirect_uri="http://localhost:8000/index/details",
            reference_id=str(uuid4())
        )

        link = init.link
        request.session['req_id'] = init.requisition_id

        return redirect(link)
    return redirect('/index')

def details(request: str):
    accounts = client.requisition.get_requisition_by_id(
        requisition_id = request.session['req_id']
    )
    request.session['ref'] = request.GET.get('ref', '')

    return HttpResponse(accounts)
