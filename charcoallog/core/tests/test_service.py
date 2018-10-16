from django.db.models import QuerySet
from django.test import TestCase

from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.core import service
from charcoallog.core.service import BuildHome
from charcoallog.investments.brief_investment_service import BriefInvestment


class BuildHomeTest(TestCase):
    def setUp(self):
        self.user = 'teste'
        self.obj = BuildHome(self.user)

    def test_attr(self):
        expected = [
            hasattr(service, 'Extract'),
            hasattr(service, 'BriefBank'),
            hasattr(service, 'Scrap'),
            hasattr(self.obj, 'query_user'),
            hasattr(self.obj, 'line1'),
            hasattr(self.obj, 'selic_info'),
            hasattr(self.obj, 'ibov_info'),
            hasattr(self.obj, 'ipca_info'),
            hasattr(self.obj, 'query_user_invest'),
            hasattr(self.obj, 'query_user_details'),
            hasattr(self.obj, 'line2'),
        ]

        for e in expected:
            with self.subTest():
                self.assertTrue(e)

    def test_instance(self):
        expected = [
            (isinstance(self.obj.query_user, QuerySet)),
            (isinstance(self.obj.line1, BriefBank)),
            (isinstance(self.obj.selic_info, list)),
            (isinstance(self.obj.ibov_info, list)),
            (isinstance(self.obj.ipca_info, list)),
            (isinstance(self.obj.query_user_invest, QuerySet)),
            (isinstance(self.obj.query_user_details, QuerySet)),
            (isinstance(self.obj.line2, BriefInvestment)),

        ]

        for e in expected:
            with self.subTest():
                self.assertTrue(e)
