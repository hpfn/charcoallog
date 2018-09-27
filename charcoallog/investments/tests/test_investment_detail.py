from decimal import Decimal

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import resolve_url as r
from django.test import TestCase

from charcoallog.investments.models import NewInvestmentDetails


class InvestmentDetailTest(TestCase):
    def setUp(self):
        user_n = 'teste'
        user = User.objects.create(username=user_n)
        user.set_password('1qa2ws3ed')
        user.save()

        self.date = '2018-03-27'
        self.money = 94.42
        self.kind = 'Títulos Públicos'
        # self.which_target = 'Tesouro Direto'

        self.login_in = self.client.login(username=user_n, password='1qa2ws3ed')

        self.which_target = 'Tesouro Direto'
        self.segment = 'Selic'
        self.tx_or_price = 0.01
        self.quant = 1.00

        self.data = dict(
            user_name=user_n,
            date=self.date,
            money=self.money,
            kind=self.kind,
            which_target=self.which_target,
            segment=self.segment,
            tx_or_price=self.tx_or_price,
            quant=self.quant,
        )

        self.obj = NewInvestmentDetails.objects.create(**self.data)
        self.resp = self.client.get(r('investments:detail', 'Títulos Públicos'))

    def test_login(self):
        """ Must login to access html file"""
        self.assertTrue(self.login_in)

    def test_get_status_code(self):
        """ Must return status code 200 """
        self.assertEqual(200, self.resp.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'investments/detail.html')

    def test_html(self):
        """
        Must contain input tags
        vue template does not count
        """
        expected = [
            ('<form', 2),
            ('<input', 4),
            ("type='hidden'", 1),
            ('type="text"', 1),
            # ('type="number"', 2),
            # ('step="0.01"', 1),
            ('type="date"', 2),
            ('type="submit"', 1),
            ('</form>', 2),
            ('class="row"', 4),
            ('method="get"', 1),
            # ('method="post"', 1),
            ('id="vue_ajax_detail"', 1),
        ]
        for tag, x in expected:
            with self.subTest():
                self.assertContains(self.resp, tag, x)

    def test_csrf(self):
        """ html must contain csrf """
        self.assertContains(self.resp, 'csrfmiddlewaretoken', 1)

    def test_context_instance(self):
        form3 = self.resp.context['d']
        self.assertIsInstance(form3, QuerySet)

    def test_context(self):
        data = self.resp.context['d']
        expected = [
            (str(data[0].date), self.date),
            (data[0].money, Decimal(str(self.money))),
            (data[0].kind, self.kind),
            (data[0].which_target, self.which_target),
            (data[0].segment, self.segment),
            (data[0].tx_or_price, Decimal(str(self.tx_or_price))),
            (data[0].quant, self.quant)
        ]

        for know, e in expected:
            with self.subTest():
                self.assertEqual(know, e)
