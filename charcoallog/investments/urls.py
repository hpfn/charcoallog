from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from charcoallog.investments.views import (
    DetailAPI, FormDeals, home, newinvestmetdetails_detail
)

app_name = 'investments'

urlpatterns = [
    path('', home, name='home'),
    path('<str:kind>/', newinvestmetdetails_detail, name='detail'),
    path('api/<int:pk>/', FormDeals.as_view(), name='api'),
    path('detail_api/<int:pk>/', DetailAPI.as_view(), name='detail_api'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
