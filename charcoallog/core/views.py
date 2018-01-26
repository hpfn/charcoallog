from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.bank.models import Extract


@login_required
def home(request):
    query_user = Extract.objects.user_logged(request.user)
    context = {'line1': BriefBank(query_user)}
    return render(request, "home.html", context)
