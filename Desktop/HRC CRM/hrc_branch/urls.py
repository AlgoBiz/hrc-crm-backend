from django.urls import path
from .views import customer_list_create, customer_detail

urlpatterns = [
    path('customers/', customer_list_create, name='customer_list_create'),
    path('customers/<int:pk>/', customer_detail, name='customer_detail'),
]