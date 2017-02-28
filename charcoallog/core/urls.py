from django.conf.urls import url
from charcoallog.core.views import home, titulo, rodape
from charcoallog.core.views import row2, coluna1, form1, form2
from charcoallog.core.views import show_data, insert_data_form, show_choice_data


urlpatterns = [
        url(r'^$', home, name='home'),
        url(r'^frameset_pages/titulo.html$', titulo, name='titulo'),
        url(r'^frameset_pages/row2.html$', row2, name='row2'),
        url(r'^frameset_pages/coluna1.html$', coluna1, name='coluna1'),
        url(r'^frameset_pages/form1.html$', insert_data_form, name='form1'),
        url(r'^frameset_pages/form2.html$', show_choice_data, name='form2'),
        url(r'^frameset_pages/rodape.html$', rodape, name='rodape'),
        url(r'^frameset_pages/linha3.html$', show_data, name='show_data'),
]                                                                               
