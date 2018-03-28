from django.test import TestCase
from charcoallog.investment.models import InvestmentDetails, KindOfInvest, BrokerFirm


class InvestmentModelTest(TestCase):
    def test_create(self):
        """ WTTD M3A03 """
        InvestmentDetails.objects.create(
            date='2018-03-27',
            money=94.42,
            kind_of_investment=KindOfInvest(
                kind='Títulos Públicos',
                which_target='Tesouro Direto',
                segment='Selic 2023',
                tx_or_price=0.01,
                quant=1.00,
            ),
            brokerage_name=BrokerFirm(brokerage='Ativa')
        )
        self.assertTrue(InvestmentDetails.objects.exists())
