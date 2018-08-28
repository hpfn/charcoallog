import json

from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from charcoallog.investments.models import BasicData, Investment


class AccessAPIView(TestCase):
    def setUp(self):
        b_data = dict(
            user_name="teste",
            date="2018-08-30",
            money=1000,
            kind="Títulos Públicos",
            which_target="selic"
        )
        bsc_data = BasicData.objects.create(**b_data)
        i_data = dict(
            tx_op=10.00,
            brokerage="ALTA",
            basic_data=bsc_data
        )
        Investment.objects.create(**i_data)
        self.to_update = {}
        self.to_update['basic_data'] = b_data
        self.to_update['brokerage'] = 'baixa'
        self.to_update['tx_op'] = 10.00

    def test_no_access(self):
        """ No login yet. No access to the APIView"""
        response = self.client.put(r('investments:update', 1), json.dumps(self.to_update),
                                   content_type='application/json')
        self.assertEqual(403, response.status_code)


class PutDeleteAPIView(TestCase):
    def setUp(self):
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        self.login_in = self.client.login(username='teste', password='1qa2ws3ed')

    def test_method_not_permitted(self):
        """ Method not Allowed """
        response = self.client.get(r('investments:update', 1))
        self.assertEqual(405, response.status_code)
