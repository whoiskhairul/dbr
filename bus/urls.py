from django.contrib import admin
from django.urls import path,include
from bus import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bus/<int:id>', views.each_bus_info, name='each_bus_info'),
    path('bus', views.bus_list, name='bus_list'),
    path('confirm/', views.confirm, name='confirm'),
    path('restaurant/<int:id>', views.restaurant, name='restaurent'),

    
]
