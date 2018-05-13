from django.test import TestCase

from charcoallog.investments.forms import InvestmentForm
from charcoallog.investments.models import Investment
from charcoallog.investments.post_service import MethodPost


class RQST:
    pass


class ValidPostMethod(TestCase):
    def setUp(self):
        self.user = 'teste'
        self.data = dict(
            user_name='you',
            date='2018-03-27',
            tx_op=00.00,
            money=94.42,
            kind='Títulos Públicos',
            which_target='Tesouro Direto',
            brokerage='Ativa'
        )

        self.query_user = Investment.objects.user_logged(self.user)
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

    def test_form_save(self):
        select_data = Investment.objects.get(id=1)
        select_dict = dict(
            user_name=select_data.user_name,
            date=select_data.date.strftime('%Y-%m-%d'),
            tx_op=float(select_data.tx_op),
            money=float(select_data.money),
            kind=select_data.kind,
            which_target=select_data.which_target,
            brokerage=select_data.brokerage
        )
        self.data['user_name'] = self.user
        self.assertDictEqual(self.data, select_dict)


# class TransferBetweenAccounts(TestCase):
#     def setUp(self):
#         self.user = 'teste'
#         self.account_1 = 'principal'
#         self.account_2 = 'cartao credito'
#         self.value = '-10.00'
#         self.value_after_transfer = '10.00'
#         self.data = dict(
#             user_name=self.user,
#             date='2017-12-21',
#             money=self.value,
#             description=self.account_2,
#             category='transfer',
#             payment=self.account_1,
#         )
#
#         self.query_user = Extract.objects.user_logged(self.user)
#         self.response = MethodPost('POST', self.data, self.user, self.query_user)
#
#     def test_negative_transfer_name(self):
#         p_data = self.query_user.get(id=1)
#         self.assertEqual(p_data.payment, self.account_1)
#
#     def test_negative_transfer_value(self):
#         p_data = self.query_user.get(id=1)
#         self.assertEqual(p_data.money, Decimal(self.value))
#
#     def test_positive_transfer_name(self):
#         c_c_data = self.query_user.get(id=2)
#         self.assertEqual(c_c_data.payment, self.account_2)
#
#     def test_positive_transfer_value(self):
#         c_c_data = self.query_user.get(id=2)
#         self.assertEqual(c_c_data.money, Decimal(self.value_after_transfer))
#
