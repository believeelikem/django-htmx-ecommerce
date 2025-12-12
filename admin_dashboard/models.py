from django.db import models
from PIL import Image
# Create your models here.
 
class TempImage(models.Model):
    temp_image = models.ImageField(upload_to="temp_images/")
    
    
    def save(self):
        super().save()
        img = Image.open(self.temp_image.path)
        if img.height > 1000 or img.width > 1000:
            output_size = (1000,1000)
            img.thumbnail(output_size)
            img.save(self.temp_image.path)