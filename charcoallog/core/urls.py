from django.conf.urls import url
from .views import home  # , exit
# from .views import show_data # why?

urlpatterns = [
    url(r'^$', home, name='home'),
    # url(r'exit$', exit, name='exit'),
    # url(r'^frameset_pages/line3.html$', show_data, name='show_data'),
]
