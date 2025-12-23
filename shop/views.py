import re
from django.http import HttpResponse
from django.shortcuts import render
from .models import Product,ProductImage
from django.db import connection
from django.db.models import F
from django.db.models import OuterRef, Subquery


def home(request):

    # Get the first image for each product specifically
    image_subquery = ProductImage.objects.filter(
        product=OuterRef('pk')
    ).order_by('id').values('photo')[:1]

    products = Product.objects.annotate(
        first_image_for_cover = Subquery(image_subquery)
    )
    
    print(vars(products.first()))
        
    # # print(products.first().images.first().photo.name)
    
    print("Querioes is = ", len(connection.queries))
    
    
    context = {
        "products":products
    }
    return render(request, "shop/index.html", context = context )


def cart(request):
    return render(request, "shop/cart.html")

def products(request):
    return render(request, "shop/product-listings.html")

def product_detail(request):
    return render(request, "shop/product-detail.html")

def checkout(request):
    return render(request, "shop/checkout.html")

def user_dashboard(request):
    return render(request, "shop/user-dashboard.html")