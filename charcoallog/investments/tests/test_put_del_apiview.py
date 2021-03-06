import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase
from rest_framework.views import APIView

from charcoallog.investments.models import NewInvestment, NewInvestmentDetails
from charcoallog.investments.views import DetailApi, HomeApi

data = dict(
    user_name="teste",
    date="2018-08-30",
    money=1000,
    kind="Títulos Públicos",
    tx_op=0.00,
    brokerage='A'
)


class FormDealsAttrTest(TestCase):
    def setUp(self):
        self.attrs = HomeApi()

    def test_get_object_attr(self):
        self.assertTrue(hasattr(self.attrs, 'get_object'))

    def test_out_attr(self):
        self.assertTrue(hasattr(self.attrs, 'put'))

    def test_delete_attr(self):
        self.assertTrue(hasattr(self.attrs, 'delete'))

    def test_get_attr(self):
        self.assertFalse(hasattr(self.attrs, 'get'))

    def test_post_attr(self):
        self.assertFalse(hasattr(self.attrs, 'post'))

    def test_inheritance(self):
        self.assertTrue(issubclass(HomeApi, APIView))

    def test_inheritance_1(self):
        self.assertTrue(issubclass(HomeApi, LoginRequiredMixin))


class NoAccessFormDealsAPIView(TestCase):
    def setUp(self):
        i_data = {}
        i_data.update(data)
        i_data['tx_op'] = 10.00
        i_data['brokerage'] = "ALTA"

        NewInvestment.objects.create(**i_data)

    def test_no_access(self):
        """ No login yet. No access to the APIView"""
        response = self.client.delete(r('investments:home_api', 1))
        self.assertEqual(403, response.status_code)

    def test_delete_data(self):
        """ DELETE data in DB"""
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        login_in = self.client.login(username='teste', password='1qa2ws3ed')  # noqa F841
        response = self.client.delete(r('investments:home_api', 1))
        self.assertEqual(204, response.status_code)


class FormDealsAPIAttrTest(TestCase):
    def setUp(self):
        self.attrs = HomeApi()

    def test_inheritance(self):
        self.assertTrue(issubclass(HomeApi, APIView))

    def test_inheritance_1(self):
        self.assertTrue(issubclass(HomeApi, LoginRequiredMixin))

    def test_get_object_attr(self):
        self.assertTrue(hasattr(self.attrs, 'get_object'))

    def test_out_attr(self):
        self.assertTrue(hasattr(self.attrs, 'put'))

    def test_delete_attr(self):
        self.assertTrue(hasattr(self.attrs, 'delete'))

    def test_get_attr(self):
        self.assertFalse(hasattr(self.attrs, 'get'))

    def test_post_attr(self):
        self.assertFalse(hasattr(self.attrs, 'post'))


class DetailApiAttrTest(TestCase):
    def setUp(self):
        self.attrs = DetailApi()

    def test_inheritance(self):
        self.assertTrue(issubclass(DetailApi, APIView))

    def test_inheritance_1(self):
        self.assertTrue(issubclass(DetailApi, LoginRequiredMixin))

    def test_get_object_attr(self):
        self.assertTrue(hasattr(self.attrs, 'get_object'))

    def test_out_attr(self):
        self.assertTrue(hasattr(self.attrs, 'put'))

    def test_delete_attr(self):
        self.assertTrue(hasattr(self.attrs, 'delete'))

    def test_get_attr(self):
        self.assertFalse(hasattr(self.attrs, 'get'))

    def test_post_attr(self):
        self.assertFalse(hasattr(self.attrs, 'post'))


to_put = dict()
to_put.update(data)
to_put['which_target'] = "NO"
to_put['segment'] = "INSERT"
to_put['tx_or_price'] = 0.00
to_put['quant'] = 0.00


class NoAccessDetailApi(TestCase):
    def setUp(self):
        NewInvestmentDetails.objects.create(**to_put)

    def test_no_access(self):
        """ No login yet. No access to the APIView"""
        response = self.client.delete(r('investments:details_api', 1))
        self.assertEqual(403, response.status_code)


class NoAccessFormDealsAPI(TestCase):
    def test_no_access(self):
        """ No login yet. No access to the APIView"""
        response = self.client.delete(r('investments:home_api', 1))
        self.assertEqual(403, response.status_code)


class FormDealsTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        NewInvestment.objects.create(**data)

        self.login_in = self.client.login(username='teste', password='1qa2ws3ed')

    def test_login(self):
        self.assertTrue(self.login_in)

    def test_send_data_to_put(self):
        data['brokerage'] = "B"
        data['kind'] = "BLABLA"
        response = self.client.put(r('investments:home_api', 1), json.dumps(data),
                                   content_type='application/json')

        self.assertEqual(200, response.status_code)

        expected = [
            'B',
            'BLABLA'
        ]

        for value in expected:
            with self.subTest():
                self.assertIn(value, response.content.decode())

        data['brokerage'] = "A"
        data['kind'] = "Títulos Públicos"

    def test_delete(self):
        response = self.client.delete(r('investments:home_api', 1))  # noqa
        self.assertFalse(NewInvestment.objects.exists())


class DetailApiTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        NewInvestmentDetails.objects.create(**to_put)

        self.login_in = self.client.login(username='teste', password='1qa2ws3ed')

    def test_login(self):
        self.assertTrue(self.login_in)

    def test_data_in_db(self):
        """ Data saved in DB showed in html"""
        response = self.client.get(r('investments:details', data['kind']))
        self.assertEqual(200, response.status_code)
        expected = [
            "NO",
            "INSERT",
            '0.00'
        ]
        for value in expected:
            with self.subTest():
                self.assertIn(value, response.content.decode())

    def test_good_data(self):
        """ Send good data to PUT"""
        l_put = dict()
        l_put.update(data)
        l_put['money'] = 3000.00
        l_put['which_target'] = "TO GO"
        l_put['segment'] = "TO PUT"
        l_put['tx_or_price'] = 10.00
        l_put['quant'] = 10.00

        self.assertTrue(NewInvestmentDetails.objects.filter(pk=1).exists())
        self.assertEqual(NewInvestmentDetails.objects.all().count(), 1)

        response = self.client.put(r('investments:details_api', 1),
                                   json.dumps(l_put),
                                   content_type='application/json')

        self.assertEqual(200, response.status_code)

        expected = [
            "TO GO",
            "TO PUT",
            '3000.00'
        ]
        for value in expected:
            with self.subTest():
                self.assertIn(value, response.content.decode())
        data['money'] = 1000.00

        self.assertTrue(NewInvestmentDetails.objects.filter(pk=1).exists())
        self.assertEqual(NewInvestmentDetails.objects.all().count(), 1)

    def test_invalid_data(self):
        """ Send invalid data to PUT """
        l_put = dict()
        l_put['segment'] = "TO PUT"
        # No fields makes data .is_valid() False
        response = self.client.put(r('investments:details_api', 1),
                                   json.dumps(l_put),
                                   content_type='application/json')
        self.assertEqual(400, response.status_code)
        # No updated data
        self.assertNotIn(to_put["segment"], response.content.decode())

    def test_delete(self):
        response = self.client.delete(r('investments:details_api', 1))  # noqa
        self.assertFalse(NewInvestmentDetails.objects.exists())
