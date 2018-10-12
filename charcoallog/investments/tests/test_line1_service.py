# from decimal import Decimal
from django.test import TestCase

from charcoallog.investments.brief_investment_service import BriefInvestment
from charcoallog.investments.models import NewInvestment, NewInvestmentDetails


class BriefInvestmentTest(TestCase):
    def setUp(self):
        user_name = 'teste'
        self.brokerage_name = 'ATIVA'
        self.kind = 'Títulos Públicos'

        data = dict(
            user_name=user_name,
            date='2018-03-27',
            money=10.00,
            kind=self.kind,
            tx_op=00.00,
            brokerage=self.brokerage_name,
        )

        NewInvestment.objects.create(**data)

        data['money'] = -10.00
        data['which_target'] = 'lft'
        data['segment'] = 'ipca 2035'
        data['tx_or_price'] = 0.00
        data['quant'] = 0.00

        NewInvestmentDetails.objects.create(**data)

        query_user_invest = NewInvestment.objects.user_logged(user_name)
        query_user_investdetail = NewInvestmentDetails.objects.user_logged(user_name)
        self.response = BriefInvestment(query_user_invest, query_user_investdetail)
        self.brief_investment_brokerage = self.response.brokerage()
        self.brief_investment_type = self.response.kind_investmentdetail()

    def test_line1_borkerage_names(self):
        """ Brokerage Name """
        self.assertIn(self.brokerage_name, self.brief_investment_brokerage.keys())

    def test_investment_type(self):
        """ Type of investment """
        self.assertIn(self.kind, self.brief_investment_type.keys())
