from collections import OrderedDict
from datetime import date

# from django.contrib import messages
from django.contrib import messages

# from .forms import EditExtractForm, SelectExtractForm
from .models import Extract
from .post_service import MethodPost
from .get_service import MethodGet


class ShowData:
    def __init__(self, request):
        self.request = request
        # self.editextractform = EditExtractForm
        # self.selectextractform = SelectExtractForm
        # self.month_01 = date.today().strftime('%Y-%m-01')
        # self.query_root = Extract.objects
        self.query_user = Extract.objects.user_logged(self.request.user)
        # self.query_default = self.query_user.filter(date__gte=self.month_01)
        # self.query_default_total = self.query_default.total()
        self.account_values = 0

        self.form1 = MethodPost(self.request, self.query_user)  # , self.editextractform)
        self.form2 = MethodGet(self.request, self.query_user)  # , self.selectextractform)
        #self.method_get()
        #self.choose_method()

    #def choose_method(self):
    #    if self.request.method == 'POST':
    #        MethodPost(self.request, self.query_root, self.editextractform)
    #    else:
    #        self.method_get()
    #        #MethodGet(self.request, self.query_user, self.query_default, self.selectextractform)

    # def method_post(self):
    #     form = self.editextractform(self.request.POST)
    #
    #     if form.is_valid():
    #         self.insert_by_post(form)

    # def method_get(self):
    #     get_form = self.selectextractform(self.request.GET)
    #
    #     if get_form.is_valid():
    #         self.search_from_get(get_form)
    #
    # def search_from_get(self, form):
    #     column = form.cleaned_data.get('column')
    #     from_date = form.cleaned_data.get('from_date')
    #     to_date = form.cleaned_data.get('to_date')
    #
    #     if column.lower() == 'all':
    #         bills = self.query_user.date_range(from_date, to_date)
    #     else:
    #         bills = self.query_user.date_range(from_date, to_date).which_field(column)
    #
    #     if bills.exists():
    #         self.query_default = bills
    #     else:
    #          messages.error(
    #              self.request,
    #              "' %s ' is an Invalid search or wrong date!" % column
    #          )

    # def insert_by_post(self, form):
    #     what_to_do = form.cleaned_data.get('update_rm')
    #     del form.cleaned_data['update_rm']
    #     id_for_update = form.cleaned_data.get('pk')
    #     del form.cleaned_data['pk']
    # 
    #     if not what_to_do:
    #         form.save()
    #     elif what_to_do == 'remove':
    #         self.query_root.filter(**form.cleaned_data).delete()
    #     elif what_to_do == 'update':
    #         obj = self.query_root.get(id=id_for_update, user_name=self.request.user)
    #         obj.date = form.cleaned_data['date']
    #         obj.money = form.cleaned_data['money']
    #         obj.description = form.cleaned_data['description']
    #         obj.category = form.cleaned_data['category']
    #         obj.payment = form.cleaned_data['payment']
    #         obj.save(update_fields=['date', 'money', 'description', 'category', 'payment'])

    def account_names(self):
        payment_iterator = set(self.query_user.values_list('payment'))

        account = {
            conta[0]: self.query_user.filter(payment=conta[0]).total()
            for conta in payment_iterator
        }

        # saldo = sum([resto['money__sum']for resto in total_account.values()])
        self.account_values = account.values()

        return OrderedDict(sorted(account.items()))  # , saldo

    def whats_left(self):
        return sum([resto['money__sum'] for resto in self.account_values])
