from django.db import models
from django.db.models import Sum, Q


# from .manager import ExtractManager


class ExtractStatementQuerySet(models.QuerySet):
    def user_logged(self, user_name):
        return self.filter(user_name=user_name)

    def date_range(self, from_date, to_date):
        return self.filter(date__gte=from_date, date__lte=to_date)

    def which_field(self, column):
        return self.filter(Q(payment=column) | Q(category=column) |
                           Q(description=column)).filter(~Q(category__startswith='transfer'))

    def total(self):
        return self.aggregate(Sum('money'))


class Extract(models.Model):
    user_name = models.CharField('Name', max_length=30)
    date = models.DateField('Date')
    money = models.DecimalField('Money', max_digits=12, decimal_places=2, null=False, blank=False)
    description = models.CharField('Description', max_length=70)
    category = models.CharField('Category', max_length=70)
    payment = models.CharField('Payment', max_length=70)

    objects = models.Manager.from_queryset(ExtractStatementQuerySet)()

    class Meta:
        ordering = ['-date']


class Schedule(models.Model):
    user_name = models.CharField('Name', max_length=30)
    date = models.DateField('Date')
    money = models.DecimalField('Money', max_digits=12, decimal_places=2, null=False, blank=False)
    description = models.CharField('Description', max_length=70)
    category = models.CharField('Category', max_length=70)
    payment = models.CharField('Payment', max_length=70)

    # objects = models.Manager.from_queryset(ExtractStatementQuerySet)()

    class Meta:
        ordering = ['-date']
