from pyexpat import model
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
import re
from users.models import is_valid_phonenum
from django.utils.text import slugify


def sluggy(model, obj, slug_field = "name"):
    if not obj.slug:
        field_value = getattr(obj, slug_field)
        base_slug = slugify(field_value)
        
        current_slug = base_slug
        current_suffix = 1
        
        while model.objects.filter(slug = current_slug).exists():
            current_slug = f"{base_slug}-{current_suffix}"
            current_suffix += 1
        obj.slug = current_slug

class Category(models.Model):
    slug = models.SlugField( null=True, blank=True, unique=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
      
    def save(self, *args, **kwargs):
        sluggy(Category, self)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.slug} "
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
             
    
class Tag(models.Model):
    slug = models.SlugField(null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        sluggy(Tag, self)
        return super().save(*args, **kwargs)
    
class Product(models.Model):
    slug = models.SlugField(unique=True, blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    categories = models.ManyToManyField(to=Category,related_name="products")
    tag = models.ManyToManyField(to=Tag, blank=True, null=True)
    added_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        blank=True, 
        null=True,
        on_delete=models.SET_NULL
    )
    is_digital = models.BooleanField(default=False)
    details = models.JSONField(default=list)

    def __str__(self):
        return self.name
    
  
    def save(self, *args, **kwargs):
        sluggy(Product, self)
        return super().save(*args, **kwargs)
   
class ProductImage(models.Model):
    photo = models.ImageField(null=True, blank=True, upload_to="products_images/")
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE,blank=True, 
        null=True, related_name="images"
    )
       
    def __str__(self):
        return f"{self.get_photo_name()} belongs to {self.product}"
    
    def get_photo_name(self):
        return self.photo.name.split("/")[1]
       
    
class Order(models.Model):
    STATUS = {
        "PENDING":"Pending",
        "COMPLETED":"Completed",
        "PAID":"Paid",
        "SHIPPED":"Shipped"
    }
    
    slug = models.SlugField(blank=True, null=True, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    is_completed = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS,blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    
    # def save(self, *args, **kwargs):
    #     sluggy(Product, self, slug_field="name")
    #     return super().save(*args, **kwargs)
    
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
    
    class Meta:
        verbose_name_plural = ("Shipping Adress")
    
class Rating:
    pass