from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# from .forms import EditExtractForm, SelectExtractForm
from .service import ShowData  # insert_by_post, search_from_get


@login_required
def home(request):
    bills = ShowData(request)
    #total_account, saldo = bills.show_total()

    context = {
        'bills': bills,
        'total': bills,
        'form': bills,
        'get_form': bills,
        'total_account': bills,
        'saldo': bills,
    }
    return render(request, "home.html", context)
