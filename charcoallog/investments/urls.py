from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from charcoallog.investments.views import (
    DetailApi, HomeApi, home, newinvestmetdetails_detail
)

app_name = 'investments'

urlpatterns = [
    path('', home, name='home'),
    path('<str:kind>/', newinvestmetdetails_detail, name='new_invest_details'),
    path('details/api/<int:pk>/', HomeApi.as_view(), name='home_api'),
    path('details/detail_api/<int:pk>/', DetailApi.as_view(), name='detail_api'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
