from django.test import TestCase

from ..forms import RegisterForm


class RegisterPageTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/conta/cadastre-se/')

    def test_status_code(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
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
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """ Context must have register form """
        form = self.response.context['form']
        self.assertIsInstance(form, RegisterForm)

    def test_form_has_fields(self):
        """ Form must have two fields """
        form = self.response.context['form']
        self.assertSequenceEqual(['username', 'password1', 'password2', 'email'], list(form.fields))
