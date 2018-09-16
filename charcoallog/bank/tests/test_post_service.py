from decimal import Decimal

from django.test import TestCase

from charcoallog.bank.forms import EditExtractForm
from charcoallog.bank.models import Extract, Schedule
from charcoallog.bank.post_service import MethodPost


class RQST:
    pass


class ValidPostMethod(TestCase):
    def setUp(self):
        self.user = 'teste'
        self.data = dict(
            # user_name='you',
            date='2017-12-21',
            money=10.00,
            description='test',
            category='test',
            payment='principal',
            # update_rm='',
            # pk=''
        )

        self.query_user = Extract.objects.user_logged(self.user)
        RQST.method = 'POST'
        RQST.POST = self.data
        RQST.user = self.user
        self.response = MethodPost(RQST, self.query_user)

    def test_editextractform_instance(self):
        """
            editextractform attr must be a EditExtractForm instance.
        """
        self.assertIsInstance(self.response.editextractform(), EditExtractForm)

    def test_form_is_valid(self):
        self.assertTrue(self.response.form.is_valid())

    def test_form_save(self):
        select_data = Extract.objects.get(id=1)
        select_dict = dict(
            user_name=select_data.user_name,
            date=select_data.date.strftime('%Y-%m-%d'),
            money=Decimal(select_data.money),
            description=select_data.description,
            category=select_data.category,
            payment=select_data.payment,
            # update_rm='',
            # pk=''
        )
        self.data['user_name'] = self.user
        self.assertDictEqual(self.data, select_dict)


class TransferBetweenAccounts(TestCase):
    def setUp(self):
        self.user = 'teste'
        self.account_1 = 'principal'
        self.account_2 = 'cartao credito'
        self.value = '-10.00'
        self.value_after_transfer = '10.00'
        self.data = dict(
            # user_name=self.user,
            date='2017-12-21',
            money=self.value,
            description=self.account_2,
            category='transfer',
            payment=self.account_1,
        )

        self.query_user = Extract.objects.user_logged(self.user)
        RQST.method = "POST"
        RQST.POST = self.data
        RQST.user = self.user
        self.response = MethodPost(RQST, self.query_user)

    def test_negative_transfer_name(self):
        p_data = self.query_user.get(id=1)
        self.assertEqual(p_data.payment, self.account_1)

    def test_negative_transfer_value(self):
        p_data = self.query_user.get(id=1)
        self.assertEqual(p_data.money, Decimal(self.value))

    def test_positive_transfer_name(self):
        c_c_data = self.query_user.get(id=2)
        self.assertEqual(c_c_data.payment, self.account_2)

    def test_positive_transfer_value(self):
        c_c_data = self.query_user.get(id=2)
        self.assertEqual(c_c_data.money, Decimal(self.value_after_transfer))


class ScheduleTest(TestCase):
    def setUp(self):
        self.user = 'teste'
        self.value = '-10.00'
        self.data = dict(
            date='2018-09-01',
            money='100.00',
            description='shedule',
            category='test',
            payment='principal',
            schedule=True,
        )

        self.query_user = Extract.objects.user_logged(self.user)
        RQST.method = "POST"
        RQST.POST = self.data
        RQST.user = self.user
        self.response = MethodPost(RQST, self.query_user)

    def test_record_in_models(self):
        # self.assertTrue(Extract.objects.get(id=1))
        extract_record = Extract.objects.all().count()
        shedule_record = Schedule.objects.filter(user_name=self.user).count()
        expected = [
            (extract_record, 0),
            (shedule_record, 1)
        ]

        for r, x in expected:
            with self.subTest():
                self.assertEqual(r, x)
        # self.assertEqual(s, 1)


class TransferScheduleTest(TestCase):
    def setUp(self):
        self.user = 'teste'
        self.account_1 = 'principal'
        self.account_2 = 'cartao credito'
        self.value = '-10.00'
        self.value_after_transfer = '10.00'
        self.data = dict(
            # user_name=self.user,
            date='2017-12-21',
            money=self.value,
            description=self.account_2,
            category='transfer',
            payment=self.account_1,
            schedule=True
        )
        self.query_user = Extract.objects.user_logged(self.user)
        RQST.method = "POST"
        RQST.POST = self.data
        RQST.user = self.user
        self.response = MethodPost(RQST, self.query_user)

    def test_no_extract_record(self):
        n_record = Extract.objects.all().count()
        self.assertEqual(n_record, 0)

    def test_records_in_schedule(self):
        n_record = Schedule.objects.all().count()
        self.assertEqual(n_record, 2)
