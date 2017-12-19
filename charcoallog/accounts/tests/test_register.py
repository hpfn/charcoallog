from django.contrib.auth.models import User
from django.test import TestCase

#from ..forms import RegisterForm
from charcoallog.accounts.forms import RegisterForm


class RegisterPageTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/conta/cadastre-se/')

    def test_status_code(self):
        """ status code must be 200 """
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """ Must use accounts/register.html template """
        self.assertTemplateUsed(self.response, 'accounts/register.html')

    def test_html_register_form(self):
        """" Html must contain input tags """
        tags = (
            ('<form', 1),
            ('<input', 5),
            ('type="text"', 1),
            ('type="password"', 2),
            ('type="email"', 1),
            ('<button', 1),
            ('type="submit"', 1)
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """ must have csrf token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """ Context must have register form """
        form = self.response.context['form']
        self.assertIsInstance(form, RegisterForm)
