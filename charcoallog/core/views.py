from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import EditExtractForm, SelectExtractForm
from .service import ShowData  # insert_by_post, search_from_get


@login_required
def home(request):
    bills = ShowData(request)
    if request.method == 'POST':
        bills_query = bills.method_post()
    else:
        bills_query = bills.method_get()

    total_account, saldo = bills.show_total()

    context = {
        'bills': bills_query,
        'total': bills_query.total(),
        'form': EditExtractForm(),
        'get_form': SelectExtractForm(),
        'total_account': total_account,
        'saldo': saldo,
    }
    return render(request, "home.html", context)


# @login_required
# def show_data(request):
#     d = date.today().strftime('%Y-%m-01')
#     bills = 0
#
#     if request.method == 'POST':
#         form = EditExtractForm(request.POST)
#
#         if form.is_valid():
#             form.cleaned_data['user_name'] = request.user
#             insert_by_post(form)
#
#     elif request.method == 'GET':
#         get_form = SelectExtractForm(request.GET)
#
#         if get_form.is_valid():
#             bills = search_from_get(request, get_form)
#
#     return bills or Extract.objects.user_logged(request.user).filter(date__gte=d)
#

# @login_required
# def show_total(request):
#     payment_iterator = set(Extract.objects.user_logged(
#         request.user).values_list('payment'))
#
#     total_account = {
#         conta[0]: Extract.objects.user_logged(request.user).filter(
#             payment=conta[0]).total() for conta in payment_iterator
#     }
#     # total_account = dict()
#     # for set_value in payment_iterator:
#     #    conta = set_value[0]
#     #    total_account[conta] = Extract.objects.user_logged(request.user).filter(
#     #        payment=conta).total()
#
#     saldo = sum([resto['money__sum']for resto in total_account.values()])
#
#     return OrderedDict(sorted(total_account.items())), saldo
