# from bs4 import BeautifulSoup
import os

from django.test import TestCase
from unittest.mock import patch

from charcoallog.core.scrap_line3_service import Scrap


class ScrapTest(TestCase):
    # @patch('os.path.isfile')
    # @patch('charcoallog.core.scrap_line3_service.request')
    # def test_info_type(self, request, check_file):
    #     check_file.return_value = True
    #     context = Scrap()
    #     contents = [
    #         context.selic_info(),
    #         context.ibov_info(),
    #         context.ipca_info(),
    #     ]
    #     for content in contents:
    #         with self.subTest():
    #             self.assertIsInstance(content, type(list()))

    @patch('charcoallog.core.scrap_line3_service.date')
    def test_selic_webscrapping(self, mocked_date):
        r = Scrap()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        selic_file = os.path.join(base_dir, 'tests/selic.html')
        r.selic_address = 'file://' + selic_file

        mocked_date.today.strftime.return_value = '2018'

        expected = [
            ['22/03/2018 - ', '6,50'],
            ['6,50', '\n'],
            ['08/02/2018 - 21/03/2018', '6,75'],
            ['\r\n\t  0,72\r\n\t  ', '\r\n\t  6,65\r\n\r\n\t'],
            ['07/12/2017 - 07/02/2018', '7,00'],
            ['7,00', '\r\n\t  1,15\r\n\t  '],
            ['\r\n\t  6,90\r\n\r\n\t', '26/10/2017 - 06/12/2017'],
            ['26/10/2017 - 06/12/2017', '7,50'],
            ['7,50', '\r\n\t  0,80\r\n\t  '],
            ['\r\n\t  0,80\r\n\t  ', '\r\n\t  7,40\r\n\r\n\t'],
            ['\r\n\t  7,40\r\n\r\n\t', '08/09/2017 - 25/10/2017'],
            ['08/09/2017 - 25/10/2017', '8,25'],
            ['\r\n\t  1,03\r\n\t  ', '\r\n\t  8,15\r\n\r\n\t']
        ]

        self.assertEqual(r.selic_webscrapping(), expected)

    def test_ibov_scrapping(self):
        index = Scrap()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ibov_file = os.path.join(base_dir, 'tests/ibov.html')
        index.ibov_address = 'file://' + ibov_file

        expected = [
            ['Período', ['Abe', '%']],
            ['1 Semana', ['80.123,449', '-3,60%']],
            ['1 Mês', ['83.286,382', '-7,26%']],
            ['3 Meses', ['84.987,154', '-9,12%']],
            ['6 Meses', ['71.955,27', '7,34%']],
            ['1 Ano', ['62.289,195', '24,00%']],
            ['3 Anos', ['53.517,601', '44,33%']],
            ['5 Anos', ['52.876,775', '46,08%']]
        ]

        self.assertEqual(index.ibov_webscrapping(), expected)

    def test_ipca_webscrapping(self):
        tx = Scrap()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ipca_file = os.path.join(base_dir, 'tests/ipca.html')
        tx.ipca_address = 'file://' + ipca_file

        expected = [
            ['2018', '0,92'],
            ['2017', '2,95'],
            ['2016', '6,29'],
            ['2015', '10,67'],
            ['2014', '6,40'],
            ['2013', '5,91'],
            ['2012', '5,83'],
            ['2011', '6,50'],
            ['2010', '5,90'],
            ['2009', '4,31']
        ]

        self.assertEqual(tx.ipca_webscrapping(), expected)
