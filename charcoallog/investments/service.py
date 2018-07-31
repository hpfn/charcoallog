from charcoallog.investments.get_service import MethodGet
from charcoallog.investments.models import Investment, InvestmentDetails
from charcoallog.investments.post_service import MethodPost
from charcoallog.investments.brief_investment_service import BriefInvestment


class ShowData:
    def __init__(self, request):
        self.query_user_invest = Investment.objects.select_related('basic_data').user_logged(request.user)
        self.query_user_investdetail = InvestmentDetails.objects.select_related('basic_data').user_logged(request.user)
        self.methodpost = MethodPost(request, self.query_user_invest)
        self.methodget = MethodGet(self.query_user_invest)
        self.brief_investment = BriefInvestment(self.query_user_invest, self.query_user_investdetail)
        # self.brief_invest_total = self.brief_investment.brokerage_or_invest_type()
        # self.account_names = self.line1.account_names()
        # self.whats_left = self.line1.whats_left()
