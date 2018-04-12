from charcoallog.investments.get_service import MethodGet
from charcoallog.investments.models import Investment
from charcoallog.investments.post_service import MethodPost


class ShowData:
    def __init__(self, request):
        self.query_user = Investment.objects.user_logged(request.user)
        self.methodpost = MethodPost(request, self.query_user)
        self.methodget = MethodGet(self.query_user)
        #self.brief_bank = BriefInvestiment(self.query_user)
        # self.account_names = self.line1.account_names()
        # self.whats_left = self.line1.whats_left()