from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.bank.models import Extract
from charcoallog.core.scrap_line3_service import Scrap


class BuildHome:
    def __init__(self, request_user):
        self.query_user = Extract.objects.user_logged(request_user)
        self.line1 = BriefBank(self.query_user)
        tabela = Scrap()
        self.selic_info = tabela.selic_info()
        self.ibov_info = tabela.ibov_info()