from django.test import TestCase

from charcoallog.investments.detail_post_service import DetailPost
from charcoallog.investments.forms import BasicDataForm, InvestmentDetailsForm
from charcoallog.investments.models import BasicData, InvestmentDetails


class RQST:
    pass


class DetailPostTest(TestCase):
    def setUp(self):
        self.post_data = dict(
            user_name='you',
            date='2018-09-21',
            money=1000.00,
            kind='NO',
            which_target='NO P',
            segment='NO S',
            tx_or_price=0.00,
            quant=0.00
        )
        RQST.POST = self.post_data
        RQST.method = 'POST'
        RQST.user = 'teste'

        self.c = DetailPost(RQST)

    def test_attr(self):
        expected = [
            'request',
            'i_detail',
            'basic_data',
            'insert_data'
        ]

        for e in expected:
            with self.subTest():
                self.assertTrue(hasattr(self.c, e))

    def test_i_detail_instance(self):
        """
        i_detail attr must be a InvestmentDetailForm instance.
        """
        self.assertIsInstance(self.c.i_detail(), InvestmentDetailsForm)

    def test_basicdata_instance(self):
        """
        basic_data attr must be a BasicDataForm instance.
        """
        self.assertIsInstance(self.c.basic_data(), BasicDataForm)

    def test_valid_form(self):
        expected = [
            self.c.i_d_form.is_valid(),
            self.c.b_d_form.is_valid()
        ]

        for e in expected:
            with self.subTest():
                self.assertTrue(e)

    def test_basic_data_db(self):
        qs = BasicData.objects.get(pk=1)

        expected = [
            (qs.user_name, 'teste'),
            (str(qs.date), self.post_data['date']),
            (qs.money, self.post_data['money']),
            (qs.kind, self.post_data['kind'])
        ]

        for q, e in expected:
            with self.subTest():
                self.assertEqual(q, e)

    def test_investment_detail_db(self):
        qs = InvestmentDetails.objects.get(pk=1)

        expected = [
            (qs.which_target, self.post_data['which_target']),
            (qs.segment, self.post_data['segment']),
            (qs.tx_or_price, self.post_data['tx_or_price']),
            (qs.quant, self.post_data['quant'])
        ]

        for q, e in expected:
            with self.subTest():
                self.assertEqual(q, e)
