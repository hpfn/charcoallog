from datetime import date
from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from .forms import EditExtractForm, SelectExtractForm
from .models import Extract


@login_required
def home(request):
    bills, total = show_data(request)
    form = EditExtractForm()
    get_form = SelectExtractForm()
    # payment_list, total_account, saldo = show_total(request)
    total_account, saldo = show_total(request)

    context = {
        'bills': bills,
        'total': total,
        'form': form,
        'get_form': get_form,
        # 'payment_list': payment_list,
        'total_account': total_account,
        'saldo': saldo,
    }
    return render(request, "home.html", context)


@login_required
def show_data(request):
    user = request.user

    d = date.today()
    d = d.strftime('%Y-%m-01')

    if request.method == 'POST':
        form = EditExtractForm(request.POST)

        if form.is_valid():
            form.cleaned_data['user_name'] = user
            Extract.objects.insert_by_post(form)
    elif request.method == 'GET':
        get_form = SelectExtractForm(request.GET)

        if get_form.is_valid():
            return Extract.objects.search_from_get(request, get_form)

    bills = Extract.objects.filter(user_name=user).filter(date__gte=d)
    total = Extract.objects.filter(user_name=user).filter(date__gte=d).aggregate(Sum('money'))

    return bills, total


@login_required
def show_total(request):
    user = request.user

    payment_iterator = set(Extract.objects.filter(user_name=user).values_list(
        'payment'))
    payment_list = [i[0] for i in payment_iterator]

    #total_account = [Extract.objects.filter(
    #    user_name=user, payment=conta).aggregate(Sum('money'))
    #                 for conta in payment_list]

    total_account = dict()
    for conta in payment_list:
        total_account[conta] = Extract.objects.filter(
            user_name=user, payment=conta).aggregate(Sum('money'))


    saldo = 0
    for resto in total_account.values():
        saldo += resto['money__sum']

    # return payment_list, total_account, saldo
    return OrderedDict(sorted(total_account.items())), saldo
