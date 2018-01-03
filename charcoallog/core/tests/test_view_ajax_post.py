from django.contrib.auth.models import User
from django.test import TestCase

from charcoallog.core.models import Extract


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
        self.assertEqual(405, self.client.get('/ajax_post/').status_code)

    def test_ajax_update(self):
        to_update = dict(
            user_name='teste',
            date='2017-12-21',
            money='30.00',
            description='test',
            category='test',
            payment='principal',
            update_rm='update',
            pk=2
        )
        response = self.client.post('/ajax_post/', to_update)
        self.assertJSONEqual(
            response.content,
            {'accounts': {'principal': {'money__sum': '40.00'}},
            'whats_left': '40.00'}
        )

    def test_ajax_remove(self):
        self.data['update_rm'] = 'remove'
        self.data['pk'] = ''
        response = self.client.post('/ajax_post/', self.data)
        self.assertJSONEqual(
            response.content,
            {'accounts': {'cartao credito': {'money__sum': '10.00'}},
            'whats_left': '10.00'}
        )

    def test_ajax_fail_update(self):
        self.data['payment'] = 'blablabla'
        self.data['update_rm'] = 'update'
        self.data['pk'] = ''
        response = self.client.post('/ajax_post/', self.data)
        self.assertJSONEqual(
            response.content,
            {'no_account': True,
            'message': 'You can not set a new account name from here'}
        )