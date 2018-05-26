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
        # to pass update test
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

    def test_login(self):
        self.assertTrue(self.login_in)

    def test_post(self):
        """
           GET method must return 405
           method not allowed
        """
        self.assertEqual(405, self.client.get(r('bank:update')).status_code)

    def test_ajax_update(self):
        to_update = dict(
            # user_name='teste',
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment='principal',
            # update_rm='update',
            pk=2
        )
        response = self.client.post(r('bank:update'), to_update, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(
            response.content,
            {'accounts': {'principal': {'money__sum': '20.00'}},
             'whats_left': '20.00'}
        )

    def test_ajax_fail_update(self):
        self.data['payment'] = 'blablabla'
        # self.data['update_rm'] = 'update'
        self.data['pk'] = ''
        response = self.client.post(r('bank:update'), self.data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(
            response.content,
            {'no_account': True,
             'message': 'You can not set a new account name from here'}
        )
