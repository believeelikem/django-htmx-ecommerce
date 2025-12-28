from math import prod
from multiprocessing import context
from os import name
import re
from zoneinfo import available_timezones
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product,ProductImage, Category
from django.db import connection
from django.db.models import F
from django.db.models import OuterRef, Subquery
from .utils import *


def home(request):

    image_subquery = ProductImage.objects.filter(
        product=OuterRef('pk')
    ).order_by('id').values('photo')[:1]

    products = Product.objects.annotate(
        first_image_for_cover = Subquery(image_subquery)
    ) 
    # request.session["cart"] = {}
    
    
    if not request.user.is_authenticated:
        if request.session.get("cart"):
            cart = request.session["cart"]
        else:
            cart = request.session["cart"] = {}
            
        for product in products:
            product.quantity_in_cart = \
            request.session["cart"][product.slug]["quantity"] \
            if cart and product.slug in request.session["cart"] else 0

        
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

def add_to_cart(request):
    if request.user.is_authenticated:
        ...
    else:
        if request.session.get("cart"):
            cart = request.session["cart"]
        else:
            cart = request.session["cart"] = {}

        order_item = {
            "product_id":request.POST.get("id"),
            "order":None,
            "quantity": None,
            "price":request.POST.get("price"),
            "color":request.POST.get("color"),
            "size":request.POST.get("size"),
            "price":request.POST.get("price"),
            "image_url":request.POST.get("image_url"),
            "slug":request.POST.get("slug"),
            
        }
        print("request.POST is = ", request.POST,"\n")       
        if cart:
            if is_already_in_cart(cart, order_item):
                order_item["quantity"] = int(request.session["cart"][order_item["slug"]]["quantity"]) + 1
        else:
            order_item["quantity"] = 1
        
        cart[order_item["slug"]] = order_item
        request.session["cart"] = cart
        request.session.modified = True
        print("cart is = ", cart)
        context = {
            "new_count":request.session["cart"][order_item["slug"]]["quantity"],
            "total_cart_count": len(request.session["cart"]),
            "product_id":order_item["product_id"]
        }
        
        if request.POST.get("from_index"):
            return render(request, "shop/partials/_cart-counter.html", context)
                
def is_already_in_cart(cart,order_item):    
    for item in cart:
        # print("o, r is = ",order_item)
        if cart[item]["product_id"] == order_item["product_id"] \
        and cart[item]["color"] == order_item["color"] and \
        cart[item]["size"] == order_item["size"]:
            return True
    return False
        

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
    
    color = request.GET.get("color")
    size = request.GET.get("size")
     
    current = get_variant(details, color, size)
    if current:
        available_sizes = get_sizes_for_chosen_color(details,current["color"])
    else:
        print("Something wrong")
        
    if not request.session.get(f"{product.slug}_quantity"):
        request.session[f"{product.slug}_quantity"] = 1
        
     
    product_quantity, should_reset = get_product_quantity(
            max_quantity=int(current["quantity"]),
            product_quantity_in_session = request.session[f"{product.slug}_quantity"]    
    )
    
    if should_reset:
        request.session[f"{product.slug}_quantity"] = int(current["quantity"])
        request.session.modified = True
        
    image_subquery = ProductImage.objects.filter(
        product=OuterRef('pk')
    ).order_by('id').values('photo')[:1]

    # related_products = pro.objects.annotate(
    #     first_image_for_cover = Subquery(image_subquery)
    # )
    
    related_products = Product.objects.filter(
        categories__in = product.categories.all()
    ).distinct().exclude(id = product.id).annotate(
        first_image_for_cover = Subquery(image_subquery)
    )
    
    for p in related_products:
        print(vars(p))

    context = {
        "variants":details,
        "sizes": get_related_specifics(details,key = "size"),
        "colors":get_related_specifics(details, key= "color"), 
        "current":current,
        "product_name":product.name,
        "product_slug":product.slug,
        "available_sizes":available_sizes,
        "product_quantity":product_quantity,
        "related_products":related_products
    }
       
    return render(request, "shop/product-detail.html", context)

def decrease_quantity(request, slug):
    if not request.session[f"{slug}_quantity"] <= 1:
        request.session[f"{slug}_quantity"] -= 1
        request.session.modified = True 
        
    return render(
        request, 
        "shop/partials/_product_quantity_count.html",
        {"new_count":request.session[f"{slug}_quantity"]}
    )
    
def increase_quantity(request, slug):
    product = get_object_or_404(Product, slug = slug)
    
    current = get_variant(product.details, request.POST.get("color"), request.POST.get("size"))
    if  int(current["quantity"]) > request.session[f"{slug}_quantity"]:
        request.session[f"{slug}_quantity"] += 1
        request.session.modified = True 
    
    return render(
        request, 
        "shop/partials/_product_quantity_count.html",
        {"new_count":request.session[f"{slug}_quantity"]}
    )

def checkout(request):
    return render(request, "shop/checkout.html")

def user_dashboard(request):
    return render(request, "shop/user-dashboard.html")