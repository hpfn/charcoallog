from collections import OrderedDict
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import EditExtractForm, SelectExtractForm
from .manager import insert_by_post, search_from_get
from .models import Extract


@login_required
def home(request):
    bills = show_data(request)
    total_account, saldo = show_total(request)

    context = {
        'bills': bills,
        'total': bills.total(),
        'form': EditExtractForm(),
        'get_form': SelectExtractForm(),
        'total_account': total_account,
        'saldo': saldo,
    }
    return render(request, "home.html", context)


@login_required
def show_data(request):
    d = date.today().strftime('%Y-%m-01')
    bills = 0

    if request.method == 'POST':
        form = EditExtractForm(request.POST)

        if form.is_valid():
            form.cleaned_data['user_name'] = request.user
            insert_by_post(form)

    elif request.method == 'GET':
        get_form = SelectExtractForm(request.GET)

        if get_form.is_valid():
            bills = search_from_get(request, get_form)

    return bills or Extract.objects.user_logged(request.user).filter(date__gte=d)


@login_required
def show_total(request):
    payment_iterator = set(Extract.objects.user_logged(request.user).values_list(
        'payment'))
    # payment_list = [i[0] for i in payment_iterator]

    total_account = dict()
    for set_value in payment_iterator:
        conta = set_value[0]
        total_account[conta] = Extract.objects.user_logged(request.user).filter(
            payment=conta).total()

    saldo = sum([resto['money__sum']for resto in total_account.values()])

    return OrderedDict(sorted(total_account.items())), saldo
