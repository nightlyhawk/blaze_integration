from django.urls import path
from .views import upload_ttl, add_namespace, homepage, create_database, connect_database, get_active_database, get_active_repository

urlpatterns = [
    path('upload/', upload_ttl, name='upload_ttl'),
    path('namespace/add/', add_namespace, name='add_namespace'),
    path('', homepage, name='homepage'),  # Root path
    path('connect_database/', connect_database, name='connect_database'),
     path('active-database/', get_active_database, name='get_active_database'),
    path('active-repository/', get_active_repository, name='get_active_repository'),
]
