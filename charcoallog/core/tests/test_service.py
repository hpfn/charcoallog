from collections import OrderedDict
from decimal import Decimal

from django.db.models import QuerySet
from django.test import TestCase

from charcoallog.core.get_service import MethodGet
from charcoallog.core.line1_service import Line1
from charcoallog.core.models import Extract
from charcoallog.core.post_service import MethodPost
from charcoallog.core.service import ShowData


class ServiceLayerTest(TestCase):
    def setUp(self):
        user_name = 'teste'
        data = dict(
            user_name=user_name,
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment='principal'
        )
        others_data = dict(
            user_name='other',
            date='2017-12-21',
            money='100.00',
            description='test',
            category='test',
            payment='principal'
        )

        Extract.objects.create(**data)
        Extract.objects.create(**others_data)
        search_data = dict(column='all', from_date='2017-12-01', to_date='2017-12-31')
        self.response = ShowData('GET', search_data, dict(), user_name)

    def test_query_user_instance(self):
        self.assertIsInstance(self.response.query_user, QuerySet)

    def test_form1_instance(self):
        self.assertIsInstance(self.response.form1, MethodPost)

    def test_form2_instance(self):
        self.assertIsInstance(self.response.form2, MethodGet)

    def test_line1_instance(self):
        self.assertIsInstance(self.response.line1, Line1)

    def test_account_names_attr(self):
        self.assertEqual(
            self.response.account_names,
            OrderedDict([('principal', {'money__sum': Decimal('10.00')})])
        )

    def test_get_total(self):
        """ whats_left attribute must be 10 for user teste """
        self.assertEqual(self.response.whats_left, Decimal('10.00'))
