from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase


class LoginFormTest(TestCase):
    def setUp(self):
        self.form = AuthenticationForm()

    def test_form_has_fields(self):
        """ Form must have two fields """
        expected = ['username', 'password']
        self.assertSequenceEqual(expected, list(self.form.fields))
