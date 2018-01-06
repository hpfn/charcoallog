from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
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
def home2(request):
    object_list = Extract.objects.all()
    context = {'object_list': object_list}
    return render(request, "home2.html", context)


@login_required
@require_POST
def ajax_post(request):
    data = dict()
    form = EditExtractForm(request.POST)
    if form.is_valid() and request.is_ajax():
        payment = form.cleaned_data.get('payment')
        query_user = Extract.objects.user_logged(request.user)

        if not query_user.filter(payment=payment).first():
            data = {'no_account': True,
                    'message': 'You can not set a new account name from here'}
        else:
            what_to_do = form.cleaned_data.get('update_rm')
            id_for_update = form.cleaned_data.get('pk')
            del form.cleaned_data['update_rm']
            del form.cleaned_data['pk']
            form.cleaned_data['user_name'] = request.user

            if what_to_do == 'remove':
                query_user.filter(**form.cleaned_data).delete()
            elif what_to_do == 'update':
                # , user_name=self.request_user)
                obj = query_user.get(id=id_for_update)
                obj.date = form.cleaned_data['date']
                obj.money = form.cleaned_data['money']
                obj.description = form.cleaned_data['description']
                obj.category = form.cleaned_data['category']
                obj.payment = form.cleaned_data['payment']
                obj.save(update_fields=['date', 'money',
                                        'description', 'category', 'payment'])

            line1 = Line1(query_user)
            data = {'accounts': line1.account_names(),
                    'whats_left': line1.whats_left()}

    return JsonResponse(data)


def money_edit(request, pk):
    obj = Extract.objects.get(pk=pk)
    obj.date = request.POST.get('date')
    obj.money = request.POST.get('money')
    obj.description = request.POST.get('description')
    obj.category = request.POST.get('category')
    obj.payment = request.POST.get('payment')
    obj.save()
    response = {'status': 'updated'}
    return JsonResponse(response)


def money_delete(request, pk):
    obj = Extract.objects.get(pk=pk)
    obj.delete()
    response = {'status': 'deleted'}
    return JsonResponse(response)
