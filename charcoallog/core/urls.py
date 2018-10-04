from django.conf.urls import url

from charcoallog.core.views import home

app_name = 'core'

urlpatterns = [
    url(r'^$', home, name='home'),
]
