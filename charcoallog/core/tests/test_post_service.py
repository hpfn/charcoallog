from decimal import Decimal
from django.test import TestCase

from charcoallog.core.forms import EditExtractForm
from charcoallog.core.models import Extract
from charcoallog.core.post_service import MethodPost


class ValidPostMethod(TestCase):
    def setUp(self):
        user = 'teste'
        self.data = dict(
            user_name=user,
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment='principal',
            update_rm='',
            pk=''
        )

        query_user = Extract.objects.user_logged(user)
        self.response = MethodPost('POST', self.data, user, query_user)

    def test_editextractform_instance(self):
        """
            editextractform attr must be a EditExtractForm instance.
        """
        self.assertIsInstance(self.response.editextractform(), EditExtractForm)

    def test_form_is_valid(self):
        self.assertTrue(self.response.form.is_valid())

    def test_form_save(self):
        select_data = Extract.objects.get(id='1')
        self.assertEqual(self.data.get('user_name'), select_data.user_name)
        self.assertEqual(self.data.get('date'), select_data.date.strftime('%Y-%m-%d'))
        self.assertEqual(Decimal(self.data.get('money')), select_data.money)
        self.assertEqual(self.data.get('description'), select_data.description)
        self.assertEqual(self.data.get('category'), select_data.category)
        self.assertEqual(self.data.get('payment'), select_data.payment)
        # self.assertEqual(self.data.get('update_rm'), select_data.update_rm)
        # self.assertEqual(self.data.get('pk'), select_data.pk)
