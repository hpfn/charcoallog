from django.contrib.auth.models import User
from django.test import TestCase

from charcoallog.core.models import Extract


class HomeAfterPostTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        data = dict(user_name='teste',
                    date='2017-12-22',
                    money='1000.00',
                    description='test',
                    category='test',
                    payment='principal'
                    )

        Extract.objects.create(**data)
        self.login_in = self.client.login(username='teste', password='1qa2ws3ed')
        self.response = self.client.get('/')

    def test_html_forms_after_insert_data(self):
        """" Html must contain input tags after a POST """
        tags = (
            ('<form', 3),
            ('<input', 19),
            ('<select', 6),
            ('type="text"', 5),
            ('type="number"', 1),
            ('type="radio"', 2),
            ('<button', 3),
            ('type=\'submit\'', 3)
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)
