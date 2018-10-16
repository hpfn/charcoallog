from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.bank.models import Extract
from charcoallog.core.scrap_line3_service import Scrap
from charcoallog.investments.brief_investment_service import BriefInvestment
from charcoallog.investments.models import NewInvestment, NewInvestmentDetails


class BuildHome:
    def __init__(self, request_user):
        self.query_user = Extract.objects.user_logged(request_user)
        self.line1 = BriefBank(self.query_user)
        tabela = Scrap()
        self.selic_info = tabela.selic_info()
        self.ibov_info = tabela.ibov_info()
        self.ipca_info = tabela.ipca_info()

        self.query_user_invest = NewInvestment.objects.user_logged(request_user)
        self.query_user_details = NewInvestmentDetails.objects.user_logged(request_user)
        self.line2 = BriefInvestment(self.query_user_invest, self.query_user_details)
