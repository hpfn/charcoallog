from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase


class RedirectOKTest(TestCase):
    def test_redirect_to_login(self):
        data = dict(username='blablabla',
                    password1='1qa2ws3ed',
                    password2='1qa2ws3ed',
                    email='blablabla@teste.com')
        resp_post = self.client.post(r('accounts:register'), data)
        self.assertRedirects(resp_post, r('accounts:login'))


class RedirectFailTest(TestCase):
    def test_no_redirect_to_login(self):
        """
        Register fails, in this case the user already exists.
        Do not redirect.
        """
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        data = dict(username='teste',
                    password1='1qa2ws3ed',
                    password2='1qa2ws3ed',
                    email='blablabla@teste.com')
        resp_post = self.client.post(r('accounts:register'), data)
        self.assertEqual(200, resp_post.status_code)
