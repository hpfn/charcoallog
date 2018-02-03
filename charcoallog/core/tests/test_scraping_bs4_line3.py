from bs4 import BeautifulSoup
from django.test import TestCase
from charcoallog.core.scrap_line3_service import Scrap


class ScrapTest(TestCase):
    def test_selic_info_type(self):
        context = Scrap()
        self.assertIsInstance(context.selic_info(), type(list()))

    def test_ibov_info_type(self):
        context = Scrap()
        self.assertIsInstance(context.ibov_info(), type(dict()))
