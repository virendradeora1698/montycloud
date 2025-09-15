from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

s3_storage = S3Boto3Storage()

class Image(models.Model):
    user = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='uploads/', storage=s3_storage)
    name = models.CharField(max_length=255, unique=False)  # New unique field for image name
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image name {self.name}"