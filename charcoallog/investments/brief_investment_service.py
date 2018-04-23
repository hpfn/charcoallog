from collections import OrderedDict
from django.db.models import Q
from charcoallog.investments.models import Investment


class BriefInvestment:
    def __init__(self, user_name):
        self._query_user = Investment.objects.user_logged(user_name)

    def brokerage_or_invest_type(self, brk_or_invest_t):
        names_iterator = set(self._query_user.values_list(brk_or_invest_t))

        account = {
            k[0]: self._query_user.filter(Q(brokerage=k[0]) | Q(kind=k[0])).total()
            for k in names_iterator
        }

        return OrderedDict(sorted(account.items()))


