from django.contrib import messages
from django.db import IntegrityError
from django.db import models
from django.db.models import Q
from django.db.models import Sum
from django.shortcuts import redirect


class ExtractManager(models.Manager):
    def search_from_get(self, request_get, form):
        user_name = request_get.user
        columm = form.cleaned_data.get('columm')
        from_date = form.cleaned_data.get('from_date')
        to_date = form.cleaned_data.get('to_date')

        if columm.lower() == 'all':
            bills = self.filter(user_name=user_name).filter(
                date__gte=from_date, date__lte=to_date)

            total = self.filter(user_name=user_name).filter(
                date__gte=from_date, date__lte=to_date).aggregate(Sum('money'))
        else:
            bills = self.filter(user_name=user_name, date__gte=from_date, date__lte=to_date).filter(
                Q(payment=columm) | Q(category=columm) | Q(description=columm))

            total = self.filter(user_name=user_name, date__gte=from_date, date__lte=to_date).filter(
                Q(payment=columm) | Q(category=columm) | Q(description=columm)).aggregate(Sum('money'))

        if not bills.exists():
            messages.error(request_get, "' %s ' is an Invalid search!" % columm)
            return redirect('core:home'), 0

        return bills, total

    def insert_by_post(self, form):
        try:
            if form.cleaned_data.get('remove'):
                del form.cleaned_data['remove']
                # checked before save. duplicate entry no more
                # self.filter(**form.cleaned_data).order_by('id')[0].delete()
                self.filter(**form.cleaned_data).order_by('id')[0].delete()
            else:
                form.save()
                # notify user is ok ? messages()
        except IntegrityError:
            # messages()
            print("An error happened")
            # return redirect(reverse('Extract-settings'))
        except IndexError:  # checked before save. this will not be printed
            print("Do not Refresh the page!!!")


class Extract(models.Model):
    user_name = models.CharField('Name', max_length=30)
    date = models.DateField('Date')
    money = models.DecimalField('Money', max_digits=12, decimal_places=2, null=False, blank=False)
    description = models.CharField('Description', max_length=70)
    category = models.CharField('Category', max_length=70)
    payment = models.CharField('Payment', max_length=70)

    objects = ExtractManager()

    def save(self, *args, **kwargs):
        if Extract.objects.filter(user_name=self.user_name, date=self.date, money=self.money,
                                  description=self.description, category=self.category,
                                  payment=self.payment).exists():
            return 
        else:
            super(Extract, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date']
