import re
from urllib import request
from urllib.error import HTTPError

from bs4 import BeautifulSoup


class Scrap:
    def __init__(self):
        self.selic_address = 'https://www.bcb.gov.br/Pec/Copom/Port/taxaSelic.asp'
        self.ibov_address = 'https://br.advfn.com/bolsa-de-valores/bovespa/ibovespa-IBOV/historico'
        self.ipca_address = 'http://www.indiceseindicadores.com.br/ipca/'

    def selic_info(self):
        html_doc = request.urlopen(self.selic_address)
        soup = BeautifulSoup(html_doc, 'html.parser')
        tabela = soup.find_all("td", class_="centralizado")
        lst_tabela = []
        for x, i in enumerate(tabela):
            if '2017' in str(i):
                celula = i.string + ' = ' + tabela[x+1].string
                lst_tabela.append(celula)

        return lst_tabela

    def ibov_info(self):
        try:
            hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
             'Accept-Encoding': 'none',
             'Accept-Language': 'en-US,en;q=0.8',
             'Connection': 'keep-alive'}
            req = request.Request(self.ibov_address, headers=hdr)
            html_doc = request.urlopen(req)
            soup = BeautifulSoup(html_doc, 'html.parser')
            tabela_hdr = soup.find_all("th", class_=re.compile("Column(1|2|10).?(ColumnLast)? (String|Numeric)"))
            column1 = soup.find_all("td", class_="String Column1")
            column2 = soup.find_all("td", class_="Numeric Column2")
            column3 = soup.find_all("td", class_="Numeric Column10 ColumnLast")

            # head_th = ''
            # for i in tabela_hdr:
            #     head_th += i.string
            #     head_th += ' '
            head_dict = {}
            head_dict['Periodo'] = ['Abertura', 'Percentual']
            for col1, col2, col3 in zip(column1, column2, column3):
                head_dict[col1.string] = [col2.string, col3.string]

            return head_dict
        except HTTPError:
            return ['http error']

    def ipca_info(self):
        html_doc = request.urlopen(self.ipca_address)
        soup = BeautifulSoup(html_doc, 'html.parser')
        # tabela_hdr = soup.find("thead")
        # rm_tag = re.compile('<t(h|d).*;">(<strong>)?')
        # letters = re.compile('[A-Z][a-z][a-z]')
        # lttr = re.findall(letters, str(tabela_hdr))
        # lttr.pop()
        # print(lttr)

        tabela_bd = soup.find("tbody")
        ano = re.compile(r'<strong>\b(?P<ano>[0-9]{4})\b</strong>')
        get_ano = re.findall(ano, str(tabela_bd))
        # get_ano = [x for x in get_ano]

        # taxas = re.compile(r'\b(?P<indice>[0-9]{,2},[0-9]{2})\b')
        # taxas = re.compile(r'\b(?P<ano>[0-9,]{4,5})\b')
        taxas = re.compile(r'<(strong|b)>\b(?P<indice>[0-9]{,2},[0-9]{2})\b</(strong|b)>')
        get_tx = re.findall(taxas, str(tabela_bd))
        get_tx = [i[1].replace(',', '.') for i in get_tx]
        # get_tx = [i.replace(',', '.') for i in get_tx]
        get_tx = [i for i in get_tx if float(i) > 0.85]

        tx_ano_dict = {}
        for ano, tx in zip(get_ano[:10], get_tx[:10]):
            tx_ano_dict[ano] = tx

        print(get_ano[:10])
        print(get_tx[:10])
        
        return tx_ano_dict