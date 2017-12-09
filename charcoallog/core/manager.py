from django.contrib import messages
from .models import Extract


def search_from_get(request_get, form):
    column = form.cleaned_data.get('column')
    from_date = form.cleaned_data.get('from_date')
    to_date = form.cleaned_data.get('to_date')

    if column.lower() == 'all':
        bills = Extract.objects.user_logged(request_get.user).date_range(
            from_date, to_date)
    else:
        bills = Extract.objects.user_logged(request_get.user).date_range(
            from_date, to_date).which_field(column)

    if bills.exists():
        return bills

    messages.error(request_get,
                   "' %s ' is an Invalid search or wrong date!" % column)


def insert_by_post(form):
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
