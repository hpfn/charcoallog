from collections import OrderedDict

from django.db.models import QuerySet
from django.test import TestCase

from charcoallog.investments.brief_investment_service import BriefInvestment
from charcoallog.investments.models import (
    BasicData, Investment, InvestmentDetails
)


class BriefInvestmentTest(TestCase):
    def setUp(self):
        b_data = dict(
            user_name='you',
            date='2018-03-27',
            money=94.42,
            kind='---',
            # which_target='---',
        )
        b_data = BasicData.objects.create(**b_data)

        self.data = dict(
            tx_op=00.00,
            brokerage='Ativa',
            basic_data=b_data
        )

        Investment.objects.create(**self.data)
        query_set_invest = Investment.objects.select_related('basic_data').user_logged('you')
        query_set_investdetail = InvestmentDetails.objects.select_related('basic_data').user_logged('you')
        self.brief = BriefInvestment(query_set_invest, query_set_investdetail)

    def test_check_query_user_invest(self):
        self.assertIsInstance(self.brief._query_user_invest, QuerySet)

    def test_check_query_user_invest_detail(self):
        self.assertIsInstance(self.brief._query_user_investdetail, QuerySet)

    def test_briefinvestments_brokerage(self):
        self.assertIsInstance(self.brief.brokerage(), OrderedDict)

    def test_dict_key_brokerage(self):
        dict_from_brief = self.brief.brokerage()
        self.assertIn('Ativa', dict_from_brief.keys())

    def test_briefinvestments_kind_invest(self):
        self.assertIsInstance(self.brief.brokerage(), OrderedDict)

    def test_dict_key_kind_invest(self):
        dict_from_brief = self.brief.brokerage()
        self.assertIn('Ativa', dict_from_brief.keys())
