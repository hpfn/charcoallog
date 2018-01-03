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

    def test_ajax_remove(self):
        self.data['update_rm'] = 'remove'
        self.data['pk'] = ''
        self.client.post('/ajax_post/', self.data)
        no_data = Extract.objects.filter(id=1).first()
        self.assertFalse(no_data)

    def test_ajax_update(self):
        to_update = dict(
            user_name='teste',
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment='principal',
            update_rm='update',
            pk=2
        )
        self.client.post('/ajax_post/', to_update)
        data = Extract.objects.user_logged('teste').get(id=2)
        self.assertEqual(data.payment, 'principal')
        # no test if a payment does not already exist
        # do not allow create a account name from an update

    #def test_json_response(self):
    #    self.data['payment'] = 'cartao credito'
    #    self.data['money'] = -10.00
    #    self.data['update_rm'] = 'update'
    #    self.data['pk'] = 1
    #    response = self.client.post('/ajax_post/', self.data)
    #
    #    self.assertJSONEqual(
    #         response.content,
    #         {'accounts': {'cartao credito': {'money__sum': '-10.00'}},
    #          'whats_left': '-10.00'}
    #    )
    #
