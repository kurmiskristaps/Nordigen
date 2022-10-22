from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .tasks import fetch_transactions, fetch_balances, fetch_details, fetch_premium_transactions
from nordigen import NordigenClient
from nordigen_api.settings import USER_SECRET_ID, USER_SECRET_KEY
from uuid import uuid4


client = NordigenClient(
    secret_id=USER_SECRET_ID,
    secret_key=USER_SECRET_KEY
)

def index(request: str):
    try:
        request.session['token'] = client.generate_token()
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
        print('Requisition_id = ' + request.session['req_id'])
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

            accounts_data.append({
                "id": id,
                "metadata": metadata,
                "details": details,
            })
            
    except Exception as e:
        print('%s' % str(e))
        return render(request, 'error.html')

    return render(request, 'account.html', {'accounts': accounts_data})


def validate_account_id(account_id):
    if not account_id or not isinstance(account_id, str):
        raise ValidationError('No account id provided')


def validate_date(date):
    if date and not isinstance(date, str):
        raise ValidationError('Invalid date')


def validate_dates(date_from, date_to):
    for date in (date_from, date_to):
        validate_date(date)
    if date_from and date_to:
        if date_from > date_to:
            raise ValidationError('Invalid date')


def validate_country(country):
    if country and (not isinstance(country, str) or len(country) != 2):
        raise ValidationError('Invalid country format')


def validate_transaction_variables(account_id, date_from, date_to, country):
    validate_account_id(account_id)
    validate_dates(date_from, date_to)
    validate_country(country)
    

def get_transactions(request):
    account_id = request.GET.get('account_id')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    country = request.GET.get('country')
    
    try:
        validate_transaction_variables(account_id, date_from, date_to, country)

        query_params = {}
        
        if date_from:
            query_params.update({'date_from': date_from})
        if date_to:
            query_params.update({'date_to': date_to})

        if country:
            query_params.update({'country': country})
            task = fetch_premium_transactions.delay(account_id, query_params, request.session['token']['access'])
        else:
            task = fetch_transactions.delay(account_id, query_params, request.session['token']['access'])
    except ValidationError as e:
        return JsonResponse({'error': e.message})
    except Exception as ex:
        return JsonResponse({'error': 'Something went wrong'})

    return JsonResponse({'finish': task.get()})


def get_balances(request) -> JsonResponse:
    account_id = request.GET.get('account_id')
    validate_account_id(account_id)

    task = fetch_balances.delay(account_id, request.session['token']['access'])
    
    return JsonResponse({'finish': task.get()})


def get_details(request) -> JsonResponse:
    account_id = request.GET.get('account_id')
    validate_account_id(account_id)

    task = fetch_details.delay(account_id, request.session['token']['access'])
    
    return JsonResponse({'finish': task.get()})
