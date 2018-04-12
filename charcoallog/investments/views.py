from django.shortcuts import render
from charcoallog.investments.forms import InvestmentForm
from charcoallog.investments.service import ShowData


def home(request):
    context = {
        'form': InvestmentForm(),
        'show_data': ShowData(request)}
    return render(request, 'investments/home.html', context)
