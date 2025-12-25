from multiprocessing import context
import re
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product,ProductImage
from django.db import connection
from django.db.models import F
from django.db.models import OuterRef, Subquery


def home(request):

    image_subquery = ProductImage.objects.filter(
        product=OuterRef('pk')
    ).order_by('id').values('photo')[:1]

    products = Product.objects.annotate(
        first_image_for_cover = Subquery(image_subquery)
    )    
    
    context = {
        "products":products
    }
    
    if request.htmx:
        return render(request, "shop/partials/_index.html", context = context )
    return render(request, "shop/index.html", context = context )


def cart(request):
    
    if request.htmx:
        return render(request, "shop/partials/_cart.html")
    
    return render(request, "shop/cart.html")



def products(request):
    return render(request, "shop/product-listings.html")

def product_detail(request,slug):
    
    product = get_object_or_404(Product, slug = slug)
    
    details = product.details
    for detail in details:
        detail["image_url"] = (
            get_object_or_404(
                ProductImage,id = detail["image_id"]
                ).photo.url
        )   
        
    context = {
        "variants":details,
        "sizes": get_related_specifics(details,key = "size"),
        "colors":get_related_specifics(details, key= "color"),
        "current":details[0]
    }
    
    return render(request, "shop/product-detail.html", context)

def get_related_specifics(details, key):
    return list(set(detail[key] for  detail in details))

def checkout(request):
    return render(request, "shop/checkout.html")

def user_dashboard(request):
    return render(request, "shop/user-dashboard.html")