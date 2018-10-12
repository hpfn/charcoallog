from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from charcoallog.investments.forms import InvestmentDetailsForm
from charcoallog.investments.service import ShowData


class InvestmentHomeOkTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        self.login_in = self.client.login(username='teste', password='1qa2ws3ed')
        self.response = self.client.get(r('investments:home'))

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
        expected = [
            ('<form', 2),
            ('<input', 14),
            ("type='hidden'", 1),
            ('type="text"', 5),
            ('type="checkbox"', 1),
            ('<template', 1),
            ('</template>', 1),
            ('type="number"', 4),
            ('step="0.01"', 4),
            ('type="date"', 3),
            ('type="submit"', 2),
            ('</form', 2),
            ('class="row"', 4),
            ('method="get"', 1),
            ('method="post"', 1)
        ]
        for tag, x in expected:
            with self.subTest():
                self.assertContains(self.response, tag, x)

    def test_csrf(self):
        """ html must contain csrf """
        self.assertContains(self.response, 'csrfmiddlewaretoken', 1)

    def test_has_form(self):
        """ Context must have Investment form """
        form = self.response.context['form']
        self.assertIsInstance(form, InvestmentDetailsForm)

    def test_show_data(self):
        data = self.response.context['show_data']
        self.assertIsInstance(data, ShowData)
