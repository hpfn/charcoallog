from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
from .models import Extract


def search_from_get(request_get, form):
    user_name = request_get.user
    column = form.cleaned_data.get('column')
    from_date = form.cleaned_data.get('from_date')
    to_date = form.cleaned_data.get('to_date')

    if column.lower() == 'all':
        bills = Extract.objects.user_logged(user_name).date_range(
            from_date, to_date)
    else:
        bills = Extract.objects.user_logged(user_name).date_range(
            from_date, to_date).which_field(column)

    if not bills.exists():
        messages.error(request_get, "' %s ' is an Invalid search!" % column)
        return redirect('core:home'), 0

    return bills  # , bills.total()


def insert_by_post(form):
    try:
        what_to_do = form.cleaned_data.get('update_rm')
        del form.cleaned_data['update_rm']
        id_for_update = form.cleaned_data.get('pk')
        del form.cleaned_data['pk']

        if what_to_do == 'remove':
            Extract.objects.filter(**form.cleaned_data).delete()
        elif what_to_do == 'update':
            obj = Extract.objects.get(id=id_for_update, user_name=form.cleaned_data['user_name'])
            obj.date = form.cleaned_data['date']
            obj.money = form.cleaned_data['money']
            obj.description = form.cleaned_data['description']
            obj.category = form.cleaned_data['category']
            obj.payment = form.cleaned_data['payment']
            obj.save(update_fields=['date', 'money', 'description', 'category', 'payment'])
        else:
            form.save()
            # notify user is ok ? messages()
    except IntegrityError:
        # messages()
        print("An error happened")
        # return redirect(reverse('Extract-settings'))
    except IndexError:  # checked before save. this will not be printed
        print("Do not Refresh the page!!!")
