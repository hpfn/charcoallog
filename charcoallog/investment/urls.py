from django.conf.urls import url
from charcoallog.investment.views import home


urlpatterns = [
    url(r'^$', home, name='home'),
]
