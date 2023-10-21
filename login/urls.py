from django.urls import path
from . import views

urlpatterns = [
    path('',views.login, name='loginhome'),
    path('login',views.login, name='login'),
    path('cadastro',views.cadastro, name='cadastro'),
    path('logout/', views.user_logout, name='deslogar'),
]
