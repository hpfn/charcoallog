from django.conf.urls import url
from charcoallog.core import views as v

urlpatterns = [
    url(r'^$', v.home, name='home'),
    url(r'^v2/$', v.home2, name='home2'),
    url(r'^v2/(?P<pk>\d+)/edit/$', v.money_edit, name='money_edit'),
    url(r'^v2/(?P<pk>\d+)/delete/$', v.money_delete, name='money_delete'),
    url(r'^ajax_post/', v.ajax_post, name='ajax_post')
]
