from datetime import date
from decimal import Decimal

from django.test import TestCase

from charcoallog.investments.forms import InvestmentDetailsForm
from charcoallog.investments.models import NewInvestmentDetails


class InvestmentDetailsFormTest(TestCase):
    def test_form_has_fields(self):
        """ Form must have 3 fields. The third field is in test_basicdata_form"""
        form = InvestmentDetailsForm()
        self.assertSequenceEqual(
            ['date', 'money', 'kind', 'tx_op',
             'brokerage', 'which_target', 'segment',
             'tx_or_price', 'quant'],
            list(form.fields)
        )


class InvestmentDetailSave(TestCase):
    def setUp(self):
        data = dict(
            user_name='teste',
            date='2018-09-19',
            money='10.00',
            kind='tesouro',
            tx_op=0.00,
            brokerage='A',
            which_target='selic',
            segment='2023',
            tx_or_price=0.00,
            quant=0.00,
        )
        self.form = InvestmentDetailsForm(data)

    def test_is_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_save(self):
        """
        .save() param must exists. That's why the test.
        """
        self.form.save('teste')

        qs = NewInvestmentDetails.objects.all()
        expected = [
            (qs[0].which_target, 'selic'),
            (qs[0].segment, '2023'),
            (qs[0].tx_or_price, Decimal('0.00')),
            (qs[0].quant, 0.00),
            (qs[0].user_name, 'teste'),
            (qs[0].date, date(2018, 9, 19)),
            (qs[0].money, Decimal('10.00')),
            (qs[0].kind, 'tesouro'),
            (qs[0].tx_op, Decimal('0.00')),
            (qs[0].brokerage, 'A'),
        ]

        for obj, v in expected:
            with self.subTest():
                self.assertEqual(obj, v)
