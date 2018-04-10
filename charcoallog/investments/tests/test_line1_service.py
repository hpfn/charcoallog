from decimal import Decimal
from django.test import TestCase
from charcoallog.investments.brief_investment_service import BriefInvestment
from charcoallog.investments.models import Investment


class BriefInvestmentTest(TestCase):
    def setUp(self):
        #user_name = 'teste'
        self.brokerage_name = 'ATIVA'
        data = dict(
            #user_name=user_name,
            date='2018-03-27',
            tx_op=00.00,
            money='10.00',
            kind='Títulos Públicos',
            which_target='Tesouro Direto',
            brokerage=self.brokerage_name
        )

        Investment.objects.create(**data)
        #query_user = Extract.objects.user_logged(user_name)
        self.response = BriefInvestment()
        self.brief_investment_brokerage = self.response.brokerage_names()

    def test_line1_borkerage_names(self):
        """ Brokerage Name """
        self.assertIn(self.brokerage_name, self.brief_investment_brokerage)

    def test_line1_brokerage_total_amount(self):
        """
            How much money at brokerage
        """
        self.assertEqual(self.response.total_amount(), Decimal('10.00'))
