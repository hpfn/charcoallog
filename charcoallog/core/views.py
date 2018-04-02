from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from charcoallog.core.service import BuildHome


@login_required
def home(request):
    context = {'build_home': BuildHome(request.user)}
    return render(request, "home.html", context)
