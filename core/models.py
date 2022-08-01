from django.db import models

# Create your models here.
class Image(models.Model):
    image_path = models.CharField(max_length=255)
    meta_data = models.JSONField()
    
    def __str__(self):
        return str(self.id)