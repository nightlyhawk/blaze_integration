from django.urls import path
from .views import upload_ttl, add_namespace

urlpatterns = [
    path('upload/', upload_ttl, name='upload_ttl'),
    path('namespace/add/', add_namespace, name='add_namespace'),
]
