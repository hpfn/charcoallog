from charcoallog.bank.models import Extract
from charcoallog.bank.get_service import MethodGet
from charcoallog.bank.post_service import MethodPost
from charcoallog.bank.brief_bank_service import BriefBank


class ShowData:
    def __init__(self, request):
        self.query_user = Extract.objects.user_logged(request.user)
        self.form1 = MethodPost(request, self.query_user)
        self.form2 = MethodGet(request, self.query_user)
        self.brief_bank = BriefBank(self.query_user)
        # self.account_names = self.line1.account_names()
        # self.whats_left = self.line1.whats_left()
