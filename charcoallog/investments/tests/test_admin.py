from django.test import TestCase

from charcoallog.investments import admin


class AdminTest(TestCase):
    def setUp(self):
        self.mod = admin

    def test_attr(self):
        expected = [
            hasattr(self.mod, 'NewInvestment'),
            hasattr(self.mod, 'NewInvestmentDetails'),
            hasattr(self.mod.NewInvestmentModelAdmin, 'list_display'),
            hasattr(self.mod.NewInvestmentDetailsModelAdmin, 'list_display'),
            hasattr(self.mod.NewInvestmentModelAdmin, 'readonly_fields'),
            hasattr(self.mod.NewInvestmentDetailsModelAdmin, 'readonly_fields'),
            hasattr(self.mod.NewInvestmentModelAdmin, 'search_fields'),
            hasattr(self.mod.NewInvestmentDetailsModelAdmin, 'search_fields'),
            hasattr(self.mod.NewInvestmentModelAdmin, 'date_hierarchy'),
            hasattr(self.mod.NewInvestmentDetailsModelAdmin, 'date_hierarchy'),
            hasattr(self.mod.NewInvestmentModelAdmin, 'get_queryset'),
        ]

        for e in expected:
            with self.subTest():
                self.assertTrue(e)
