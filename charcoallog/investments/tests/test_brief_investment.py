from collections import OrderedDict

from django.db.models import QuerySet
from django.test import TestCase

from charcoallog.investments.brief_investment_service import BriefInvestment
from charcoallog.investments.models import Investment


class BriefInvestmentTest(TestCase):
    def setUp(self):
        self.data = dict(
            user_name='you',
            date='2018-03-27',
            tx_op=00.00,
            money=94.42,
            kind='---',
            which_target='---',
            brokerage='Ativa'
        )
        Investment.objects.create(**self.data)
        self.brief = BriefInvestment('you')

    def test_check_query_user(self):
        self.assertIsInstance(self.brief._query_user, QuerySet)

    def test_briefinvestments(self):
        self.assertIsInstance(self.brief.brokerage_or_invest_type(), OrderedDict)

    def test_dict_key(self):
        dict_from_brief = self.brief.brokerage_or_invest_type()
        self.assertIn('Ativa', dict_from_brief.keys())
