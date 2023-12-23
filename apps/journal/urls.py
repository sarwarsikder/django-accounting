# urls.py
from django.urls import path
from .views import transaction_list, create_transaction, update_transaction, delete_transaction

urlpatterns = [
    path('list', transaction_list, name='transaction-list'),
    path('create/', create_transaction, name='create-transaction'),
    path('update/<int:transaction_id>/', update_transaction, name='update-transaction'),
    path('delete/<int:transaction_id>/', delete_transaction, name='delete-transaction'),
]
