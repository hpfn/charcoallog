from django.conf.urls import url
from charcoallog.bank.views import home, ajax_post, delete

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^ajax_post/', ajax_post, name='ajax_post'),
    url(r'^delete/', delete, name='delete'),
]
