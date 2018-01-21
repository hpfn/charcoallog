from django.conf.urls import url
from charcoallog.core.views import home #, ajax_post

urlpatterns = [
    url(r'^$', home, name='home'),
#    url(r'^ajax_post/', ajax_post, name='ajax_post')
]
