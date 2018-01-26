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
        'show_data': ShowData(request.method, request.GET, request.POST, request.user),
    }
    return render(request, "bank/home.html", context)


@login_required
@require_POST
def ajax_post(request):
    data = dict()
    form = EditExtractForm(request.POST)
    if form.is_valid() and request.is_ajax():
        query_user = Extract.objects.user_logged(request.user)
        what_to_do, id_for_update, form = prepare_action(form, request.user)

        if what_to_do == 'remove':
            query_user.filter(**form.cleaned_data).delete()
        elif what_to_do == 'update':
            data = update_data(query_user, id_for_update, form)

        if not data:
            line1 = BriefBank(query_user)
            data = {'accounts': line1.account_names(),
                    'whats_left': line1.whats_left()}

    return JsonResponse(data)


def update_data(query_user, id_for_update, form):
    payment = form.cleaned_data.get('payment')
    if not query_user.filter(payment=payment).first():
        return {'no_account': True,
                'message': 'You can not set a new account name from here'}
    else:
        obj = query_user.get(id=id_for_update)  # , user_name=self.request_user)
        obj.date = form.cleaned_data.get('date')
        obj.money = form.cleaned_data.get('money')
        obj.description = form.cleaned_data.get('description')
        obj.category = form.cleaned_data.get('category')
        obj.payment = form.cleaned_data.get('payment')
        obj.save(update_fields=['date', 'money', 'description', 'category', 'payment'])


def prepare_action(form, request_user):
    what_to_do = form.cleaned_data.get('update_rm')
    id_for_update = form.cleaned_data.get('pk')
    del form.cleaned_data['update_rm']
    del form.cleaned_data['pk']
    form.cleaned_data['user_name'] = request_user

    return what_to_do, id_for_update, form
