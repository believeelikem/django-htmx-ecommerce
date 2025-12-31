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
        cart = get_cart_in_session(request.session)
            
        for product in products:
            # print("details = ", product.details)
            # splt_url = get_object_or_404(ProductImage, id = product.details[0]['image_id']).photo.url.split("/")[-1]
            # print("obj is = ",splt_url)
            # print("= ",request.session["cart"][f"{product.slug}-{splt_url}"])
            product.quantity_in_cart = request.session["cart"][f"{product.slug}-{get_object_or_404(ProductImage, id=product.details[0]['image_id']).photo.url.split('/')[-1]}"]["quantity"] if cart and product.slug in request.session["cart"] else 0
            # print(product.quantity_in_cart)

            
    # print(len(request.session["cart"]))
        
    context = {
    "products":products,
    "total_cart_count": len(request.session["cart"])
    }
        
    if request.htmx:
        return render(request, "shop/partials/_index.html", context = context )
    return render(request, "shop/index.html", context = context )


def cart(request):
    context = {
        "cart":request.session["cart"]
    }
    
    for item in request.session["cart"]:
        print(item," = ",request.session["cart"][item])
        
    
    if request.htmx:
        return render(request, "shop/partials/_cart.html",context)
    
    return render(request, "shop/cart.html", context)

def add_to_cart(request):
    if request.user.is_authenticated:
        ...
    else:
        cart = get_cart_in_session(request.session)
        
        order_item = get_order_item(request)

        order_item["quantity"] = get_new_quantity(request, cart, order_item)
        order_item["subtotal"] = f"{order_item['quantity'] * order_item['price'] :,.2f}" 
        cart[f'{order_item["slug"]}-{order_item["image_url"].split("/")[-1]}'] = order_item
        request.session["cart"] = cart
        request.session.modified = True
        context = {
            "new_count":request.session["cart"][f'{order_item["slug"]}-{order_item["image_url"].split("/")[-1]}']["quantity"],
            "total_cart_count": len(request.session["cart"]),
            "product_id":order_item["product_id"],
            "from":None,
            "order_item":order_item
        }
        
       
        context["from"] = request.POST.get("from")
            
        return render(request, "shop/partials/_cart-counter.html", context)

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
    print(details)
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
    
    context = {
        "variants":details,
        "sizes": get_related_specifics(details,key = "size"),
        "colors":get_related_specifics(details, key= "color"), 
        "current":current,
        "product_name":product.name,
        "product_id":product.id,
        "product_slug":product.slug,
        "available_sizes":available_sizes,
        "product_quantity":product_quantity,
        "related_products":related_products,
        "total_cart_count": len(request.session["cart"])
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