from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from charcoallog.investments.views import (
    DetailAPI, FormDeals, home, newinvestmetdetails_detail
)

app_name = 'investments'

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^([\w ]+)/$', newinvestmetdetails_detail, name='detail'),
    url(r'^api/(?P<pk>[0-9]+)/$', FormDeals.as_view(), name='api'),
    url(r'^detail_api/(?P<pk>[0-9]+)/$', DetailAPI.as_view(), name='detail_api'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
