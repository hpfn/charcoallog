from django.test import TestCase

from charcoallog.bank.models import Extract
from charcoallog.investments.models import NewInvestment, NewInvestmentDetails


class InvestmentModelTest(TestCase):
    """ M3A03 - WTTD """

    def setUp(self):
        self.user = 'teste'

        self.data_i = dict(
            user_name=self.user,
            date='2018-03-27',
            money=94.42,
            kind='Títulos Públicos',
            tx_op=00.00,
            brokerage='Ativa',
        )
        NewInvestment.objects.create(**self.data_i)

    def test_investments_exists(self):
        """ Test if investment is created"""
        self.assertTrue(NewInvestment.objects.exists())

    def test_investment_details_exists(self):
        """ Test if details is created """
        self.assertTrue(NewInvestmentDetails.objects.exists())

    def test_created_fields_in_details(self):
        qs = NewInvestmentDetails.objects.get(pk=1)
        self.assertEqual(qs.which_target, '---')
        self.assertEqual(qs.segment, '---')

    def test_update_investment_details(self):
        """ Test if created details object can be updated """
        obj = NewInvestmentDetails.objects.user_logged(self.user).get()
        obj.which_target = 'tesouro'
        obj.segment = 'Selic 2023'
        obj.tx_or_price = 0.01
        obj.quant = 1.00
        obj.save(update_fields=['which_target', 'segment', 'tx_or_price', 'quant'])
        segment_update = NewInvestmentDetails.objects.user_logged(self.user)
        segment_update.filter(segment='Selic 2023')

        self.assertTrue(segment_update.exists())

    def test_delete_data(self):
        """
        If delete a record in Investment
        Must delete that record in Details too
        """
        NewInvestment.objects.get(pk=1).delete()

        expected = [
            NewInvestment.objects.exists(),
            NewInvestmentDetails.objects.exists()
        ]
        for x in expected:
            with self.subTest():
                self.assertFalse(x)


class DataFromBankTest(TestCase):
    def setUp(self):
        self.user = 'you'
        self.data = dict(
            user_name=self.user,
            date='2018-04-20',
            money=10.00,
            description='Ativa',
            category='investments',
            payment='principal',
        )
        Extract.objects.create(**self.data)

    def test_data_in_investments(self):
        ativa = NewInvestment.objects.user_logged('you')
        ativa.filter(brokerage='Ativa')
        self.assertTrue(ativa.exists())

    def test_data_not_in_investmentdetails(self):
        kind = NewInvestmentDetails.objects.user_logged(self.user)
        kind.filter(kind='---')
        self.assertFalse(kind.exists())

    def test_bank_enty_delete(self):
        """ Delete Bank entry, delete Investment entry too """
        Extract.objects.get(pk=1).delete()
        qs = NewInvestment.objects.all().count()
        self.assertEqual(0, qs)
