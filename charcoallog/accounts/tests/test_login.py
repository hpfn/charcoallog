from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase


class LoginPageTest(TestCase):
    """ Using Django login, but testing anyway
        success login test is done in core/tests
    """
    def setUp(self):
        self.response = self.client.get('/', follow=True)

    def test_login_fail(self):
        """ Login should be false. We did not make a login """
        self.assertFalse(self.client.login(username='teste', password='1qa2ws3ed'))

    def test_status_code(self):
        """ Must return status code 200 """
        self.assertEqual(200, self.response.status_code)

    def test_follow_true(self):
        """ Template should be accounts/login.html """
        self.assertTemplateUsed(self.response, 'accounts/login.html')

    def test_html_login_form(self):
        """ Html must contain input tags """
        tags = (
            ('<form', 1),
            ('<input', 3),
            ('type="text"', 1),
            ('type="password"', 1),
            ('<button', 1),
            ('type="submit"', 1)
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """ Context must have register form """
        form = self.response.context['form']
        self.assertIsInstance(form, AuthenticationForm)

