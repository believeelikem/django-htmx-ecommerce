from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
import re
from users.models import is_valid_phonenum

class Category(models.Model):
    slug = models.SlugField( null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
class Tag(models.Model):
    slug = models.SlugField(null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)    
    
class Product(models.Model):
    slug = models.SlugField()
    name = models.CharField(blank=True, null=True)
    quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    category = models.ManyToManyField(to=Category,blank=True, null=True)
    tag = models.ManyToManyField(to=Tag, blank=True, null=True)
    added_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        blank=True, 
        null=True,
        on_delete=models.SET_NULL
    )
    is_digital = models.BooleanField(default=False)
    details = models.JSONField(default=list)
    
class Order(models.Model):
    STATUS = {
        "PENDING":"Pending",
        "COMPLETED":"Completed",
        "PAID":"Paid",
        "SHIPPED":"Shipped"
    }
    
    slug = models.SlugField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    is_completed = models.BooleanField(default=False)
    staus = models.CharField(choices=STATUS,blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
class OrderItem(models.Model):
    product = models.ForeignKey(to=Product,blank=True, null=True, on_delete=models.SET_NULL) 
    order = models.ForeignKey(to=Order,blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    total = models.PositiveSmallIntegerField(blank=True, null=True)
    
    
    
class ShippingAddress(models.Model):
    order = models.ForeignKey(to=Order, blank=True, null=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(
        max_length=10,
        validators= [is_valid_phonenum], 
        null=True,
        blank=True
    )
    city = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=150, null=True, blank=True)
    postal_code = models.CharField(max_length=150, blank=True, null=True)
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    is_delivered = models.BooleanField(default=False)
    shipped_at = models.DateTimeField()
    
class Rating:
    pass