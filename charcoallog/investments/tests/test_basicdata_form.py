from django.test import TestCase

from charcoallog.investments.forms import BasicDataForm


class BasicDataTest(TestCase):
    def test_form_has_fields(self):
        """ Form must have 4 fields"""
        basic_data = BasicDataForm()
        self.assertSequenceEqual(
            ['date', 'money', 'kind', 'which_target'],
            list(basic_data.fields)
            )
