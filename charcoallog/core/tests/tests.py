from django.test import TestCase, Client
from django.contrib.auth.models import User


class HomeFailTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_fail_response(self):
        self.assertEqual(302, self.response.status_code)


class HomeOKTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()
        self.c = Client()
        self.login_in = self.c.login(username='teste', password='1qa2ws3ed')
        self.response = self.c.get('/')

    def test_login(self):
        self.assertTrue(self.login_in)

    def test_get_root(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'home.html')
