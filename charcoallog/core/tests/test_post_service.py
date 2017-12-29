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

#    def test_delete_data(self):
#        self.data['update_rm'] = 'remove'
#        MethodPost('POST', self.data, self.user, self.query_user)
#        self.assertIsNone(Extract.objects.filter(id=1).first())
#
#    def test_update_data(self):
#        self.data['update_rm'] = 'update'
#        self.data['category'] = 'new_category'
#        self.data['pk'] = 1
#        MethodPost('POST', self.data, self.user, self.query_user)
#        select_data = Extract.objects.get(id=1)
#        self.assertEqual(self.data['category'], select_data.category)
#




