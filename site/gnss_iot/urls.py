
from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/devices/', views.devices, name='devices'),
    path('profile/new_device/', views.new_device, name='new_device'),
    path('profile/delete_device/<int:device_id>/', views.delete_device, name='delete_device'),
    path('profile/edit_device/<int:device_id>/', views.edit_device, name='edit_device'),
]
