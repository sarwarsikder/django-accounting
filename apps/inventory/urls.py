from django.urls import path
from .views import inventory_list, inventory_create, inventory_update, inventory_delete

urlpatterns = [
    path('list/', inventory_list, name='inventory-list'),
    path('create/', inventory_create, name='inventory-create'),
    path('<int:pk>/edit/', inventory_update, name='inventory-edit'),
    path('<int:pk>/delete/', inventory_delete, name='inventory-delete'),
]
