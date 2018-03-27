from django.test import TestCase


class InvestmentModelTest(TestCase):
    def test_create(self):
        """ WTTD M3A03 """
        obj = InvestmentDetails(
            date='2018-03-27',
            money='94.42',
            #kind_of_investment=models.ForeignKey(KindOfInvest, on_delete=models.CASCADE),
            # Nome Acao, Tesouro, CDB, FII
            kind='Títulos Públicos',
            # Qual acao, tesouro, banco(CDB), cod FII
            which_target='Tesouro Direto',
            # PN|ON, NTNB|SELIC|LTF, carencia CDB, QUANT FII
            segment='Selic 2023',
            # VALOR cada acao, taxa Tesouro, taxa CDB, valor de compra|venda FII
            tx_or_price='0.01',
            quant='1',
            brokerage_name='Ativa'
        )
        obj.save()
        self.assertTrue(InvestmentDetail.objects.exists())
