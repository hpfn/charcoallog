from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from charcoallog.core.forms import EditExtractForm
from charcoallog.core.line1_service import Line1
from charcoallog.core.models import Extract
from .service import ShowData


@login_required
def home(request):
    context = {
        'show_data': ShowData(request.method, request.GET, request.POST, request.user),
    }
    return render(request, "home.html", context)


@login_required
@require_POST
def ajax_post(request):
    form = EditExtractForm(request.POST)
    if form.is_valid():
        what_to_do = form.cleaned_data.get('update_rm')
        del form.cleaned_data['update_rm']
        id_for_update = form.cleaned_data.get('pk')
        del form.cleaned_data['pk']

        form.cleaned_data['user_name'] = request.user

        payment = form.cleaned_data.get('payment')
        payment_confirm = Extract.objects.user_logged(request.user).filter(
            payment=payment).first()

        if not payment_confirm:
            print('not payment_confirm')
            # messages.error(request, "You can not fill account entry with
            #                          a new account name from here")
            return redirect('core:home')

        if what_to_do == 'remove':
            Extract.objects.user_logged(request.user).filter(**form.cleaned_data).delete()
        elif what_to_do == 'update':
            obj = Extract.objects.user_logged(request.user).get(id=id_for_update)  # , user_name=self.request_user)
            obj.date = form.cleaned_data['date']
            obj.money = form.cleaned_data['money']
            obj.description = form.cleaned_data['description']
            obj.category = form.cleaned_data['category']
            obj.payment = form.cleaned_data['payment']
            obj.save(update_fields=['date', 'money', 'description', 'category', 'payment'])

    line1 = Line1(Extract.objects.user_logged(request.user))
    data = {'accounts': line1.account_names(),
            'whats_left': line1.whats_left()}

    return JsonResponse(data)
