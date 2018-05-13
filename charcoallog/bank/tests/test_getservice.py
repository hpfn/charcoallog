from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.test import TestCase

from charcoallog.bank.forms import SelectExtractForm
from charcoallog.bank.get_service import MethodGet
from charcoallog.bank.models import Extract


class RQST:
    pass


class InvalidGetMethod(TestCase):
    def test_no_get_method(self):
        """ Send a POST must keep get_form attribute as 'None' """
        data = dict(date='2017-12-21',
                    money='10.00',
                    description='test',
                    category='test',
                    payment='principal')
        query_user = Extract.objects.user_logged('teste')
        RQST.method = "POST"
        RQST.GET = data
        response = MethodGet(RQST, query_user)
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
        RQST.method = "GET"
        RQST.GET = search_data
        self.response = MethodGet(RQST, query_user)

    def test_send_get_method(self):
        """
            Valid GET method must set get_form attribute as
            an instance of SelectExtractForm.
        """
        self.assertIsInstance(self.response.get_form, SelectExtractForm)

    def test_valid_form(self):
        self.assertTrue(self.response.get_form.is_valid())

    def test_valid_search(self):
        """
            query_default attribute must be a QuerySet instance
            after a valid search.
        """
        self.assertIsInstance(self.response.query_default, QuerySet)


# I do not know how to pretend a complete request(RQST)
# to show an 'messages.error()
class InvalidSearch(TestCase):
    def setUp(self):
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        self.login_in = self.client.login(username='teste', password='1qa2ws3ed')
        search_data = dict(column='all', from_date='2017-01-01', to_date='2017-01-01')
        self.response = self.client.get('/bank/', search_data)

    def test_invalid_search(self):
        """ Invalid search must shows an error message """
        self.assertContains(self.response, '<ul class="messages"', 1)
        self.assertContains(self.response, '<li class="error">', 1)
