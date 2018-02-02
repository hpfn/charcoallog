from charcoallog.bank.brief_bank_service import BriefBank
from charcoallog.bank.models import Extract


class BuildHome:
    def __init__(self, request_user):
        self.query_user = Extract.objects.user_logged(request_user)
        self.line1 = BriefBank(self.query_user)