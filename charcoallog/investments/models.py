from django.db import models
from django.db.models import Sum


class InvestmentStatementQuerySet(models.QuerySet):
    def user_logged(self, user_name):
        return self.filter(basic_data__user_name=user_name)

    # def date_range(self, from_date, to_date):
    #     return self.filter(date__gte=from_date, date__lte=to_date)
    #
    # def which_field(self, column):
    #     return self.filter(Q(payment=column) | Q(category=column) |
    #                        Q(description=column)).filter(~Q(category__startswith='transfer'))

    def total(self):
        return self.aggregate(Sum('basic_data__money'))


class BasicData(models.Model):
    user_name = models.CharField(max_length=30)
    date = models.DateField()
    money = models.DecimalField(max_digits=8, decimal_places=2)
    # Acao, Titulo Publico, CDB, FII
    kind = models.CharField(max_length=20)
    # Qual acao, titulo publico, banco(CDB), cod FII
    which_target = models.CharField(max_length=20)


class InvestmentDetails(models.Model):
    # PN|ON, NTNB|SELIC|LTF, carencia CDB, sobre FII
    segment = models.CharField(max_length=10)
    # VALOR cada acao, taxa Tesouro, taxa CDB, valor de compra|venda FII
    tx_or_price = models.DecimalField(max_digits=8, decimal_places=2)
    quant = models.DecimalField(max_digits=8, decimal_places=2)
    basic_data = models.OneToOneField(
        BasicData,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    objects = models.Manager.from_queryset(InvestmentStatementQuerySet)()


class Investment(models.Model):
    tx_op = models.DecimalField(max_digits=4, decimal_places=2)
    brokerage = models.CharField(max_length=15)
    basic_data = models.OneToOneField(
        BasicData,
        on_delete=models.CASCADE,
        primary_key=True,
        # default=0
        # null=True
    )

    objects = models.Manager.from_queryset(InvestmentStatementQuerySet)()

    # def save(self, *args, **kwargs):
    #     super(Investment, self).save(*args, **kwargs)
    #
    #     data = {
    #         'user_name': self.user_name,
    #         'date': self.date,
    #         'money': self.money,
    #         'kind': self.kind,
    #         'which_target': self.which_target,
    #         'segment': '---',
    #         'tx_or_price': 00.00,
    #         'quant': 00.00
    #     }
    #
    #     InvestmentDetails.objects.create(**data)
