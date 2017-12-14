from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

from .forms import RegisterForm


def register(request):
    template_name = 'accounts/register.html'

    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
    else:
        # form = UserCreationForm()
        form = RegisterForm()

    context = {
        'form': form
    }

    return render(request, template_name, context)
