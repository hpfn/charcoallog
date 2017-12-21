from django.db.models import QuerySet
from django.test import TestCase

from charcoallog.core.forms import SelectExtractForm
from charcoallog.core.get_service import MethodGet
from charcoallog.core.models import Extract


class InvalidGetMethod(TestCase):
    def test_no_get_method(self):
        """ Send a POST must keep get_form attribute as 'None' """
        data = dict(date='2017-12-21',
                    money='10.00',
                    description='test',
                    category='test',
                    payment='principal')
        query_user = Extract.objects.user_logged('teste')
        response = MethodGet('POST', data, query_user)
        self.assertEqual(response.get_form, None)


class ValidGetMethod(TestCase):
    def setUp(self):
        data = dict(
            user_name='teste',
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment='principal'
        )

        Extract.objects.create(**data)

        query_user = Extract.objects.user_logged('teste')
        search_data = dict(column='all', from_date='2017-12-01', to_date='2017-12-31')
        self.response = MethodGet('GET', search_data, query_user)

    def test_send_get_method(self):
        """
            Valid GET method must set get_form attribute as
            an instance of SelectExtractForm.
        """
        self.assertIsInstance(self.response.get_form, SelectExtractForm)

    def test_valid_search(self):
        """
            query_default attribute must be a QuerySet instance
            after a valid search.
        """
        self.assertIsInstance(self.response.query_default, QuerySet)


class InvalidSearch(TestCase):
    def setUp(self):
        self.data = dict(
            user_name='teste',
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment='principal'
        )
        Extract.objects.create(**self.data)
        self.query_user = Extract.objects.user_logged('teste')

    def test_invalid_search(self):
        """ Invalid search must set query_default attribute as 'None' """
        search_data = dict(column='all', from_date='2017-01-01', to_date='2017-01-01')
        response = MethodGet('GET', search_data, self.query_user)
        self.assertEqual(response.query_default, None)
