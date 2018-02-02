from urllib import request

from bs4 import BeautifulSoup


class Scrap:
    def __init__(self):
        self.html_doc = request.urlopen('http://www.portalbrasil.net/indices_selic.htm')
        self.soup = BeautifulSoup(self.html_doc, 'html.parser')
        table = self.soup.find_all("div", align="center")
        self.tabela = table[3]
        # tables.remove('table')
        # print(tables.count('table'))


