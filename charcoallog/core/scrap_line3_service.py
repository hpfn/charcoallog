import json
import os
import re
from datetime import date
from urllib import request
from urllib.error import HTTPError

from bs4 import BeautifulSoup


class Scrap:
    def __init__(self):
        self.selic_address = 'https://www.bcb.gov.br/Pec/Copom/Port/taxaSelic.asp'
        self.ibov_address = 'https://br.advfn.com/bolsa-de-valores/bovespa/ibovespa-IBOV/historico'
        self.ipca_address = 'http://www.portalbrasil.net/ipca.htm'

    def selic_info(self):
        if os.path.isfile('./charcoallog/core/selic.json'):
            with open('./charcoallog/core/selic.json', 'r') as selic:
                selic = json.load(selic)

            return selic['selic']

        return self.selic_webscrapping()

    def ibov_info(self):
        if os.path.isfile('./charcoallog/core/ibov.json'):
            with open('./charcoallog/core/ibov.json', 'r') as ibov:
                ibov = json.load(ibov)

            return ibov['ibov']

        return self.ibov_webscrapping()

    def ipca_info(self):
        if os.path.isfile('./charcoallog/core/ipca.json'):
            with open('./charcoallog/core/ipca.json', 'r') as ipca:
                ipca = json.load(ipca)

            return ipca['ipca']

        return self.ipca_webscrapping()

    def selic_webscrapping(self):
        # data = date.today()
        this_year = date.today().strftime("%Y")
        last_year = str(int(this_year) - 1)

        html_doc = request.urlopen(self.selic_address)
        soup = BeautifulSoup(html_doc, 'html.parser')
        tabela = soup.find_all("td", class_="centralizado")

        tabela_dict = [[i.string, tabela[x + 1].string]
                       for x, i in enumerate(tabela)
                       if str(last_year) in i.string or str(this_year) in i.string]

        return tabela_dict

    def ibov_webscrapping(self):
        try:
            hdr = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                              'AppleWebKit/537.11 (KHTML, like Gecko) '
                              'Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                # 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                # 'Accept-Encoding': 'none',
                # 'Accept-Language': 'en-US,en;q=0.8',
                # 'Connection': 'keep-alive'
            }

            req = request.Request(self.ibov_address, headers=hdr)
            html_doc = request.urlopen(req)
            soup = BeautifulSoup(html_doc, 'html.parser')
            tabela_hdr = soup.find_all(
                "th",
                class_=re.compile("Column(1|2|10).?(ColumnLast)? (String|Numeric)"))
            column1 = soup.find_all("td", class_="String Column1")
            column1.insert(0, tabela_hdr[0])
            column2 = soup.find_all("td", class_="Numeric Column2")
            column2.insert(0, tabela_hdr[1])
            column3 = soup.find_all("td", class_="Numeric Column10 ColumnLast")
            column3.insert(0, tabela_hdr[2])

            head_dict = [[col1.string, [col2.string, col3.string]]
                         for col1, col2, col3 in zip(column1, column2, column3)]

            return head_dict
        except HTTPError:
            return ['http error']

    def ipca_webscrapping(self):
        year = str(date.today().year - 1)

        html_doc = request.urlopen(self.ipca_address)
        soup = BeautifulSoup(html_doc, 'html.parser')
        tabela_bd = soup.find_all('table')

        font_tag = tabela_bd[3].find_all('font')
        count = 0
        prt_str = ''
        final_r = []
        for i in list(font_tag):
            if year in str(i.string):
                break

            if count == 4:
                final_r.append(prt_str)
                prt_str = ''
                count = 0
                continue

            prt_str += str(i.string).strip() + ' '
            count += 1

        final_r[0] = 'M/A  Mes  Ano  12meses'
        return final_r
