from decimal import Decimal
from django.test import TestCase

from charcoallog.core.line1_service import Line1
from charcoallog.core.models import Extract


class Line1Test(TestCase):
    def setUp(self):
        user_name = 'teste'
        self.account_name = 'principal'
        data = dict(
            user_name=user_name,
            date='2017-12-21',
            money='10.00',
            description='test',
            category='test',
            payment=self.account_name
        )

        Extract.objects.create(**data)
        query_user = Extract.objects.user_logged(user_name)
        self.response = Line1(query_user)
        self.line1_account_name = self.response.account_names()

    def test_line1_account_names(self):
        self.assertIn(self.account_name, self.line1_account_name)

    def test_line1_whats_left(self):
        """
            whats_left attribute must be 10 for user teste
            line1.account_names must be called before whats_left
            (account_values)
        """
        self.assertEqual(self.response.whats_left(), Decimal('10.00'))
