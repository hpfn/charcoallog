from django.test import TestCase

from charcoallog.investments.forms import InvestmentForm


class InvestmentFormTest(TestCase):
    def test_form_has_fields(self):
        """ Form must have 2 fields. The third field is in test_basicdata_form"""
        form = InvestmentForm()
        self.assertSequenceEqual(
            ['tx_op', 'brokerage'],
            list(form.fields)
        )
