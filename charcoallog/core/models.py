from django.shortcuts import redirect
from django.db import models
from django.db.models import Sum
from django.db import IntegrityError, transaction
from django.core.urlresolvers import reverse


# from django.utils import timezone
# import Q ?

class ExtractManager(models.Manager):
    def search_from_get(self, form):
        user_name = form.cleaned_data.get('user_name')
        columm = form.cleaned_data.get('columm')
        from_date = form.cleaned_data.get('from_date')
        to_date = form.cleaned_data.get('to_date')

        if columm.lower() == 'all':
            builds = self.filter(user_name=user_name).filter(
                date__gte=from_date,
                date__lte=to_date).order_by('date')
            total = self.filter(user_name=user_name).filter(
                date__gte=from_date,
                date__lte=to_date).aggregate(Sum('money'))
        else:
            builds = self.filter(user_name=user_name, payment=columm).filter(
                date__gte=from_date, date__lte=to_date).order_by('date')
            total = self.filter(user_name=user_name,
                                payment=columm).filter(
                date__gte=from_date,
                date__lte=to_date).aggregate(Sum('money'))

            if not builds:
                builds = self.filter(user_name=user_name,
                                     category=columm).filter(
                    date__gte=from_date,
                    date__lte=to_date).order_by('date')
                total = self.filter(user_name=user_name,
                                    category=columm).filter(
                    date__gte=from_date,
                    date__lte=to_date).aggregate(Sum('money'))

            if not builds:
                builds = self.filter(user_name=user_name,
                                     description=columm).filter(
                    date__gte=from_date,
                    date__lte=to_date).order_by('date')
                total = self.filter(user_name=user_name,
                                    description=columm).filter(
                    date__gte=from_date,
                    date__lte=to_date).aggregate(Sum('money'))

        return builds, total

    def insert_by_post(self, form):
        newdata = []
        user_name = form.cleaned_data.get('user_name')
        date = form.cleaned_data.get('date')
        money = form.cleaned_data.get('money')
        description = form.cleaned_data.get('description')
        category = form.cleaned_data.get('category')
        payment = form.cleaned_data.get('payment')
        remove = form.cleaned_data.get('remove')
        # if all vars, but no remove.
        newdata.append(Extract(user_name=user_name, date=date, money=money,
                               description=description, category=category,
                               payment=payment))

        try:
            with transaction.atomic():
                if remove:
                    self.filter(user_name=user_name, date=date,
                                money=money, description=description,
                                category=category, payment=payment).delete()
                else:
                    self.bulk_create(newdata)
                    # notify user is ok ? messages()
        except IntegrityError:
            # messages()
            print("An error happened")
            return redirect(reverse('Extract-settings'))

    def delete(self, query):
        return self.filter(query).delete()


class Extract(models.Model):
    user_name = models.CharField('Name', max_length=30)
    date = models.DateField('Date')
    money = models.FloatField('Money', default=00.00, null=False, blank=False)
    description = models.CharField('Description', max_length=70)
    category = models.CharField('Category', max_length=70)
    payment = models.CharField('Payment', max_length=70)

    objects = ExtractManager()

    class Meta:
        ordering = ['date']
