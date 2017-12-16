from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase, Client


class RedirectToLoginTest(TestCase):
    """ Using Django login, but testing anyway """
    def setUp(self):
        self.c = Client()
        self.response = self.c.get('/', follow=True)

    def test_login_fail(self):
        """ Login should be false. We did not make a login """
        self.assertFalse(self.c.login(username='teste', password='1qa2ws3ed'))

    def test_status_code(self):
        """ Must return status code 200 """
        self.assertEqual(200, self.response.status_code)

    def test_redirect(self):
        """ Template should be accounts/login.html """
        self.assertTemplateUsed(self.response, 'accounts/login.html')

    def test_html_login_form(self):
        """ Html must contain input tags """
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="password"', 1)
        self.assertContains(self.response, '<button', 1)
        self.assertContains(self.response, 'type="submit"', 1)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """ Context must have register form """
        form = self.response.context['form']
        self.assertIsInstance(form, AuthenticationForm)

    def test_form_has_fields(self):
        """ Form must have two fields """
        form = self.response.context['form']
        self.assertSequenceEqual(['username', 'password'], list(form.fields))
