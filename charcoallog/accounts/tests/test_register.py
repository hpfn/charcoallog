from django.test import TestCase, Client
from django.contrib.auth.forms import AuthenticationForm

from ..forms import RegisterForm


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
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="password"', 2)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, '<button', 1)
        self.assertContains(self.response, 'type="submit"', 1)

    def test_csrf(self):
        """ must have csrf token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """ Context must have register form """
        form = self.response.context['form']
        self.assertIsInstance(form, RegisterForm)

    def test_form_has_fields(self):
        """ Form must have two fields """
        form = self.response.context['form']
        self.assertSequenceEqual(['username', 'password1', 'password2', 'email'], list(form.fields))


class RedirectTest(TestCase):
    def test_redirect_to_login(self):
        data = dict(username='blablabla',
                    password1='1qa2ws3ed',
                    password2='1qa2ws3ed',
                    email='blablabla@teste.com')
        resp_post = self.client.post('/conta/cadastre-se/', data)
        self.assertRedirects(resp_post, '/conta/entrar/')


