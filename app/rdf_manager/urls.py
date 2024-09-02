from django.urls import path
from .views import upload_ttl, add_namespace, homepage, create_database, connect_database, get_active_database, get_active_repository, get_files, createActualDB, destroyDB, retrieveDBlogs, retrieveDBcontainers, testWithin, upload_file

urlpatterns = [
    path('', homepage, name='homepage'),  # Root path
    path('get_files/', get_files, name='get_files'),
    path('upload_file/', upload_file, name='upload_file'),
    path('upload_ttl/', upload_ttl, name='upload_ttl'),
    path('namespace/add/', add_namespace, name='add_namespace'),
    path('create_database/', create_database, name='create_database'),
    path('db_create/', createActualDB, name='create_database_instance'),
    path('db_destroy/', destroyDB, name='destroy_database_instance'),
    path('db_logs/', retrieveDBlogs, name='view_database_logs'),
    path('db_containers/', retrieveDBcontainers, name='view_database_containers'),
    path('test/', testWithin, name='test'),
    path('connect_database/', connect_database, name='connect_database'),
    path('active_database/', get_active_database, name='get_active_database'),
    path('active_repository/', get_active_repository, name='get_active_repository'),
]
