from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import resolve_url as r
from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.core.service import BuildHome


class HomeContextTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        self.login_in = self.client.login(username='teste', password='1qa2ws3ed')
        self.response = self.client.get(r('core:home'))

    def test_status_code(self):
        """ status code must be 200 """
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_html_link(self):
        self.assertContains(self.response, '<a href', 4)

    def test_context_only_instance(self):
        build_home = self.response.context['build_home']
        self.assertIsInstance(build_home, BuildHome)

