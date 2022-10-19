from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name ='index'),    
    path('index/auth/<str:institution_id>', views.auth),
    path('index/details/check_status', views.check_status, name = 'check-status'),
    path('index/details/get_transactions', views.get_transactions, name = 'get-transactions'),
    path('index/details/get_balances', views.get_balances, name = 'get-balances'),
    path('index/details', views.details),
]