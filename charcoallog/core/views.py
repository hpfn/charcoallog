from django.shortcuts import render
# from django.core.urlresolvers import reverse
# from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# from django.db import IntegrityError, transaction
from django.db.models import Sum
from .models import Extract
from .forms import EditExtractForm, SelectExtractForm


# Create your views here.
@login_required
def home(request):
    return render(request, "principal.html")


@login_required
def titulo(request):
    return render(request, "frameset_pages/titulo.html")


@login_required
def row2(request):
    return render(request, "frameset_pages/row2.html")


@login_required
def rodape(request):
    return render(request, "frameset_pages/rodape.html")


@login_required
def show_data(request):
    user = request.user
    builds = Extract.objects.filter(user_name=user).order_by('date')
    total = Extract.objects.filter(user_name=user).aggregate(Sum('money'))

    if request.method == 'POST':
        form = EditExtractForm(request.POST)

        if form.is_valid():
            Extract.objects.insert_by_post(form)

        builds = Extract.objects.filter(user_name=user).order_by('date')
        total = Extract.objects.filter(user_name=user).aggregate(Sum('money'))

    elif request.method == 'GET':
        get_form = SelectExtractForm(request.GET)

        if get_form.is_valid():
            builds, total = Extract.objects.search_from_get(get_form)

    template_name = 'frameset_pages/linha3.html'
    context = {
        'builds': builds,
        'total': total,
    }

    return render(request, template_name, context)


@login_required
def show_choice_data(request):
    get_form = SelectExtractForm()

    template_name = "frameset_pages/form2.html"
    context = {
        'get_form': get_form,
    }

    return render(request, template_name, context)


@login_required
def insert_data_form(request):
    form = EditExtractForm()

    template_name = "frameset_pages/form1.html"
    context = {
        'form': form,
    }

    return render(request, template_name, context)


def show_total(request):
    user = request.user

    payment_iterator = Extract.objects.filter(user_name=user).values_list('payment').iterator()
    payment_list = set([i for i in payment_iterator])

    total_account = [Extract.objects.filter(user_name=user, payment=conta[0]).aggregate(Sum('money'))
                     for conta in payment_list]

    saldo = 0.0
    for resto in total_account:
        saldo += float(resto['money__sum'])

    template_name = 'frameset_pages/linha1.html'
    context = {
        'payment_list': payment_list,
        'total_account': total_account,
        'saldo': saldo
    }
    return render(request, template_name, context)
