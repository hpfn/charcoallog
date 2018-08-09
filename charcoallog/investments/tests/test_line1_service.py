# from decimal import Decimal
from django.test import TestCase

from charcoallog.investments.brief_investment_service import BriefInvestment
from charcoallog.investments.models import (BasicData, Investment,
                                            InvestmentDetails)


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
            which_target='Tesouro Direto',
        )
        b_data = BasicData.objects.create(**data)

        data = dict(
            tx_op=00.00,
            brokerage=self.brokerage_name,
            basic_data=b_data

        )
        Investment.objects.create(**data)
        query_user_invest = Investment.objects.select_related('basic_data').user_logged(user_name)
        query_user_investdetail = InvestmentDetails.objects.select_related('basic_data').user_logged(user_name)
        self.response = BriefInvestment(query_user_invest, query_user_investdetail)
        self.brief_investment_brokerage = self.response.brokerage()
        self.brief_investment_type = self.response.kind_investment()

    def test_line1_borkerage_names(self):
        """ Brokerage Name """
        self.assertIn(self.brokerage_name, self.brief_investment_brokerage.keys())

    def test_investment_type(self):
        """ Type of investment """
        self.assertIn(self.kind, self.brief_investment_type.keys())

    #  def test_line1_brokerage_total_amount(self):
    #      """ How much money at brokerage """
    #      self.assertEqual(self.response.total_amount(self.brief_investment_brokerage.values()), Decimal('10.00'))
    #
    #  def test_investment_type_total_amount(self):
    #      """ How much money by investment """
    #      self.assertEqual(self.response.total_amount(self.brief_investment_type.values()), Decimal('10.00'))
