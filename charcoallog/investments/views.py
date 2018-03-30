from django.shortcuts import render
from charcoallog.investments.forms import InvestmentForm


def home(request):
    context = {'form': InvestmentForm()}
    return render(request, 'investments/home.html', context)