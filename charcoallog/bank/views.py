import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.bank.forms import EditExtractForm
from charcoallog.bank.models import Extract

from .service import ShowData


@login_required
def home(request):
    context = {
        'show_data': ShowData(request),
    }
    return render(request, "bank/home.html", context)


@login_required
def update(request):
    data = {"js_alert": True, "message": 'Not a valid request'}
    query_user = Extract.objects.user_logged(request.user)
    # body = request.body.decode('utf-8')
    form_data = form_data_from_body(request.body)

    if request.is_ajax() and request.method == 'PUT':
        # data = new_account(form_data, query_user)

        # if not data:
        form = EditExtractForm(form_data)
        # what is not on forms.py '.is_valid()' remove
        # - the update and pk fields in .html file
        if form.is_valid():
            update_db(form_data['pk'], form.cleaned_data, query_user, request.user)
            data = build_json_data(query_user)
        else:
            data = {"js_alert": True, "message": 'Form is not valid'}

    return JsonResponse(data)


@login_required
def delete(request):
    query_user = Extract.objects.user_logged(request.user)
    if request.is_ajax() and request.method == 'DELETE':
        # body = request.body.decode('utf-8')
        form_data = form_data_from_body(request.body)
        pk = form_data['pk']
        query_user.filter(pk=pk).delete()

    data = build_json_data(query_user)

    return JsonResponse(data)


# helpers for update and delete views
def form_data_from_body(request_body):
    body = request_body.decode('utf-8')
    return json.loads(body)


def build_json_data(query_user):
    line1 = BriefBank(query_user)
    return {"accounts": line1.account_names(),
            "whats_left": line1.whats_left()}


def new_account(form_data, query_user):
    payment = form_data.get('payment')
    if not query_user.filter(payment=payment).first():
        return {"js_alert": True,
                "message": 'You can not set a new account name from here'}


def update_db(pk, form_cleaned_data, query_user, request_user):
    obj = query_user.get(id=pk)
    new_form = EditExtractForm(form_cleaned_data, instance=obj)
    new_form.save(request_user)
