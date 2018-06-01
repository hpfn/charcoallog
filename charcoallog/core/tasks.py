# from celery import Celery
import json
import re
from datetime import date
from urllib import request

from bs4 import BeautifulSoup
from celery.schedules import crontab
from celery.utils.log import get_task_logger
# from charcoallog.celery import app as celery_app
# RealPython.com
# from celery.decorators import periodic_task
from celery.task import periodic_task

# app = Celery('charcoallog')
# @app.on_after_configure


logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(day_of_week='sat', hour='6', minute='0')), name='ibov')
def ibov():
    logger.info('inicio de core/ibov.json')

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

    ibov_address = 'https://br.advfn.com/bolsa-de-valores/bovespa/ibovespa-IBOV/historico'
    req = request.Request(ibov_address, headers=hdr)
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

    # head_dict = {col1.string: [col2.string, col3.string]
    #             for col1, col2, col3 in zip(column1, column2, column3)}

    head_dict = [[col1.string, [col2.string, col3.string]]
                 for col1, col2, col3 in zip(column1, column2, column3)]

    json_data = {"ibov": head_dict}

    with open('./charcoallog/core/ibov.json', 'w') as ibov_info:
        json.dump(json_data, ibov_info)

    logger.info('fim de core/ibov.json')


@periodic_task(run_every=(crontab(day_of_month='14-15-16', hour='6', minute='10')), name='selic')
def selic():
    logger.info('inicio de core/selic.json')

    data = date.today()
    this_year = data.strftime("%Y")
    last_year = str(int(this_year) - 1)

    selic_address = 'https://www.bcb.gov.br/Pec/Copom/Port/taxaSelic.asp'

    html_doc = request.urlopen(selic_address)
    soup = BeautifulSoup(html_doc, 'html.parser')
    tabela = soup.find_all("td", class_="centralizado")

    tabela_dict = [[i.string, tabela[x + 1].string]
                   for x, i in enumerate(tabela)
                   if last_year in i.string or this_year in i.string]

    json_data = {"selic": tabela_dict}

    with open('./charcoallog/core/selic.json', 'w') as selic_info:
        json.dump(json_data, selic_info)

    logger.info('fim de core/selic.json')


@periodic_task(run_every=(crontab(day_of_month='14-15-16', hour='6', minute='20')), name='ipca')
def ipca():
    logger.info('inicio de core/ipca.json')

    ipca_address = 'http://www.indiceseindicadores.com.br/ipca/'

    html_doc = request.urlopen(ipca_address)
    soup = BeautifulSoup(html_doc, 'html.parser')

    tabela_bd = soup.find("tbody")

    ano = re.compile(r'<strong>\b(?P<ano>[0-9]{4})\b</strong>')
    get_ano = re.findall(ano, str(tabela_bd))

    # taxas = re.compile(r'<(strong|b)>\b(?P<indice>[0-9]{,2},[0-9]{2})\b</(strong|b)>')
    taxas = re.compile(
        r'<td style="text-align: right; width: [0-9.]{3,}px; height: [0-9.]{2,}px;">'
        r'(<span style="font-size: 10pt;">)?(<(strong|b)>)?\b(?P<indice>[0-9]{,2},[0-9]{2})\b'
        r'(</(strong|b)>)?(</span>)?</td>')

    get_tx = re.findall(taxas, str(tabela_bd))
    get_tx = [i[3] for i in get_tx]
    tx_ano_dict = [[ano, tx] for ano, tx in zip(get_ano[:10], get_tx[:10])]

    json_data = {"ipca": tx_ano_dict}

    with open('./charcoallog/core/ipca.json', 'w') as ipca_info:
        json.dump(json_data, ipca_info)

    logger.info('fim de core/ipca.json')
