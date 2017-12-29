from django.contrib.auth.models import User
from django.test import TestCase

from charcoallog.core.models import Extract


class AjaxPostTest(TestCase):
    def setUp(self):
        self.data = dict(
            user_name='teste',
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment='principal'
        )
        Extract.objects.create(**self.data)

        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        self.login_in = self.client.login(username='teste', password='1qa2ws3ed')

    def test_login(self):
        self.assertTrue(self.login_in)

    def test_post(self):
        """
           GET method must return 405
           method not allowed
        """
        self.assertEqual(405, self.client.get('/ajax_post/').status_code)

    def test_ajax_remove(self):
        self.data['update_rm'] = 'remove'
        self.data['pk'] = ''
        self.client.post('/ajax_post/', self.data)
        no_data = Extract.objects.filter(id=1).first()
        self.assertFalse(no_data)

    def test_ajax_update(self):
        self.data['payment'] = 'cartao credito'
        self.data['update_rm'] = 'update'
        self.data['pk'] = 1
        self.client.post('/ajax_post/', self.data)
        data = Extract.objects.get(id=1)
        self.assertEqual(data.payment, 'cartao credito')

    def test_json_response(self):
        self.data['payment'] = 'cartao credito'
        self.data['money'] = -10.00
        self.data['update_rm'] = 'update'
        self.data['pk'] = 1
        response = self.client.post('/ajax_post/', self.data)

        self.assertJSONEqual(
             response.content,
             {'accounts': {'cartao credito': {'money__sum': '-10.00'}},
              'whats_left': '-10.00'}
        )
