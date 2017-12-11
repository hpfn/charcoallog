from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .service import ShowData


@login_required
def home(request):
    context = {
        'show_data': ShowData(request),
    }
    return render(request, "home.html", context)
