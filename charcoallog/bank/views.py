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


# @login_required
# @require_POST
# def ajax_post(request):
#    return JsonResponse(update_data(request))

@login_required
# @require_POST
def update(request):
    data = {}
    query_user = Extract.objects.user_logged(request.user)
    body = request.body.decode('utf-8')
    form_data = json.loads(body)

    if request.is_ajax() and request.method == 'PUT':
        # payment = form_data.get('payment')
        data = new_account(form_data, query_user)

        if not data:
            form = EditExtractForm(form_data)
            # what is not on forms.py '.is_valid()' remove - update field in .html file
            if form.is_valid():
                update_data(form, form_data, query_user, request.user)
                # id_for_update = form_data['pk']
                # del form_data['pk']
                # obj = query_user.get(id=id_for_update)
                # new_form = EditExtractForm(form.cleaned_data, instance=obj)
                # new_form.save(request.user)
                data = build_json_data(query_user)
            else:
                data = {"js_alert": True, "message": 'Form is not valid'}

    return JsonResponse(data)


# def prepare_action(form):
#     id_for_update = form.cleaned_data.get('pk')
#     del form.cleaned_data['pk']
#     # form.cleaned_data['user_name'] = request_user
#
#     return id_for_update, form


@login_required
# @require_POST
def delete(request):
    query_user = Extract.objects.user_logged(request.user)
    # form = EditExtractForm(request.POST)
    if request.is_ajax() and request.method == 'DELETE':
        body = request.body.decode('utf-8')
        form_data = json.loads(body)
        pk = form_data['pk']
        query_user.filter(pk=pk).delete()

    data = build_json_data(query_user)

    return JsonResponse(data)


def build_json_data(query_user):
    line1 = BriefBank(query_user)
    return {"accounts": line1.account_names(),
            "whats_left": line1.whats_left()}


def new_account(form_data, query_user):
    # payment = form.cleaned_data.get('payment')
    payment = form_data.get('payment')
    if not query_user.filter(payment=payment).first():
        return {"js_alert": True,
                "message": 'You can not set a new account name from here'}


def update_data(form, form_data, query_user, request_user):
    id_for_update = form_data['pk']
    del form_data['pk']
    obj = query_user.get(id=id_for_update)
    new_form = EditExtractForm(form.cleaned_data, instance=obj)
    new_form.save(request_user)
