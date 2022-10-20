from multiprocessing.pool import AsyncResult
from django.shortcuts import render
from nordigen import NordigenClient
from .tasks import initialize_session, get_institutions, get_accounts, get_account_data, fetch_transactions

from django.http import JsonResponse, HttpRequest
from celery.result import AsyncResult
from django.shortcuts import redirect
from nordigen_api.settings import USER_SECRET_ID, USER_SECRET_KEY

def index(request: str):
    try:
        institutions = get_institutions()
    except Exception:
        return render(request, 'error.html')

    return render(request, 'index.html', {'banks': institutions})


def auth(request: str, institution_id: str):
    if (institution_id):
        try:
            init = initialize_session(
                institution_id=institution_id,
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
        accounts = get_accounts(
            requisition_id = request.session['req_id']
        )

        request.session['ref'] = request.GET.get('ref')

        request.session['accounts'] = accounts
        accounts_data = []

        for id in accounts['accounts']:
            data = get_account_data(id)

            accounts_data.append(data)
            
    except Exception as e:
        print('%s' % str(e))
        return render(request, 'error.html')

    return render(request, 'account.html', {'accounts': accounts_data})

def get_transactions(request):
    account_id = request.GET.get('account_id')

    if account_id == False:
        return JsonResponse({'error': 'No account id provided'})

    task = fetch_transactions.delay(account_id)

    return JsonResponse({'finish': task.get()})


def get_balances(request) -> JsonResponse:
    account_id = request.GET.get('account_id')
    
    if account_id == False:
        return JsonResponse({'error': 'No account id provided'})
    # task = fetch_balances.delay(account_id, token_data['access'])
    
    return {'finish': 'lol'}


def check_status(request):
    task_id = request.GET.get('task_id')
    if task_id:
        async_result = AsyncResult(id=task_id)
        return JsonResponse({'finish': async_result.get()})
    return JsonResponse({'error': 'No task id provided'})
