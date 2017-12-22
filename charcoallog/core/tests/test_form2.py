from django.test import TestCase

from charcoallog.core.forms import SelectExtractForm


class Form2Test(TestCase):
    def setUp(self):
        self.form2 = SelectExtractForm()

    def test_form1_has_fields(self):
        expected = ['column', 'from_date', 'to_date']
        self.assertSequenceEqual(expected, list(self.form2.fields))
