from django.test import TestCase

from charcoallog.investments.brief_investment_service import BriefInvestment
from charcoallog.investments.get_service import MethodGet
from charcoallog.investments.models import InvestmentStatementQuerySet
from charcoallog.investments.post_service import MethodPost
from charcoallog.investments.service import ShowData


class RQST:
    pass


class ServiceTest(TestCase):
    def setUp(self):
        RQST.method = None
        RQST.POST = {}
        RQST.user = 'teste'
        self.service = ShowData(RQST)

    def test_query_set_invest(self):
        self.assertIsInstance(self.service.newinvestment, InvestmentStatementQuerySet)

    def test_query_set_investdetail(self):
        self.assertIsInstance(self.service.newinvestmentdetails, InvestmentStatementQuerySet)

    def test_methodget(self):
        self.assertIsInstance(self.service.methodget, MethodGet)

    def test_methodpost(self):
        self.assertIsInstance(self.service.methodpost, MethodPost)

    def test_brief_investment(self):
        self.assertIsInstance(self.service.brief_investment, BriefInvestment)
