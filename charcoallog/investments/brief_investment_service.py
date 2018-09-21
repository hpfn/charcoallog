from collections import OrderedDict


class BriefInvestment:
    def __init__(self, query_user_invest, query_user_investdetail):
        self._query_user_invest = query_user_invest
        self._query_user_investdetail = query_user_investdetail

    # def brokerage_or_invest_type(self):
    #     brk_knd = self._brokerage()
    #     brk_knd.update(self._kind_investment())
    #
    #     return OrderedDict(sorted(brk_knd.items()))

    def brokerage(self):
        names_iterator = set(self._query_user_invest.brokerage())

        brk = {
            k[0]: self._query_user_invest.filter(brokerage=k[0]).total_money()
            for k in names_iterator
        }

        return OrderedDict(sorted(brk.items()))

    def kind_investmentdetail(self):
        names_iterator = set(self._query_user_investdetail.kind())

        # Show value from brokerage to investment as positive
        kind = {
            k[0]: self._query_user_investdetail.filter(basic_data__kind=k[0]).total_money()
            for k in names_iterator
        }

        return OrderedDict(sorted(kind.items()))
