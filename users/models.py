from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
import re

def is_valid_phonenum(number):
    if not re.search(r"^\d{10}$"):
        raise ValidationError("Invalid Number")

class CustomUser(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(default="avatar.png", upload_to="profile_pics/")
    address = models.CharField(max_length = 150, null=True, blank=False)
    phone_number = models.CharField(
        max_length=10,
        validators= [is_valid_phonenum], 
        null=True,
        blank=True
    )
    city = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=150, null=True, blank=True)
    