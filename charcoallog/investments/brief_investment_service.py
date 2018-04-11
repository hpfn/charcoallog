from collections import OrderedDict
from django.db.models import Q
from charcoallog.investments.models import Investment


class BriefInvestment:
    def __init__(self):
        self.query_user = Investment.objects
        self.account = {}
        # self.investment_type = {}

    def brokerage_or_invest_type(self, brk_or_invest_t):
        names_iterator = set(self.query_user.values_list(brk_or_invest_t))

        self.account = {
            k[0]: self.query_user.filter(Q(brokerage=k[0]) | Q(kind=k[0])).total()
            for k in names_iterator
        }

        # self.account_values = account.values()

        return OrderedDict(sorted(self.account.items()))

#    @staticmethod
#    def total_amount(values):
#        return sum([resto['money__sum'] for resto in values])

