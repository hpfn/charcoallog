from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import register

app_name = 'accounts'

urlpatterns = [
    path('entrar/',
         LoginView.as_view(template_name='accounts/login.html'),
         name='login'),
    path('sair/',
         LogoutView.as_view(next_page='core:home'),
         name='logout'),
    path('cadastre-se/', register, name='register'),
]
