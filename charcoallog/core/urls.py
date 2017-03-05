from django.conf.urls import url
from .views import home, title, bottom
from .views import middle
from .views import insert_data_form
from .views import show_data, show_choice_data, show_total

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^frameset_pages/title.html$', title, name='title'),
    url(r'^frameset_pages/middle.html$', middle, name='middle'),
    url(r'^frameset_pages/form1.html$', insert_data_form, name='form1'),
    url(r'^frameset_pages/form2.html$', show_choice_data, name='form2'),
    url(r'^frameset_pages/line1.html$', show_total, name='show_total'),
    # url(r'^frameset_pages/linha2.html$', show_data, name='show_data'),
    url(r'^frameset_pages/line3.html$', show_data, name='show_data'),
    url(r'^frameset_pages/bottom.html$', bottom, name='bottom'),
]
