from django.contrib.auth.models import User
from django.test import TestCase

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

    def test_form_has_fields(self):
        """ Form must have 4 fields """
        form = self.response.context['form']
        self.assertSequenceEqual(['username', 'password1', 'password2', 'email'], list(form.fields))


class RedirectOKTest(TestCase):
    def test_redirect_to_login(self):
        data = dict(username='blablabla',
                    password1='1qa2ws3ed',
                    password2='1qa2ws3ed',
                    email='blablabla@teste.com')
        resp_post = self.client.post('/conta/cadastre-se/', data)
        self.assertRedirects(resp_post, '/conta/entrar/')


class RedirectFailTest(TestCase):
    def test_no_redirect_to_login(self):
        """
        If POST fails, do not redirect. In this case
        the user already exists.
        """
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        data = dict(username='teste',
                    password1='1qa2ws3ed',
                    password2='1qa2ws3ed',
                    email='blablabla@teste.com')
        resp_post = self.client.post('/conta/cadastre-se/', data)
        self.assertEqual(200, resp_post.status_code)