from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.criar, name="criar"),
    path('ver/', views.ver, name="ver"),
    path('registros/', views.registros, name="registros"),
]
