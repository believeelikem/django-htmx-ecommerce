from django.db import models
from PIL import Image
# Create your models here.
 
class TempImage(models.Model):
    temp_image = models.ImageField(upload_to="temp_images/")
    
    
    def save(self):
        super().save()
        img = Image.open(self.temp_image.path)
        if img.height > 900 or img.width > 900:
            output_size = (900,900)
            img.thumbnail(output_size)
            img.save(self.temp_image.path)