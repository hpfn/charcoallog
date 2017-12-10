from collections import OrderedDict
from datetime import date

from django.contrib import messages
from .forms import EditExtractForm, SelectExtractForm
from .models import Extract


class ShowData:
    def __init__(self, request):
        self.request = request
        self.month_01 = date.today().strftime('%Y-%m-01')
        self.query_root = Extract.objects
        self.query_user = self.query_root.user_logged(self.request.user)
        self.query_default = self.query_user.filter(date__gte=self.month_01)

    def method_post(self):
        form = EditExtractForm(self.request.POST)

        if form.is_valid():
            self.insert_by_post(form)

        return self.query_default

    def method_get(self):
        bills = 0
        get_form = SelectExtractForm(self.request.GET)

        if get_form.is_valid():
            bills = self.search_from_get(get_form)

        return bills or self.query_default

    def search_from_get(self, form):
        column = form.cleaned_data.get('column')
        from_date = form.cleaned_data.get('from_date')
        to_date = form.cleaned_data.get('to_date')

        if column.lower() == 'all':
            bills = self.query_user.date_range(from_date, to_date)
        else:
            bills = self.query_user.date_range(from_date, to_date).which_field(column)

        if bills.exists():
            return bills

        messages.error(self.request,
                       "' %s ' is an Invalid search or wrong date!" % column)

    def insert_by_post(self, form):
        what_to_do = form.cleaned_data.get('update_rm')
        del form.cleaned_data['update_rm']
        id_for_update = form.cleaned_data.get('pk')
        del form.cleaned_data['pk']

        if what_to_do == 'remove':
            self.query_root.filter(**form.cleaned_data).delete()
        elif what_to_do == 'update':
            obj = self.query_root.get(id=id_for_update, user_name=self.request.user)
            obj.date = form.cleaned_data['date']
            obj.money = form.cleaned_data['money']
            obj.description = form.cleaned_data['description']
            obj.category = form.cleaned_data['category']
            obj.payment = form.cleaned_data['payment']
            obj.save(update_fields=['date', 'money', 'description', 'category', 'payment'])
        else:
            form.save()

    def show_total(self):
        payment_iterator = set(self.query_root.values_list('payment'))

        total_account = {
            conta[0]: self.query_root.filter(payment=conta[0]).total()
            for conta in payment_iterator
        }

        saldo = sum([resto['money__sum']for resto in total_account.values()])

        return OrderedDict(sorted(total_account.items())), saldo
