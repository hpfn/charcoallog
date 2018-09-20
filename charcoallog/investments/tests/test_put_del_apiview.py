import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase
from rest_framework.views import APIView

from charcoallog.investments.models import (
    BasicData, Investment, InvestmentDetails
)
from charcoallog.investments.views import DetailAPI, FormDeals

b_data = dict(
    user_name="teste",
    date="2018-08-30",
    money=1000,
    kind="Títulos Públicos",
    # which_target="selic"
)

i_data = dict(
    tx_op=10.00,
    brokerage="ALTA",
    basic_data=""
)


class FormDealsAttrTest(TestCase):
    def setUp(self):
        self.attrs = FormDeals()

    def test_get_object_attr(self):
        self.assertTrue(hasattr(self.attrs, 'get_object'))

    def test_out_attr(self):
        self.assertFalse(hasattr(self.attrs, 'put'))

    def test_delete_attr(self):
        self.assertTrue(hasattr(self.attrs, 'delete'))

    def test_get_attr(self):
        self.assertFalse(hasattr(self.attrs, 'get'))

    def test_post_attr(self):
        self.assertFalse(hasattr(self.attrs, 'post'))

    def test_inheritance(self):
        self.assertTrue(issubclass(FormDeals, APIView))

    def test_inheritance_1(self):
        self.assertTrue(issubclass(FormDeals, LoginRequiredMixin))


class AccessFormDealsAPIView(TestCase):
    def setUp(self):
        bsc_data = BasicData.objects.create(**b_data)
        i_data['basic_data'] = bsc_data
        Investment.objects.create(**i_data)

        self.to_update = dict()
        self.to_update['basic_data'] = b_data
        self.to_update['brokerage'] = 'baixa'
        self.to_update['tx_op'] = 10.00

    def test_no_access(self):
        """ No login yet. No access to the APIView"""
        response = self.client.put(r('investments:api', 1), json.dumps(self.to_update),
                                   content_type='application/json')
        self.assertEqual(403, response.status_code)


class FormDealsDeleteAPIView(TestCase):
    def setUp(self):
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        bsc_data = BasicData.objects.create(**b_data)
        i_data['basic_data'] = bsc_data
        Investment.objects.create(**i_data)

        self.login_in = self.client.login(username='teste', password='1qa2ws3ed')

    def test_method_not_permitted(self):
        """ Method not Allowed """
        response = self.client.get(r('investments:api', 1))
        self.assertEqual(405, response.status_code)

    def test_good_data(self):
        """ Send good data to PUT"""
        to_put = dict()
        b_data['money'] = 3000.00
        to_put['basic_data'] = b_data
        to_put['brokerage'] = "TO PUT"
        to_put['tx_op'] = 10.00
        response = self.client.put(r('investments:api', 1), json.dumps(to_put),
                                   content_type='application/json')
        # method PUT is not allowed
        self.assertEqual(405, response.status_code)
        #
        # expected = [
        #     "TO PUT",
        #     '3000.00'
        # ]
        # for value in expected:
        #     with self.subTest():
        #         self.assertNotIn(value, response.content.decode())
        # # self.assertIn('3000.00', response.content.decode())
        # b_data['money'] = 1000.00

    # def test_invalid_data(self):
    #     """ Send invalid data to PUT """
    #     to_put = dict()
    #     to_put['basic_data'] = b_data
    #     to_put['brokerage'] = "TO PUT"
    #     # No 'tx_op' makes data .is_valid() False
    #     response = self.client.put(r('investments:api', 1), json.dumps(to_put),
    #                                content_type='application/json')
    #     self.assertEqual(400, response.status_code)
    #     # No updated data
    #     self.assertNotIn(to_put["brokerage"], response.content.decode())

    def test_delete_data(self):
        """ DELETE data in DB"""
        response = self.client.delete(r('investments:api', 1))
        self.assertEqual(204, response.status_code)


class DetailAPIAttrTest(TestCase):
    def setUp(self):
        self.attrs = DetailAPI()

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
        self.assertTrue(issubclass(DetailAPI, APIView))

    def test_inheritance_1(self):
        self.assertTrue(issubclass(DetailAPI, LoginRequiredMixin))


class AccessDetailAPI(TestCase):
    def setUp(self):
        bsc_data = BasicData.objects.create(**b_data)
        i_data['basic_data'] = bsc_data
        Investment.objects.create(**i_data)

        self.to_update = dict()
        self.to_update['basic_data'] = b_data
        self.to_update['which_target'] = 'qq'
        self.to_update['segment'] = 'baixa'
        self.to_update['tx_or_price'] = 10.00
        self.to_update['quant'] = 10.00

    def test_no_access(self):
        """ No login yet. No access to the APIView"""
        response = self.client.put(r('investments:detail_api', 1), json.dumps(self.to_update),
                                   content_type='application/json')
        self.assertEqual(403, response.status_code)


class DetailAPITest(TestCase):
    def setUp(self):
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        to_put = dict()
        to_put['basic_data'] = b_data
        to_put['which_target'] = "NO"
        to_put['segment'] = "INSERT"
        to_put['tx_or_price'] = 0.00
        to_put['quant'] = 0.00

        bsc_data = BasicData.objects.create(**b_data)
        to_put['basic_data'] = bsc_data
        InvestmentDetails.objects.create(**to_put)

        self.login_in = self.client.login(username='teste', password='1qa2ws3ed')

    def test_login(self):
        self.assertTrue(self.login_in)

    def test_data_in_db(self):
        """ Data saved in html"""
        response = self.client.get(r('investments:detail', b_data['kind']))
        self.assertEqual(200, response.status_code)

    def test_good_data(self):
        """ Send good data to PUT"""
        to_put = dict()
        b_data['money'] = 3000.00
        to_put['basic_data'] = b_data
        to_put['which_target'] = "TO GO"
        to_put['segment'] = "TO PUT"
        to_put['tx_or_price'] = 10.00
        to_put['quant'] = 10.00

        self.assertTrue(InvestmentDetails.objects.filter(pk=1).exists())
        self.assertEqual(InvestmentDetails.objects.all().count(), 1)

        response = self.client.put(r('investments:detail_api', 1),
                                   json.dumps(to_put),
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
        # self.assertIn('3000.00', response.content.decode())
        b_data['money'] = 1000.00

        self.assertTrue(InvestmentDetails.objects.filter(pk=1).exists())
        self.assertEqual(InvestmentDetails.objects.all().count(), 1)

    def test_invalid_data(self):
        """ Send invalid data to PUT """
        to_put = dict()
        to_put['basic_data'] = b_data
        to_put['segment'] = "TO PUT"
        # No 'tx_op' makes data .is_valid() False
        response = self.client.put(r('investments:detail_api', 1), json.dumps(to_put),
                                   content_type='application/json')
        self.assertEqual(400, response.status_code)
        # No updated data
        self.assertNotIn(to_put["segment"], response.content.decode())

    def test_delete_data(self):
        """ DELETE data in DB"""
        response = self.client.delete(r('investments:detail_api', 1))
        self.assertEqual(204, response.status_code)
