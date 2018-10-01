from django.db import models
from django.db.models import Sum


class InvestmentStatementQuerySet(models.QuerySet):
    def user_logged(self, user_name):
        return self.filter(user_name=user_name)

    # def date_range(self, from_date, to_date):
    #     return self.filter(date__gte=from_date, date__lte=to_date)
    #
    # def which_field(self, column):
    #     return self.filter(Q(payment=column) | Q(category=column) |
    #                        Q(description=column)).filter(~Q(category__startswith='transfer'))

    def total_money(self):
        return self.aggregate(Sum('money'))['money__sum']

    def brokerage(self):
        return self.values_list('brokerage')

    def kind(self):
        return self.values_list('kind')


class NewBasicData(models.Model):
    user_name = models.CharField(max_length=30)
    date = models.DateField()
    money = models.DecimalField(max_digits=8, decimal_places=2)
    # Acao, Titulo Publico, CDB, FII
    kind = models.CharField(max_length=35)

    # both a custom Manager and a custom QuerySet
    # https://docs.djangoproject.com/en/1.11/topics/db/managers/#from-queryset
    # objects = models.Manager.from_queryset(InvestmentStatementQuerySet)()
    #
    # to create an instance of Manager with a copy of a custom QuerySet’s
    # https://docs.djangoproject.com/en/1.11/topics/
    # db/managers/#creating-a-manager-with-queryset-methods
    objects = InvestmentStatementQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ['-date']


class NewInvestmentDetails(NewBasicData):
    # Qual acao, titulo publico, banco(CDB), cod FII
    which_target = models.CharField(max_length=20, default='---')
    # PN|ON, NTNB|SELIC|LTF, carencia CDB, sobre FII
    segment = models.CharField(max_length=20)
    # VALOR cada acao, taxa Tesouro, taxa CDB, valor de compra|venda FII
    tx_or_price = models.DecimalField(max_digits=8, decimal_places=2)
    quant = models.DecimalField(max_digits=8, decimal_places=2)


class NewInvestment(NewBasicData):
    # corretagem
    tx_op = models.DecimalField(max_digits=4, decimal_places=2)
    brokerage = models.CharField(max_length=15)
