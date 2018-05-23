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


@login_required
@require_POST
def ajax_post(request):
    return JsonResponse(update_data(request))


def update_data(request):
    data = {'no_account': True,
            'message': 'Form is not valid'}

    # query_user = Extract.objects.user_logged(request.user)

    form = EditExtractForm(request.POST)
    if form.is_valid() and request.is_ajax():
        query_user = Extract.objects.user_logged(request.user)
        payment = form.cleaned_data.get('payment')
        if not query_user.filter(payment=payment).first():
            data = {'no_account': True,
                    'message': 'You can not set a new account name from here'}
        else:
            id_for_update, form = prepare_action(form, request.user)
            obj = query_user.get(id=id_for_update)  # , user_name=self.request_user)
            new_form = EditExtractForm(form.cleaned_data, instance=obj)
            if new_form.is_valid():
                new_form.save()

            line1 = BriefBank(query_user)
            data = {'accounts': line1.account_names(),
                    'whats_left': line1.whats_left()}

    return data


def prepare_action(form, request_user):
    # what_to_do = form.cleaned_data.get('update_rm')
    id_for_update = form.cleaned_data.get('pk')
    # del form.cleaned_data['update_rm']
    del form.cleaned_data['pk']
    form.cleaned_data['user_name'] = request_user

    return id_for_update, form


def delete(request):
    form = EditExtractForm(request.POST)
    if form.is_valid() and request.is_ajax():
        # this should be removed after new JS -  ajax
        pk, form = prepare_action(form, request.user)

        query_user = Extract.objects.user_logged(request.user)
        # query_user.filter(**form.cleaned_data).delete()
        query_user.filter(pk=pk).delete()

        line1 = BriefBank(query_user)
        data = {'accounts': line1.account_names(),
                'whats_left': line1.whats_left()}
        return JsonResponse(data)
