from django.conf.urls import url
from charcoallog.core.views import home, home2, ajax_post, money_delete

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^v2/$', home2, name='home2'),
    url(r'^v2/(?P<pk>\d+)/delete/$', money_delete, name='money_delete'),
    url(r'^ajax_post/', ajax_post, name='ajax_post')
]
