from urllib import request

from bs4 import BeautifulSoup


class Scrap:
    def __init__(self):
        self.html_doc = request.urlopen('https://www.bcb.gov.br/Pec/Copom/Port/taxaSelic.asp')
        self.soup = BeautifulSoup(self.html_doc, 'html.parser')
        tabela = self.soup.find_all("td", class_="centralizado")
        lst_tabela = []
        for x, i in enumerate(tabela):
            if '2017' in str(i):
                celula = i.string + ' = ' + tabela[x+1].string
                lst_tabela.append(celula)
        self.tabela = lst_tabela

        # tables.remove('table')
        # print(tables.count('table'))


