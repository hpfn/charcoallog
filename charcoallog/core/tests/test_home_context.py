from django.contrib.auth.models import User
from django.test import TestCase

from charcoallog.core.service import ShowData


class HomeContextTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        self.login_in = self.client.login(username='teste', password='1qa2ws3ed')
        self.response = self.client.get('/')

    def test_status_code(self):
        """ status code must be 200 """
        self.assertEqual(200, self.response.status_code)

    def test_context_only_instance(self):
        show_data = self.response.context['show_data']
        self.assertIsInstance(show_data, ShowData)

    def test_logout_link(self):
        self.assertContains(self.response, '<a href', 1)

    def test_html_forms_initial(self):
        """" Html must contain input tags at first time """
        tags = (
            ('<form', 2),
            ('<input', 9),
            ('<select', 6),
            ('type="text"', 5),
            ('type="number"', 1),
            ('<button', 2),
            ('type=\'submit\'', 2)
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """" must have csrf token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken', 2)

    def test_total_line3(self):
        """ Total must be 'Wrong date or invalid search' at first time """
        self.assertContains(self.response, 'Wrong date or invalid search', 1)

    def test_whats_left(self):
        """ Whats left must be zero at first time """
        zero = self.response.context['show_data']
        self.assertEqual(zero.whats_left, 0)

    def test_bottom_id(self):
        self.assertContains(self.response, '<b>charcoallog released under GPL-3+</b>')
