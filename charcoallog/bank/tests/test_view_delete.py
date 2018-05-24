from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import resolve_url as r

from charcoallog.bank.models import Extract


class AjaxPostTest(TestCase):
    def setUp(self):
        user_name = 'teste'
        self.data = dict(
            user_name=user_name,
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment='principal'
        )
        Extract.objects.create(**self.data)

        # the return after delete
        update_test = dict(
            user_name=user_name,
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment='cartao credito'
        )
        Extract.objects.create(**update_test)

        user = User.objects.create(username=user_name)
        user.set_password('1qa2ws3ed')
        user.save()

        self.login_in = self.client.login(username=user_name, password='1qa2ws3ed')

    def test_login_ok(self):
        self.assertTrue(self.login_in)

    def test_ajax_remove(self):
        obj = Extract.objects.get(**self.data)

        # self.data['update_rm'] = 'remove'
        self.data['pk'] = obj.pk
        # response = self.client.post('/bank/delete/', self.data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.post(r('bank:delete'), self.data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(
            response.content,
            {'accounts': {'cartao credito': {'money__sum': '10.00'}},
             'whats_left': '10.00'}
        )
