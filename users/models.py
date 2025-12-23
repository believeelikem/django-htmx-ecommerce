from encodings.punycode import T
from turtle import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
import re

def is_valid_phonenum(number):
    if not re.search(r"^\d{10}$"):
        raise ValidationError("Invalid Number")

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, null=True, blank= True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email
    

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
    
