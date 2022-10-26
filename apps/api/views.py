from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from .tasks import fetch_transactions, fetch_balances, fetch_details, fetch_premium_transactions
from .forms import GetTransactionsForm, GetAccountIdForm
from nordigen import NordigenClient
from nordigen_api.settings import USER_SECRET_ID, USER_SECRET_KEY
from uuid import uuid4


client = NordigenClient(
    secret_id=USER_SECRET_ID,
    secret_key=USER_SECRET_KEY
)

generic_error_message = 'Something went wrong'
post_error_message = 'Request method must be "POST"'


def index(request: str):
    try:
        request.session['token'] = client.generate_token()
        institutions = client.institution.get_institutions()
    except Exception:
        return render(request, 'error.html')

    return render(request, 'index.html', {'banks': institutions})


def auth(request: str, institution_id: str):
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

    return redirect(str(link))


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

            accounts_data.append({
                "id": id,
                "metadata": metadata,
                "details": details,
            })
            
    except Exception as e:
        return render(request, 'error.html')

    return render(request, 'account.html', {'accounts': accounts_data})


def format_form_dates(form: GetTransactionsForm):
    date_from = form['date_from']
    date_to = form['date_to']

    if date_from:
        form['date_from'] = str(date_from)

    if date_to:
        form['date_to'] = str(date_to)

    return form

    
def get_transactions(request):
    try: 
        if request.method == 'POST':
            form = GetTransactionsForm(request.POST)

            if form.is_valid():
                form_data = format_form_dates(form.cleaned_data)
                task = get_transactions_task(form_data, request.session['token']['access'])

                return JsonResponse(task.get())
            else:
                error_string = ' '.join([' '.join(message for message in list) for list in list(form.errors.values())])
                
                return JsonResponse({'error': error_string})
        else:
            return JsonResponse({'error': post_error_message}, status = 403)

    except Exception as ex:
        return JsonResponse({'error': generic_error_message}, status = 500)
    

def get_transactions_task(form: GetTransactionsForm, token):
    account_id = form['account_id']
    del form['account_id']

    if form['country']:
        task = fetch_premium_transactions.delay(account_id, form, token)
    else:
        del form['country']
        task = fetch_transactions.delay(account_id, form, token)

    return task


def get_balances(request) -> JsonResponse:
    try:
        if request.method == 'POST':
            form = GetAccountIdForm(request.POST)
            
            if form.is_valid():
                task = fetch_balances.delay(form.cleaned_data['account_id'], request.session['token']['access'])
        
                return JsonResponse(task.get())
            else:
                error_string = ' '.join([' '.join(message for message in list) for list in list(form.errors.values())])
                
                return JsonResponse({'error': error_string})
        else:
            return JsonResponse({'error': post_error_message}, status = 403)

    except Exception as ex:
        return JsonResponse({'error': generic_error_message}, status = 500)


def get_details(request) -> JsonResponse:
    try:
        if request.method == 'POST':
            form = GetAccountIdForm(request.POST)
            
            if form.is_valid():
                task = fetch_details.delay(form.cleaned_data['account_id'], request.session['token']['access'])
        
                return JsonResponse(task.get())
            else:
                error_string = ' '.join([' '.join(message for message in list) for list in list(form.errors.values())])
                
                return JsonResponse({'error': error_string})
        else:
            return JsonResponse({'error': post_error_message}, status = 403)

    except Exception as ex:
        return JsonResponse({'error': generic_error_message}, status = 500)
