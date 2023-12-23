# urls.py
from django.urls import path
from .views import persons_list, person_edit, person_delete, person_create

urlpatterns = [
    path('list/<str:person_type>/', persons_list, name='person-list'),
    path('create/<str:person_type>/', person_create, name='person-create'),
    path('persons/<int:pk>/edit/<str:person_type>/', person_edit, name='person-edit'),
    path('persons/<int:pk>/delete/<str:person_type>/', person_delete, name='person-delete'),

    # Add other URLs as needed
]
