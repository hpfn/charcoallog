from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from charcoallog.bank.line1_service import Line1
from charcoallog.bank.models import Extract


@login_required
def home(request):
    query_user = Extract.objects.user_logged(request.user)
    context = {'line1': Line1(query_user)}
    return render(request, "home.html", context)
