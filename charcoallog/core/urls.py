from django.conf.urls import url
from charcoallog.core.views import home

urlpatterns = [
    url(r'^$', home, name='home'),
]
