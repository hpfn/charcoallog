from django.test import TestCase

from charcoallog.bank.models import Extract
from charcoallog.investments.models import NewInvestment, NewInvestmentDetails


class FromInvestToBank(TestCase):
    def setUp(self):
        i_data = dict(
            user_name='teste',
            date='2018-10-01',
            money=-100.00,
            kind='CDB transfer to Bank',
            tx_op=0.00,
            brokerage='Brokerage'
        )
        NewInvestment.objects.create(**i_data)

    def test_newinvest_exists(self):
        self.assertTrue(NewInvestment.objects.exists())

    def test_details_exists(self):
        self.assertTrue(NewInvestmentDetails.objects.exists())

    def test_bank_exists(self):
        self.assertTrue(Extract.objects.exists())

    def test_money_transfer(self):
        detail = NewInvestmentDetails.objects.get(pk=1)
        invest = NewInvestment.objects.get(pk=1)
        bank = Extract.objects.get(pk=1)

        expected = [
            (detail.money, -100.00),
            (detail.kind, 'CDB'),
            (invest.money, -100.00),
            (bank.money, 100.00),
            (bank.description, 'credit from CDB'),
            (bank.payment, 'Bank'),
        ]

        for qs, e in expected:
            with self.subTest():
                self.assertEqual(qs, e)

    def test_delete_invest_delete_detail(self):
        NewInvestment.objects.all().delete()
        self.assertFalse(NewInvestmentDetails.objects.exists())


class DeleteTransferToBank(TestCase):
    def setUp(self):
        i_data = dict(
            user_name='teste',
            date='2018-10-01',
            money=-100.00,
            kind='CDB transfer to Bank',
            tx_op=0.00,
            brokerage='Brokerage'
        )
        NewInvestment.objects.create(**i_data)

    def test_record_exists(self):
        expected = [
            NewInvestment.objects.exists(),
            NewInvestmentDetails.objects.exists(),
            Extract.objects.exists(),
        ]

        for e in expected:
            with self.subTest():
                self.assertTrue(e)

    def test_delete(self):
        NewInvestment.objects.get(pk=1).delete()

        expected = [
            NewInvestment.objects.exists(),
            NewInvestmentDetails.objects.exists(),
            Extract.objects.exists(),
        ]

        for e in expected:
            with self.subTest():
                self.assertFalse(e)
