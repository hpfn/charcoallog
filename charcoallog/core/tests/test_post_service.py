from decimal import Decimal
from django.test import TestCase

from charcoallog.core.forms import EditExtractForm
from charcoallog.core.models import Extract
from charcoallog.core.post_service import MethodPost


class ValidPostMethod(TestCase):
    def setUp(self):
        self.user = 'teste'
        self.data = dict(
            user_name=self.user,
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment='principal',
            update_rm='',
            pk=''
        )

        self.query_user = Extract.objects.user_logged(self.user)
        self.response = MethodPost('POST', self.data, self.user, self.query_user)

    def test_editextractform_instance(self):
        """
            editextractform attr must be a EditExtractForm instance.
        """
        self.assertIsInstance(self.response.editextractform(), EditExtractForm)

    def test_form_is_valid(self):
        self.assertTrue(self.response.form.is_valid())

    def test_form_save(self):
        select_data = Extract.objects.get(id=1)
        select_dict = dict(
            user_name=select_data.user_name,
            date=select_data.date.strftime('%Y-%m-%d'),
            money=str(select_data.money),
            description=select_data.description,
            category=select_data.category,
            payment=select_data.payment,
            update_rm='',
            pk=''
        )
        self.assertDictEqual(self.data, select_dict)


class TransferBetweenAccounts(TestCase):
    def setUp(self):
        self.user = 'teste'
        self.account_1 = 'principal'
        self.account_2 = 'cartao credito'
        self.value = '-10.00'
        self.value_after_transfer = '10.00'
        self.data = dict(
            user_name=self.user,
            date='2017-12-21',
            money=self.value,
            description=self.account_2,
            category='transfer',
            payment=self.account_1,
        )

        self.query_user = Extract.objects.user_logged(self.user)
        self.response = MethodPost('POST', self.data, self.user, self.query_user)

    def test_negative_transfer_name(self):
        p_data = self.query_user.get(id=1)
        self.assertEqual(p_data.payment, self.account_1)

    def test_negative_transfer_value(self):
        p_data = self.query_user.get(id=1)
        self.assertEqual(p_data.money, Decimal(self.value))

    def test_positive_transfer_name(self):
        c_c_data = self.query_user.get(id=2)
        self.assertEqual(c_c_data.payment, self.account_2)

    def test_positive_transfer_value(self):
        c_c_data = self.query_user.get(id=2)
        self.assertEqual(c_c_data.money, Decimal(self.value_after_transfer))

