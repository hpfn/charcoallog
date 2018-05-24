from django.conf.urls import url
from charcoallog.bank.views import home, update, delete

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^update/', update, name='update'),
    url(r'^delete/', delete, name='delete'),
]
