from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from charcoallog.core.models import Extract
from charcoallog.core.forms import EditExtractForm

# Create your views here.
@login_required
def home(request):
    user = request.user
    builds = Extract.objects.filter(user_name=user).order_by('date')
    if request.method == 'POST':
        form = EditExtractForm(request.POST)
        if form.is_valid():
            NewData = []
            user_name = form.cleaned_data.get('user_name')
            date = form.cleaned_data.get('date')
            money = form.cleaned_data.get('money')
            description = form.cleaned_data.get('description')
            category = form.cleaned_data.get('category')
            payment = form.cleaned_data.get('payment')
            # if all vars
            NewData.append(Extract(user_name=user_name, date=date,
            money=money, description=description, category=category,
            payment=payment))

            try:
                with transaction.atomic():
                    Extract.objects.bulk_create(NewData)
                    # notify user is ok ? messages()
            except IntegrityError:
                # messages()
                print("An error happened")
                return redirect(reverse('Extract-settings'))

            return redirect('core:home')
    else:
        form = EditExtractForm()

    template_name = 'home.html'
    context = {
            'builds': builds,
            'form' : form,
    }

    return render(request, template_name, context)

