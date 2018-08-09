# from bs4 import BeautifulSoup
import os
from unittest.mock import patch

from django.test import TestCase

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
            ['\n\t  0,72\n\t  ', '\n\t  6,65\n\n\t'],
            ['07/12/2017 - 07/02/2018', '7,00'],
            ['7,00', '\n\t  1,15\n\t  '],
            ['\n\t  6,90\n\n\t', '26/10/2017 - 06/12/2017'],
            ['26/10/2017 - 06/12/2017', '7,50'],
            ['7,50', '\n\t  0,80\n\t  '],
            ['\n\t  0,80\n\t  ', '\n\t  7,40\n\n\t'],
            ['\n\t  7,40\n\n\t', '08/09/2017 - 25/10/2017'],
            ['08/09/2017 - 25/10/2017', '8,25'],
            ['\n\t  1,03\n\t  ', '\n\t  8,15\n\n\t']
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
            'M/A  Mes  Ano  12meses',
            'Jun/2018 1,26 2,6034 4,3910 ',
            'Mai/2018 0,40 1,3267 2,8549 ',
            'Abr/2018 0,22 0,9230 2,7627 ',
            'Mar/2018 0,09 0,7015 2,6807 ',
            'Fev/2018 0,32 0,6109 2,8448 ',
            'Jan/2018 0,29 0,2900 2,8550 ',
        ]

        self.assertEqual(tx.ipca_webscrapping(), expected)
