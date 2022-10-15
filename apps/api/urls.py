from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),    
    path('index/auth/<str:institution_id>', views.auth),
    path('index/details', views.details),
]