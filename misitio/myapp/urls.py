from django.urls import path
from . import views

urlpatterns = [
    path('', views.frontal),
    path('prueba/', views.prueba, name='prueba'),
    path('enviar/', views.enviar, name='enviar'),
    path('index.html/', views.peticiones, name='peticiones'),
    path('index.html/FFU.html/', views.FFU, name='FFU'),
    path('index.html/FFC.html/', views.FFC, name='FFC'),
]