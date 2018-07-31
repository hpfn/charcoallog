from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import resolve_url as r
from django.test import TestCase

from charcoallog.investments.models import InvestmentDetails, BasicData


class InvestmentDetailTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        self.login_in = self.client.login(username='teste', password='1qa2ws3ed')
        b_data = dict(
            user_name='teste',
            date='2018-03-27',
            money=94.42,
            kind='Títulos Públicos',
            which_target='Tesouro Direto',
        )
        b_data = BasicData.objects.create(**b_data)

        self.data = dict(
            segment='Selic 2023',
            tx_or_price=0.01,
            quant=1.00,
            basic_data=b_data
        )

        self.obj = InvestmentDetails.objects.create(**self.data)
        self.resp = self.client.get(r('investments:detail', 'Títulos Públicos'))

    def test_login(self):
        """ Must login to access html file"""
        self.assertTrue(self.login_in)

    def test_get_status_code(self):
        """ Must return status code 200 """
        self.assertEqual(200, self.resp.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'investments/detail.html')

    def test_context_instance(self):
        data = self.resp.context['d']
        self.assertIsInstance(data, QuerySet)

    def test_context(self):
        data = self.resp.context['d']
        for i in data:
            self.assertIn(i.basic_data.kind, 'Títulos Públicos')
            self.assertIn(i.basic_data.which_target, 'Tesouro Direto')
