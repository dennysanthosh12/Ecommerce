
from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home', views.home,name='home'),
    path('home/results', views.result,name='results'),
    path('home/product',views.product,name='product'),
    path('home/Tracking',views.Tracking,name='Tracking'),
    
]
