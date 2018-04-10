from django.db import models


class BasicData(models.Model):
    date = models.DateField()
    money = models.DecimalField(max_digits=8, decimal_places=2)
    # Acao, Titulo Publico, CDB, FII
    kind = models.CharField(max_length=20)
    # Qual acao, titulo publico, banco(CDB), cod FII
    which_target = models.CharField(max_length=20)

class InvestmentDetails(BasicData):
    # PN|ON, NTNB|SELIC|LTF, carencia CDB, sobre FII
    segment = models.CharField(max_length=10)
    # VALOR cada acao, taxa Tesouro, taxa CDB, valor de compra|venda FII
    tx_or_price = models.DecimalField(max_digits=8, decimal_places=2)
    quant = models.DecimalField(max_digits=8, decimal_places=2)


class Investment(BasicData):
    tx_op = models.DecimalField(max_digits=4, decimal_places=2)
    brokerage = models.CharField(max_length=15)

    def save(self, **kwargs):
        super(Investment, self).save(**kwargs)

        data = {
            'date': self.date,
            'money': self.money,
            'kind': self.kind,
            'which_target': self.which_target,
            'segment': '---',
            'tx_or_price': 00.00,
            'quant': 00.00
        }
        InvestmentDetails.objects.create(**data)






