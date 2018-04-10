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

    @staticmethod
    def total_amount(values):
        return sum([resto['money__sum'] for resto in values])
    #        return sum([resto['money__sum'] for resto in self.account.values()])

    # def brokerage_names(self):
    #     names_iterator = set(self.query_user.values_list('brokerage'))
    #
    #     self.account = {
    #         conta[0]: self.query_user.filter(brokerage=conta[0]).total()
    #         for conta in names_iterator
    #     }
    #
    #     # self.account_values = account.values()
    #
    #     return OrderedDict(sorted(self.account.items()))

# def investment_types(self):
#     names_iterator = set(self.query_user.values_list('kind'))
#
#     self.investment_type = {
#         type[0]: self.query_user.filter(kind=type[0]).total()
#         for type in names_iterator
#     }
#
#     # self.investment_amount = invest_type.values()
#
#     return OrderedDict(sorted(self.investment_type.items()))

# def investment_total_amount(self):
#     return sum([resto['money__sum'] for resto in self.investment_type.values()])
#
