from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from charcoallog.investments.views import FormDeals, detail, home

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^([\w ]+)/$', detail, name='detail'),
    url(r'^api/(?P<pk>[0-9]+)/$', FormDeals.as_view(), name='api'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
