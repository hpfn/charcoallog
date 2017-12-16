from django.test import TestCase

from ..forms import RegisterForm


class RegisterFormTest(TestCase):
    def setUp(self):
        self.form = RegisterForm()

    def test_form_has_fields(self):
        """ Form must have 4 fields """
        expected = ['username', 'password1', 'password2', 'email']
        self.assertSequenceEqual(expected, list(self.form.fields))
