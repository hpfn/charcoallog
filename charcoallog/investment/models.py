# from django.db import models
#
#
# class BrokerFirm(models.Model):
#     brokerage = models.CharField(max_length=30)
#
#
# class KindOfInvest(models.Model):
#     # Nome Acao, Tesouro, CDB, FII
#     kind = models.CharField(max_length=20)
#     # Qual acao, tesouro, banco(CDB), cod FII
#     which_target = models.CharField(max_length=20)
#     # PN|ON, NTNB|SELIC|LTF, carencia CDB, QUANT FII
#     segment = models.CharField(max_length=10)
#     # VALOR cada acao, taxa Tesouro, taxa CDB, valor de compra|venda FII
#     tx_or_price = models.DecimalField(max_length=8, decimal_places=2)
#     quant = models.DecimalField(max_length=8, decimal_places=2)
#
#
# class InvestmentDetails(models.Model):
#     date = models.DateField()
#     # money invested
#     money = models.DecimalField(max_digits=8, decimal_places=2)
#     kind_of_investment = models.ForeignKey(KindOfInvest, on_delete=models.CASCADE)
#     brokerage_name = models.ManyToManyField(BrokerFirm)

