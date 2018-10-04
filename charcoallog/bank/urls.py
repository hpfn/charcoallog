from django.conf.urls import url

from charcoallog.bank.views import delete, home, update

app_name = 'bank'

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^update/', update, name='update'),
    url(r'^delete/', delete, name='delete'),
]
