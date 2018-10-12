from unittest.mock import patch

from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
# from django.template.response import SimpleTemplateResponse
from django.test import TestCase

# from charcoallog.bank.brief_bank_service import BriefBank
# from charcoallog.bank.models import Extract


class HomeContextTest(TestCase):
    @patch('charcoallog.core.views.BuildHome')
    # @patch('charcoallog.core.service.Scrap')
    def setUp(self, build_home_mock):
        self.build_home = build_home_mock
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        self.login = self.client.login(username='teste', password='1qa2ws3ed')
        self.response = self.client.get(r('core:home'))
        # self.response = home()

    def test_status_code(self):
        """ status code must be 200 """
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/home.html')

    def test_html_link(self):
        self.assertContains(self.response, '<a href', 4)

    def test_context_only_instance(self):
        # build_home = self.response.context_data['build_home']
        # self.assertIsInstance(build_home, BuildHome)
        self.assertEqual(self.build_home.call_count, 1)
