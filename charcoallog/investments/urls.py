from django.conf.urls import url

from charcoallog.investments.views import detail, home

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^([\w ]+)/$', detail, name='detail'),
]
