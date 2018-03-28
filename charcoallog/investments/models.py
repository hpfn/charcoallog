from django.db import models


class BrokerFirm(models.Model):
    pass
#     brokerage = models.CharField(max_length=30)
#
#
class KindOfInvest(models.Model):
    pass
#     # Nome Acao, Titulo Publico, CDB, FII
#     kind = models.CharField(max_length=20)
#     # Qual acao, tesouro, banco(CDB), cod FII
#     which_target = models.CharField(max_length=20)
#     # PN|ON, NTNB|SELIC|LTF, carencia CDB, QUANT FII
#     segment = models.CharField(max_length=10)
#     # VALOR cada acao, taxa Tesouro, taxa CDB, valor de compra|venda FII
#     tx_or_price = models.DecimalField(max_digits=8, decimal_places=2)
#     quant = models.DecimalField(max_digits=8, decimal_places=2)


class InvestmentDetails(models.Model):
    pass
#    brokerage_name = models.ForeignKey(BrokerFirm, on_delete=models.CASCADE)
#    #id = models.AutoField(auto_created=True, primary_key=True)
#    date = models.DateField()
#    # money invested
#    money = models.DecimalField(max_digits=8, decimal_places=2)
#    kind_of_investment = models.ManyToManyField(KindOfInvest)
#    #brokerage_name = models.CharField(max_length=20)


