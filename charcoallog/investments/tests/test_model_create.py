from decimal import Decimal

from django.test import TestCase

from charcoallog.bank.models import Extract
from charcoallog.investments.models import NewInvestment, NewInvestmentDetails


class InvestmentModelTest(TestCase):
    """ Create and delete data in NewInvestments"""

    def setUp(self):
        self.user = 'teste'

        self.data_i = dict(
            user_name=self.user,
            date='2018-03-27',
            money=94.42,
            kind='Títulos Públicos',
            tx_op=00.00,
            brokerage='A',
        )
        NewInvestment.objects.create(**self.data_i)

    def test_investments_exists(self):
        """ Test if investment is created"""
        self.assertTrue(NewInvestment.objects.exists())

    def test_each_field(self):
        qs = NewInvestment.objects.get(pk=1)

        expected = [
            (qs.user_name, 'teste'),
            (str(qs.date), '2018-03-27'),
            (qs.money, Decimal('94.42')),
            (qs.kind, 'Títulos Públicos'),
            (qs.tx_op, Decimal('00.00')),
            (qs.brokerage, 'A'),
            (str(qs), 'A')
        ]

        for q, e in expected:
            with self.subTest():
                self.assertEqual(q, e)

    def test_delete_data(self):
        """
        delete a record in Investment
        """
        NewInvestment.objects.get(pk=1).delete()
        self.assertFalse(NewInvestment.objects.exists())


class DataFromBankTest(TestCase):
    def setUp(self):
        self.user = 'you'
        self.data = dict(
            user_name=self.user,
            date='2018-04-20',
            money=10.00,
            description='A',
            category='investments',
            payment='principal',
        )
        Extract.objects.create(**self.data)

    def test_data_in_investments(self):
        brkrg = NewInvestment.objects.user_logged('you').filter(brokerage='A')
        self.assertTrue(brkrg.exists())

    def test_bank_enty_delete(self):
        """ Delete Bank entry, delete Investment entry too """
        Extract.objects.get(pk=1).delete()
        qs = NewInvestment.objects.all().count()
        self.assertEqual(0, qs)


class InvestmentDetails(TestCase):
    def setUp(self):
        data = dict(
            user_name='teste',
            date='2018-03-27',
            money=94.42,
            kind='Títulos Públicos',
            tx_op=00.00,
            brokerage='A',
            which_target='LFT',
            segment='selic 2023',
            tx_or_price=00.00,
            quant=00.00
        )
        NewInvestmentDetails.objects.create(**data)

    def test_investment_details_exists(self):
        """ Test if details is created """
        self.assertTrue(NewInvestmentDetails.objects.exists())

    def test_same_pk(self):
        i = NewInvestment.objects.get(pk=1)
        d = NewInvestmentDetails.objects.get(pk=1)
        self.assertEqual(i.kind, d.kind)

    def test_details_dunder_str(self):
        qs = NewInvestmentDetails.objects.get(pk=1)
        self.assertEqual(str(qs), 'LFT')
