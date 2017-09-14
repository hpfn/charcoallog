from django.contrib import messages
from django.db import IntegrityError
from django.db import models
from django.db.models import Q
from django.db.models import Sum
from django.shortcuts import redirect


class ExtractManager(models.Manager):
    def search_from_get(self, request_get, form):
        user_name = request_get.user
        column = form.cleaned_data.get('column')
        from_date = form.cleaned_data.get('from_date')
        to_date = form.cleaned_data.get('to_date')

        if column.lower() == 'all':
            bills = self.filter(user_name=user_name).filter(
                date__gte=from_date, date__lte=to_date)

            total = self.filter(user_name=user_name).filter(
                date__gte=from_date, date__lte=to_date).aggregate(Sum('money'))
        else:
            bills = self.filter(user_name=user_name, date__gte=from_date, date__lte=to_date).filter(
                Q(payment=column) | Q(category=column) | Q(description=column))

            total = self.filter(user_name=user_name, date__gte=from_date, date__lte=to_date).filter(
                Q(payment=column) | Q(category=column) | Q(description=column)).aggregate(Sum('money'))

        if not bills.exists():
            messages.error(request_get, "' %s ' is an Invalid search!" % column)
            return redirect('core:home'), 0

        return bills, total

    def insert_by_post(self, form):
        try:
            what_to_do = form.cleaned_data.get('update_rm')
            del form.cleaned_data['update_rm']
            id_for_update = form.cleaned_data.get('pk')
            del form.cleaned_data['pk']

            if what_to_do == 'remove':
                self.filter(**form.cleaned_data).delete()
            elif what_to_do == 'update':
                obj = self.get(id=id_for_update, user_name=form.cleaned_data['user_name'])
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
