from django.db import models

# Create your models here.
 
class TempImage(models.Model):
    temp_image = models.ImageField(upload_to="temp_images/")
    