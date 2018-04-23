from collections import OrderedDict
from django.db.models import Q
from charcoallog.investments.models import Investment


class BriefInvestment:
    def __init__(self, query_user):
        self._query_user = query_user

    def brokerage_or_invest_type(self):
        brk_knd = self._brokerage()
        brk_knd.update(self._kind_investment())

        return OrderedDict(sorted(brk_knd.items()))

    def _brokerage(self):
        names_iterator = set(self._query_user.values_list('brokerage'))

        brk = {
            k[0]: self._query_user.filter(brokerage=k[0]).total()
            for k in names_iterator
        }

        return brk

    def _kind_investment(self):
        names_iterator = set(self._query_user.values_list('kind'))

        kind = {
            k[0]: self._query_user.filter(kind=k[0]).total()
            for k in names_iterator
        }

        return kind

