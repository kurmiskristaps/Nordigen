from multiprocessing.pool import AsyncResult
from django.shortcuts import render
from nordigen import NordigenClient
from uuid import uuid4
from .tasks import fetch_transactions, fetch_balances
from django.http import JsonResponse
from celery.result import AsyncResult
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

        request.session['accounts'] = accounts
        accounts_data = []

        for id in accounts['accounts']:
            account = client.account_api(id)
            metadata = account.get_metadata()
            details = account.get_details()

            accounts_data.append(
                {
                    "id": id,
                    "metadata": metadata,
                    "details": details,
                }
            )
            
    except Exception as e:
        print('%s' % str(e))
        return render(request, 'error.html')

    return render(request, 'account.html', {'accounts': accounts_data})

async def get_transactions(account_id: str) -> JsonResponse:
    if account_id == False:
        return JsonResponse({'error': 'No account id provided'})
    task = fetch_transactions.delay(account_id, token_data['access'])
    
    return JsonResponse({'finish': task.get()})


async def get_balances(account_id: str) -> JsonResponse:
    if account_id == False:
        return JsonResponse({'error': 'No account id provided'})
    task = fetch_balances.delay(account_id, token_data['access'])
    
    return JsonResponse({'finish': task.get()})


def check_status(request):
    task_id = request.GET.get('task_id')
    if task_id:
        async_result = AsyncResult(id=task_id)
        return JsonResponse({'finish': async_result.get()})
    return JsonResponse({'error': 'No task id provided'})
