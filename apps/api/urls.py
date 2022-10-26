from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.IndexPage.index, name = 'index'),    
    path('index/auth/<str:institution_id>', views.Authentication.auth, name = 'auth'),
    path('index/details', views.DetailView.details, name = 'details'),
    path('index/details/get_transactions', views.DetailView.get_transactions, name = 'get-transactions'),
    path('index/details/get_balances', views.DetailView.get_balances, name = 'get-balances'),
    path('index/details/get_details', views.DetailView.get_details, name = 'get-details'),
]
