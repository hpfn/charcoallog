from decimal import Decimal
from django.test import TestCase

from charcoallog.core.models import Extract
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

    def test_get_total(self):
        """ whats_left attribute must be 10 for user teste """
        self.assertEqual(self.response.whats_left, Decimal('10.00'))
