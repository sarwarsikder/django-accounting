# apps/inventory_transaction/urls.py
from django.urls import path

from .views import (
    inventory_transaction_list,
    inventory_transaction_create,
    inventory_transaction_update,
    inventory_transaction_delete,
)

urlpatterns = [
    path('list/<str:type_of_transaction>/', inventory_transaction_list, name='inventory-transaction-list'),
    path('create/<str:type_of_transaction>/', inventory_transaction_create, name='inventory-transaction-create'),
    path('update/<int:pk>/<str:type_of_transaction>/', inventory_transaction_update,
         name='inventory-transaction-update'),
    path('delete/<int:pk>/', inventory_transaction_delete, name='inventory-transaction-delete'),
]
