from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from charcoallog.bank.forms import EditExtractForm
from charcoallog.bank.brief_bank_service import BriefBank
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
@require_POST
def update(request):
    data = {'no_account': True,
            'message': 'Form is not valid'}

    query_user = Extract.objects.user_logged(request.user)
    form = EditExtractForm(request.POST)
    if form.is_valid() and request.is_ajax():
        # return?
        data = new_account(form, query_user)

        if not data:
            id_for_update, form = prepare_action(form)
            obj = query_user.get(id=id_for_update)
            new_form = EditExtractForm(form.cleaned_data, instance=obj)
            # if new_form.is_valid():
            new_form.save(request.user)

            data = build_json_data(query_user)

    return JsonResponse(data)


def prepare_action(form):
    id_for_update = form.cleaned_data.get('pk')
    del form.cleaned_data['pk']
    # form.cleaned_data['user_name'] = request_user

    return id_for_update, form


@login_required
@require_POST
def delete(request):
    query_user = Extract.objects.user_logged(request.user)
    form = EditExtractForm(request.POST)
    if form.is_valid() and request.is_ajax():
        pk, form = prepare_action(form)
        query_user.filter(pk=pk).delete()

    data = build_json_data(query_user)

    return JsonResponse(data)


def build_json_data(query_user):
    line1 = BriefBank(query_user)
    return {'accounts': line1.account_names(),
            'whats_left': line1.whats_left()}


def new_account(form, query_user):
    payment = form.cleaned_data.get('payment')
    if not query_user.filter(payment=payment).first():
        return {'no_account': True,
                'message': 'You can not set a new account name from here'}
