from django.conf.urls import url
from django.contrib.auth.views import login, logout
from charcoallog.accounts.views import register

urlpatterns = [
        url(r'^entrar/', login,
            {'template_name': 'accounts/login.html'}, name='login'),
        url(r'^sair/', logout,
            {'next_page': 'core:home'}, name='logout'),
        url(r'^cadastre-se/', register, name='register'),
]   
