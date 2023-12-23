from django.urls import path
from django.contrib.auth.views import LogoutView

from apps.users.views import user_login, user_list, edit_user, delete_user

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('list/', user_list, name='user-list'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    # Add other URL patterns for your views
]
