from django.urls import path

from charcoallog.bank.views import delete, home, update

app_name = 'bank'

urlpatterns = [
    path('', home, name='home'),
    path('update/', update, name='update'),
    path('delete/', delete, name='delete'),
]
