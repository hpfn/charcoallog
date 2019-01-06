from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from charcoallog.investments.views import (
    DetailApi, HomeApi, home, newinvestmetdetails_detail
)

app_name = 'investments'

urlpatterns = [
    path('', home, name='home'),
    path('home_api/<int:pk>/', HomeApi.as_view(), name='home_api'),
    path('details/<str:kind>/', newinvestmetdetails_detail, name='details'),
    path('details/detail_api/<int:pk>/', DetailApi.as_view(), name='details_api'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
