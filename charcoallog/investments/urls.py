from django.conf.urls import url
from charcoallog.investments.views import home


urlpatterns = [
    url(r'^$', home, name='home'),
]
