# from django.contrib.auth.models import User
# from django.template import Template, Context
from django.template.response import SimpleTemplateResponse
from django.test import TestCase
# from django.shortcuts import resolve_url as r, render
from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.bank.models import Extract
# from charcoallog.core.service import BuildHome


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


class FakeBuildHome:
    def __init__(self, user):
        self.query_user = Extract.objects.user_logged(user)
        self.line1 = BriefBank(self.query_user)
        tabela = FakeScrap()
        self.selic_info = tabela.selic_info()
        self.ibov_info = tabela.ibov_info()
        self.ipca_info = tabela.ipca_info()


def home():
    user = {'username': 'teste'}
    context = {
        'build_home': FakeBuildHome('teste'),
        'user': user}
    # print(t.render(context))
    return SimpleTemplateResponse('home.html', context=context, status=200, charset='utf-8')


class HomeContextTest(TestCase):
    def setUp(self):
        # user = User.objects.create(username='teste')
        # user.set_password('1qa2ws3ed')
        # user.save()

        # self.login_in = self.client.login(username='teste', password='1qa2ws3ed')
        # self.response = self.client.get(r('core:home'))
        self.response = home()

    def test_status_code(self):
        """ status code must be 200 """
        self.assertEqual(200, self.response.status_code)

    # def test_template(self):
    #    self.assertTemplateUsed(self.response, 'home.html')

    def test_html_link(self):
        self.assertContains(self.response, '<a href', 4)

    def test_context_only_instance(self):
        build_home = self.response.context_data['build_home']
        self.assertIsInstance(build_home, FakeBuildHome)
