from django.test import TestCase
from charcoallog.investments.models import Investment, InvestmentDetails


class InvestmentModelTest(TestCase):
    def test_create_investment(self):
        """ WTTD M3A03 """
        Investment.objects.create(
            date='2018-03-27',
            tx_op=00.00,
            money=94.42,
            kind='Títulos Públicos',
            which_target='Tesouro Direto',
            brokerage='Ativa'
        )
        self.assertTrue(Investment.objects.exists())

    def test_create_investment_details(self):
        InvestmentDetails.objects.create(
            date='2018-03-27',
            money=94.42,
            kind='Títulos Públicos',
            which_target='Tesouro Direto',
            segment='Selic 2023',
            tx_or_price=0.01,
            quant=1.00,
        )