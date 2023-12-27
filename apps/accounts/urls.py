from django.urls import path
from .views import index, get_account_level2_options, get_account_level3_options, account_create, account_list, \
    edit_account, delete_account

urlpatterns = [
    path('', index, name='dashboard'),
    path('account/create', account_create, name='account-create'),
    path('account/list', account_list, name='account-list'),
    path('account/edit/<str:account_id>/', edit_account, name='edit-account'),
    path('account/delete/<str:account_id>/', delete_account, name='delete-account'),
    path('get_account_level2_options/', get_account_level2_options, name='get_account_level2_options'),
    path('get_account_level3_options/', get_account_level3_options, name='get_account_level3_options'),

]
