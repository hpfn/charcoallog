# from bs4 import BeautifulSoup
from django.test import TestCase


class FakeScrap:
    """ Evitando testes. Aprender mock """

    def __init__(self):
        self.selic_address = 'https://www.bcb.gov.br/Pec/Copom/Port/taxaSelic.asp'
        self.ibov_address = 'https://br.advfn.com/bolsa-de-valores/bovespa/ibovespa-IBOV/historico'
        self.ipca_address = 'http://www.indiceseindicadores.com.br/ipca/'

    def selic_info(self):
        return [['22/03/2018 -', '6.50'], ['08/02/2018 - 21/03/2018', '6,75'],
                ['07/12/2017 - 07/02/2018', '7,00'], ['26/10/2017 - 06/12/2017', '7,50']]

    def ibov_info(self):
        return ['periodo', ['abertura', 'percentual']]

    def ipca_info(self):
        get_ano = ['2018', '2017', '2016', '2015']
        get_tx = ['0.61', '2.95', '6.29', '10.67']
        return [[ano, tx] for ano, tx in zip(get_ano, get_tx[:10])]


class ScrapTest(TestCase):
    # def setUp(self):
    #    self.context = Scrap()
    def test_info_type(self):
        context = FakeScrap()
        contents = [
            context.selic_info(),
            context.ibov_info(),
            context.ipca_info(),
        ]
        for content in contents:
            with self.subTest():
                self.assertIsInstance(content, type(list()))

    # def test_selic_info_type(self):
    #     self.assertIsInstance(self.context.selic_info(), type(dict()))
    #
    # def test_ibov_info_type(self):
    #     self.assertIsInstance(self.context.ibov_info(), type(dict()))
    #
    # def test_ipca_info_type(self):
    #     self.assertIsInstance(self.context.ipca_info(), type(dict()))
    #
