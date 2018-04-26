from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from charcoallog.investments.forms import InvestmentForm
from charcoallog.investments.models import InvestmentDetails
from charcoallog.investments.service import ShowData


@login_required
def home(request):
    context = {
        'form': InvestmentForm(),
        'show_data': ShowData(request)}
    return render(request, 'investments/home.html', context)


@login_required
def detail(request, kind):

    context = {
        'd': InvestmentDetails.objects.user_logged(request.user).filter(kind=kind),
    }
    return render(request, 'investments/detail.html', context)
