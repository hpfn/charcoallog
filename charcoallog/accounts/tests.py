from django.test import TestCase, Client


class HomeFailTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_fail_response(self):
        self.assertEqual(302, self.response.status_code)


class RedirectToLogin(TestCase):
    def setUp(self):
        self.c = Client()
        self.response = self.c.get('/', follow=True)

    # def test_loginfail(self):
    #    self.assertFalse(self.c.login(username='teste', password='1qa2ws3ed'))

    def test_redirect(self):
        self.assertTemplateUsed(self.response, 'accounts/login.html')
