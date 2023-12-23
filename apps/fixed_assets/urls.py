# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.asset_list, name='asset-list'),
    path('create/', views.create_asset, name='create-asset'),
    path('<int:depreciation_id>/update/', views.update_asset, name='update-asset'),
    path('<int:depreciation_id>/delete/', views.delete_asset, name='delete-asset'),
]
