from django.test import TestCase

from charcoallog.bank.models import Extract
from charcoallog.investments.models import (
    BasicData, Investment, InvestmentDetails
)


class InvestmentModelTest(TestCase):
    """ M3A03 - WTTD """

    def setUp(self):
        self.data_b = dict(
            user_name='teste',
            date='2018-03-27',
            money=94.42,
            kind='Títulos Públicos',
            # which_target='Tesouro Direto',
        )
        b_data = BasicData.objects.create(**self.data_b)

        self.data_i = dict(
            tx_op=00.00,
            brokerage='Ativa',
            basic_data=b_data
        )
        Investment.objects.create(**self.data_i)

    def test_investments_exists(self):
        """ Test if investment is created"""
        self.assertTrue(Investment.objects.exists())

    def test_investment_details_exists(self):
        """ Test if details is created """
        self.assertTrue(InvestmentDetails.objects.exists())

    def test_created_fields_in_details(self):
        qs = InvestmentDetails.objects.get(pk=2)
        self.assertEqual(qs.which_target, '---')
        self.assertEqual(qs.segment, '---')

    def test_update_investment_details(self):
        """ Test if created details object can be updated """
        obj = InvestmentDetails.objects.select_related('basic_data').get()
        obj.which_target = 'tesouro'
        obj.segment = 'Selic 2023'
        obj.tx_or_price = 0.01
        obj.quant = 1.00
        obj.save(update_fields=['which_target', 'segment', 'tx_or_price', 'quant'])
        segment_update = InvestmentDetails.objects
        segment_update.select_related('basic_data')
        segment_update.filter(segment='Selic 2023')

        self.assertTrue(segment_update.exists())

    def test_delete_data(self):
        """
        If delete a record in Investment
        Must delete that record in Details too
        """
        Investment.objects.get(pk=1).delete()

        expected = [
            Investment.objects.exists(),
            InvestmentDetails.objects.exists()
        ]
        for x in expected:
            with self.subTest():
                self.assertFalse(x)


class DataFromBankTest(TestCase):
    def setUp(self):
        self.user = 'teste'
        self.data = dict(
            user_name='you',
            date='2018-04-20',
            money=10.00,
            description='Ativa',
            category='investments',
            payment='principal',
        )
        Extract.objects.create(**self.data)

    def test_data_in_investments(self):
        ativa = Investment.objects.select_related('basic_data')
        ativa.filter(brokerage='Ativa')
        self.assertTrue(ativa.exists())

    def test_data_not_in_investmentdetails(self):
        kind = InvestmentDetails.objects.select_related('basic_data')
        kind.filter(basic_data__kind='---')
        self.assertFalse(kind.exists())

    def test_bank_enty_delete(self):
        """ Delete Bank entry, delete Investment entry too """
        Extract.objects.get(pk=1).delete()
        qs = Investment.objects.all().count()
        self.assertEqual(0, qs)
