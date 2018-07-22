from django.db import models

# Create your models here.
# here upload_to will be appended to the media root
class Document(models.Model):
    name = models.CharField(max_length=100)
    path = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='document'


class UserDirectory(models.Model):
    directory_path = models.CharField(max_length=100)
    crt_dt = models.DateTimeField(auto_now_add=True)
    upd_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='user_directory'
