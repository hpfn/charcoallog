from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
# from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from .models import Extract
from .forms import EditExtractForm, SelectExtractForm


# Create your views here.
@login_required
def home(request):
    return render(request, "principal.html")


@login_required
def titulo(request):
    return render(request, "frameset_pages/titulo.html")


@login_required
def row2(request):
    return render(request, "frameset_pages/row2.html")


@login_required
def coluna1(request):
    return render(request, "frameset_pages/coluna1.html")


@login_required
def form1(request):
    return render(request, "frameset_pages/form1.html")


@login_required
def form2(request):
    return render(request, "frameset_pages/form2.html")


@login_required
def rodape(request):
    return render(request, "frameset_pages/rodape.html")


@login_required
def show_data(request):
    user = request.user
    builds = Extract.objects.filter(user_name=user).order_by('date')

    if request.method == 'POST':
        form = EditExtractForm(request.POST)

        if form.is_valid():
            newdata = []
            user_name = form.cleaned_data.get('user_name')
            date = form.cleaned_data.get('date')
            money = form.cleaned_data.get('money')
            description = form.cleaned_data.get('description')
            category = form.cleaned_data.get('category')
            payment = form.cleaned_data.get('payment')
            # if all vars
            newdata.append(Extract(user_name=user_name, date=date,
                                   money=money, description=description, category=category,
                                   payment=payment))

            try:
                with transaction.atomic():
                    Extract.objects.bulk_create(newdata)
                    # notify user is ok ? messages()
            except IntegrityError:
                # messages()
                print("An error happened")
                return redirect(reverse('Extract-settings'))

        # return redirect('core:home')
        builds = Extract.objects.filter(user_name=user).order_by('date')

    elif request.method == 'GET':
        get_form = SelectExtractForm(request.GET)

        if get_form.is_valid():
            user_name = get_form.cleaned_data.get('user_name')
            columm = get_form.cleaned_data.get('columm')

            builds = Extract.objects.filter(user_name=user_name,
                                            payment=columm).order_by('date')

            if not builds:
                builds = Extract.objects.filter(user_name=user_name,
                                                category=columm).order_by('date')

            if not builds:
                builds = Extract.objects.filter(user_name=user_name,
                                                description=columm).order_by('date')

    template_name = 'frameset_pages/linha3.html'
    context = {
        'builds': builds,
    }

    return render(request, template_name, context)


@login_required
def show_choice_data(request):
    get_form = SelectExtractForm()

    template_name = "frameset_pages/form2.html"
    context = {
        'get_form': get_form,
    }

    return render(request, template_name, context)


@login_required
def insert_data_form(request):
    form = EditExtractForm()

    template_name = "frameset_pages/form1.html"
    context = {
        'form': form,
    }

    return render(request, template_name, context)
