from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# from .forms import EditExtractForm, SelectExtractForm
from .service import ShowData  # insert_by_post, search_from_get


@login_required
def home(request):
    bills = ShowData(request)
    total_account, saldo = bills.show_total()

    context = {
        'bills': bills.query_default,
        'total': bills.query_default.total(),
        'form': bills.editextractform,
        'get_form': bills.selectextractform,
        'total_account': total_account,
        'saldo': saldo,
    }
    return render(request, "home.html", context)
