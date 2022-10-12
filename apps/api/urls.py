from urllib import request
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),    
    path('index/auth/<str:institution_id>', views.auth),
    path('index/details', views.auth),
]