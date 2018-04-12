from datetime import date

from charcoallog.investments.forms import InvestmentForm


class MethodGet:
    def __init__(self, query_user):
        """
        :param query_user: Investment objects from ..models.py
        """
        self.month_01 = date.today().strftime('%Y-%m-01')
        # self.query_user = query_user
        self.query_default = query_user.filter(date__gte=self.month_01)
        # self.selectextractform = InvestmentForm()