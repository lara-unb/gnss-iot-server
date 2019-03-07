"""Define o padrão de URL para gnss_iot"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
