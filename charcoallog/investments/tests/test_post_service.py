from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from charcoallog.investments.forms import InvestmentForm
from charcoallog.investments.models import NewInvestment, NewInvestmentDetails
from charcoallog.investments.post_service import MethodPost


class RQST:
    pass


class ValidPostMethod(TestCase):
    def setUp(self):
        self.user = 'teste'
        user = User.objects.create(username=self.user)
        user.set_password('1qa2ws3ed')
        user.save()

        self.login_in = self.client.login(username=self.user, password='1qa2ws3ed')

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

    def test_login(self):
        self.assertTrue(self.login_in)

    def test_investmentform_instance(self):
        """
            investmentform attr must be a InvestmentForm instance.
        """
        self.assertIsInstance(self.response.investmentform(), InvestmentForm)

    def test_form_is_valid(self):
        self.assertTrue(self.response.i_form.is_valid())

    def test_invest_form_save(self):
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

    def test_send_invest_post_url(self):
        self.data['kind'] = 'HERE'
        response = self.client.post(r('investments:home'), self.data)  # noqa
        self.assertEqual('HERE', NewInvestment.objects.get(pk=2).kind)
        self.assertEqual(2, NewInvestment.objects.count())

    def test_send_details_post_url(self):
        self.data['kind'] = 'Details'
        self.data['which_target'] = 'Details'
        self.data['segment'] = 'Details'
        self.data['tx_or_price'] = 0.00
        self.data['quant'] = 0.00

        response = self.client.post(r('investments:home'), self.data)  # noqa
        self.assertTrue(NewInvestmentDetails.objects.exists())
        self.assertEqual('Details', NewInvestmentDetails.objects.get(pk=2).kind)
        self.assertEqual(2, NewInvestment.objects.count())
