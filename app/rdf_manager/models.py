from django.db import models

# Create your models here.

class UploadedFile(models.Model):
    name = models.CharField(max_length=255)
    graph_id = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    file = models.FileField(upload_to="ttl_files")
    uploaded_at = models.DateTimeField(auto_now_add=True)