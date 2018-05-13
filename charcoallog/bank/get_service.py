from datetime import date

from django.contrib import messages

from charcoallog.bank.forms import SelectExtractForm


class MethodGet:
    def __init__(self, request, query_user):
        """
        :param request: request from views
        :param query_user: Extract objects from ..models.py
        """
        self.request = request
        self.request_get = request.GET
        self.month_01 = date.today().strftime('%Y-%m-01')
        self.query_user = query_user
        self.query_default = self.query_user.filter(date__gte=self.month_01)
        self.query_default_total = self.query_default.total()
        self.selectextractform = SelectExtractForm
        self.get_form = None

        if request.method == "GET":
            self.method_get()

    def method_get(self):
        self.get_form = self.selectextractform(self.request_get)

        if self.get_form.is_valid():
            self.search_from_get(self.get_form)

    def search_from_get(self, form):
        column = form.cleaned_data.get('column')
        from_date = form.cleaned_data.get('from_date')
        to_date = form.cleaned_data.get('to_date')

        if column.lower() == 'all':
            bills = self.query_user.date_range(from_date, to_date)
        else:
            bills = self.query_user.date_range(from_date, to_date).which_field(column)

        if bills.exists():
            # print('bills exists')
            self.query_default = bills
        else:
            # self.query_default = None
            messages.error(
                self.request,
                "' %s ' - Invalid search or nothing for these dates." % column
            )
