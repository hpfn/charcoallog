from collections import OrderedDict
from decimal import Decimal

from django.db.models import QuerySet
from django.test import TestCase

from charcoallog.investments.brief_investment_service import BriefInvestment
from charcoallog.investments.models import (
    BasicData, Investment, InvestmentDetails
)


class BriefInvestmentTest(TestCase):
    def setUp(self):
        self.b_data = dict(
            user_name='you',
            date='2018-03-27',
            money=-94.42,
            kind='CDB',
            # which_target='---',
        )
        b_data = BasicData.objects.create(**self.b_data)

        self.data = dict(
            tx_op=00.00,
            brokerage='Ativa',
            basic_data=b_data
        )

        Investment.objects.create(**self.data)
        query_set_invest = Investment.objects.user_logged('you')
        query_set_investdetail = InvestmentDetails.objects.user_logged('you')
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
        self.assertEqual(Decimal('-94.42'), list(dict_from_brief.values())[0])

    def test_briefinvestments_kind_invest(self):
        self.assertIsInstance(self.brief.kind_investment(), OrderedDict)

    def test_dict_key_kind(self):
        dict_kind = self.brief.kind_investment()
        expected = [
            ('CDB', dict_kind.keys()),
            (Decimal('94.42'), dict_kind.values())
        ]

        for e, d in expected:
            with self.subTest():
                self.assertIn(e, d)

    def test_sum_with_two_brokerages(self):
        self.b_data['money'] = -100.00
        b_data = BasicData.objects.create(**self.b_data)
        self.data['brokerage'] = 'BLABLA'
        self.data['basic_data'] = b_data
        Investment.objects.create(**self.data)

        dict_kind = self.brief.kind_investment()
        dict__brokerage = self.brief.brokerage()

        expected = [
            ('BLABLA', dict__brokerage.keys()),
            (Decimal('194.42'), dict_kind.values())
        ]

        for e, d in expected:
            with self.subTest():
                self.assertIn(e, d)
