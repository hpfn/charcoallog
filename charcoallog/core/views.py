from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# from .forms import EditExtractForm, SelectExtractForm
from .service import ShowData  # insert_by_post, search_from_get


@login_required
def home(request):
    context = {
        'show_data': ShowData(request),
    }
    return render(request, "home.html", context)
