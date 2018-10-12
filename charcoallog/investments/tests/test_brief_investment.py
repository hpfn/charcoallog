from collections import OrderedDict
from decimal import Decimal

from django.db.models import QuerySet
from django.test import TestCase

from charcoallog.investments.brief_investment_service import BriefInvestment
from charcoallog.investments.models import NewInvestment, NewInvestmentDetails


class BriefInvestmentTest(TestCase):
    def setUp(self):
        # models has default value
        self.data_i = dict(
            user_name='you',
            date='2018-03-27',
            money=94.42,
            # kind
            # tx_op
            brokerage='A'
        )

        NewInvestment.objects.create(**self.data_i)

        # models has default value
        self.data_d = dict(
            user_name='you',
            date='2018-03-27',
            money=-94.42,
            kind='CDB',
            # tx_op
            brokerage='A',
            which_target='banco segunda linha',
            segment='12 meses',
            tx_or_price=00.00,
            quant=00.00
        )

        NewInvestmentDetails.objects.create(**self.data_d)

        query_set_invest = NewInvestment.objects.user_logged('you')
        query_set_investdetail = NewInvestmentDetails.objects.user_logged('you')
        self.brief = BriefInvestment(query_set_invest, query_set_investdetail)

    def test_check_query_user_invest(self):
        self.assertIsInstance(self.brief._query_user_invest, QuerySet)

    def test_check_query_user_invest_detail(self):
        self.assertIsInstance(self.brief._query_user_investdetail, QuerySet)

    def test_briefinvestments_brokerage(self):
        self.assertIsInstance(self.brief.brokerage(), OrderedDict)

    def test_newinvest_data_exits(self):
        self.assertTrue(NewInvestment.objects.exists())

    def test_investdetails_data_exists(self):
        self.assertTrue(NewInvestmentDetails.objects.exists())

    def test_dict_key_brokerage(self):
        """
        Brokerage received 94.42 and put 94.42 in CDB. 0 is expected in account
        """
        dict_from_brief = self.brief.brokerage()
        self.assertIn('A', dict_from_brief.keys())
        self.assertEqual(Decimal('0.00'), list(dict_from_brief.values())[0])

    def test_briefinvestments_kind_invest(self):
        self.assertIsInstance(self.brief.kind_investmentdetail(), OrderedDict)

    def test_dict_key_kind(self):
        dict_kind = self.brief.kind_investmentdetail()
        expected = [
            ('CDB', dict_kind.keys()),
            (Decimal('-94.42'), dict_kind.values())
        ]

        for e, d in expected:
            with self.subTest():
                self.assertIn(e, d)

    def test_sum_with_two_brokerages(self):
        self.data_i['money'] = 100.00
        self.data_i['brokerage'] = 'BLABLA'
        NewInvestment.objects.create(**self.data_i)

        dict_brokerage = self.brief.brokerage()

        expected = [
            ('BLABLA', dict_brokerage.keys()),
            (Decimal('100.00'), dict_brokerage.values())
        ]

        for e, d in expected:
            with self.subTest():
                self.assertIn(e, d)

    def test_two_kind_investdetails(self):
        self.data_d['kind'] = 'paper'
        self.data_d['which_target'] = 'vale'
        self.data_d['segment'] = 'on'
        NewInvestmentDetails.objects.create(**self.data_d)

        dict_kind = self.brief.kind_investmentdetail()
        expected = [
            ('CDB', dict_kind.keys()),
            (Decimal('-94.42'), dict_kind.values()),
            ('paper', dict_kind.keys()),
            (Decimal('-94.42'), dict_kind.values())
        ]

        for e, d in expected:
            with self.subTest():
                self.assertIn(e, d)
