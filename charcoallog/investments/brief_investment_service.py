from collections import OrderedDict

from charcoallog.investments.models import Investment


class BriefInvestment:
    def __init__(self):
        self.query_user = Investment.objects
        self.account_values = None
        self.investment_amount = None

    def brokerage_names(self):
        names_iterator = set(self.query_user.values_list('brokerage'))

        account = {
            conta[0]: self.query_user.filter(brokerage=conta[0]).total()
            for conta in names_iterator
        }

        self.account_values = account.values()

        return OrderedDict(sorted(account.items()))

    def total_amount(self):
        return sum([resto['money__sum'] for resto in self.account_values])

    def investment_types(self):
        names_iterator = set(self.query_user.values_list('kind'))

        account = {
            conta[0]: self.query_user.filter(kind=conta[0]).total()
            for conta in names_iterator
        }

        self.investment_amount = account.values()

        return OrderedDict(sorted(account.items()))

    def investment_total_amount(self):
        return sum([resto['money__sum'] for resto in self.investment_amount])
