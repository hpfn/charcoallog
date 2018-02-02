from bs4 import BeautifulSoup
from django.test import TestCase
from charcoallog.core.scrap_line3_service import Scrap


class ScrapTest(TestCase):
    def test_bs4_instance(self):
        context = Scrap()
        self.assertIsInstance(context.soup, BeautifulSoup)