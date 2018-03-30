from django.contrib.auth.models import User
from django.test import TestCase
from charcoallog.investments.forms import InvestmentForm

class InvestmentHomeOkTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        self.login_in = self.client.login(username='teste', password='1qa2ws3ed')
        self.response = self.client.get('/investments/')

    def test_login(self):
        """ Must login to access html file"""
        self.assertTrue(self.login_in)

    def test_get_status_code(self):
        """ Must return status code 200 """
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """ Must use 'investments/home.html' """
        self.assertTemplateUsed(self.response, 'investments/home.html')

    def test_html(self):
        """ Must contain input tags """
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 8)
        self.assertContains(self.response, 'type="text"', 4)
        self.assertContains(self.response, 'type="number"', 2)
        self.assertContains(self.response, 'type="submit"')
        self.assertContains(self.response, '</form')

    def test_csrf(self):
        """ html must contain csrf """
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """ Context must have Investment form """
        form = self.response.context['form']
        self.assertIsInstance(form, InvestmentForm)

    def test_form_has_fields(self):
        """ Form must have 6 fields"""
        form = self.response.context['form']
        self.assertSequenceEqual(
            ['date', 'money', 'kind', 'which_target', 'tx_op', 'brokerage'],
            list(form.fields)
        )



