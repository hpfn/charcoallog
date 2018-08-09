from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from charcoallog.investments.forms import BasicDataForm, InvestmentForm
from charcoallog.investments.models import InvestmentDetails
from charcoallog.investments.service import ShowData


@login_required
def home(request):
    context = {
        'basic_data': BasicDataForm(),
        'form': InvestmentForm(),
        'show_data': ShowData(request)}
    return render(request, 'investments/home.html', context)


@login_required
def detail(request, kind):
    qs = InvestmentDetails.objects.select_related(
        'basic_data').user_logged(request.user).filter(
        basic_data__kind=kind)

    context = {
        'd': qs
    }
    return render(request, 'investments/detail.html', context)
