from django.test import TestCase

from charcoallog.investments.forms import InvestmentForm
from charcoallog.investments.models import NewInvestment
from charcoallog.investments.post_service import MethodPost


class RQST:
    pass


class ValidPostMethod(TestCase):
    def setUp(self):
        self.user = 'teste'
        self.data = dict(
            user_name='you',
            date='2018-03-27',
            money=94.42,
            kind='Títulos Públicos',
            tx_op=00.00,
            brokerage='Ativa'
        )

        self.query_user = NewInvestment.objects.user_logged(self.user)
        RQST.method = 'POST'
        RQST.POST = self.data
        RQST.user = self.user
        self.response = MethodPost(RQST, self.query_user)

    def test_investmentform_instance(self):
        """
            investmentform attr must be a InvestmentForm instance.
        """
        self.assertIsInstance(self.response.investmentform(), InvestmentForm)

    def test_form_is_valid(self):
        self.assertTrue(self.response.form.is_valid())

    def test_basicdata_form_save(self):
        select_data = self.query_user.get(pk=1)
        select_dict = dict(
            user_name=select_data.user_name,
            date=select_data.date.strftime('%Y-%m-%d'),
            tx_op=float(select_data.tx_op),
            money=float(select_data.money),
            kind=select_data.kind,
            brokerage=select_data.brokerage
        )
        self.data['user_name'] = self.user
        self.assertDictEqual(self.data, select_dict)
