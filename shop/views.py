from email.mime import image
import re
from urllib import response
from webbrowser import get
from django import db
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Order, Product,ProductImage, Category
from django.db import connection
from django.db.models import F
from django.db.models.functions import Concat
from django.db.models import OuterRef, Subquery,Value, CharField
from .utils import *
from django.contrib import messages
from django.core.paginator import Paginator

def home(request):

    image_subquery = ProductImage.objects.filter(
        product=OuterRef('pk')
    ).order_by('id').values('photo')[:1]

    products = Product.objects.annotate(
        first_image_for_cover = Concat(
        Value('/media/'),
        Subquery(image_subquery),
        output_field=CharField()
    )
    ) 
    
    # request.session["cart"] = {}
    # print(request.session["cart"])
    
    cart = dict_cart(get_cart(request))
            
    for product in products:
        product.quantity_in_cart = \
        cart[f'{product.slug}-{product.details[0]["image_id"]}']["quantity"] \
        if cart and f'{product.slug}-{product.details[0]["image_id"]}' in cart else 0
    
    page = request.GET.get("page")
    if not page:
        page = 1
        
    p = Paginator(products, 3)
    
    products = p.get_page(page)    
    
    context = {
    "products":products,
    "categories": Category.objects.only("name","slug")
    }
    
    if request.htmx :
        if request.GET.get("from_paginated"):
            response = render(request, "shop/partials/_pagination.html", context)
            response["HX-Push-Url"] = f"?page={page}"
            return response
        
        return render(request, "shop/partials/_index.html", context = context )
    return render(request, "shop/index.html", context = context )

# def get_paginated_list(request, page_num):
#     p = Paginator(products, 3)
#     products = p.get_page(page_num)  
    
    
    

def cart(request):
    cart = dict_cart(get_cart(request))
    context = {
        "cart": cart,
        "mergeable_products":None
    }
    
    if request.user.is_authenticated:
        if request.session["cart"]:
            mergeable_products = get_cart_in_session(request.session)
            # print(mergeable_products)
            
            context["mergeable_products"] = mergeable_products
        
    if request.htmx:
        return render(request, "shop/partials/_cart.html",context)
    
    return render(request, "shop/cart.html", context)

def add_to_cart(request):
    cart = dict_cart(get_cart(request)) 
    order_item = get_order_item(request)    
    try:
        order_item["quantity"] = get_new_quantity_or_err(request, cart, order_item)
    except ValueError as e:
        messages.error(request, e)
    else:
        order_item["sub_total"] = f"{order_item['quantity'] * order_item['price'] :,.2f}" 

        if request.user.is_authenticated:
            order = get_order(request.user)
            order_item_to_db, created = OrderItem.objects.get_or_create(
                product = get_object_or_404(Product, slug = order_item["slug"]),
                color = order_item["color"],
                size = order_item["size"],
                price = order_item["price"],
                image_url = order_item["image_url"],
                image_id = order_item["image_id"],
            )  
            
            order_item_to_db.order = order
            order_item_to_db.quantity = order_item["quantity"]
            order_item_to_db.save()
            
            cart = dict_cart(get_cart(request))
            # some fields can be gotten in a cleaner way through chained db search
            # (fk relationships) but i add them here so we dont have to hit db 
            # when we want to access values like image_url etc
            # in cart view 
        else:  
            cart[f'{order_item["slug"]}-{order_item["image_id"]}'] = order_item
            request.session["cart"] = cart
            request.session.modified = True
            
        if "subtract" == request.POST.get("action"):
            messages.warning(request, f" -1({order_item['name']})  in cart")
        else:
            messages.success(request, f"{order_item['name']} added to cart")            
    
    context = {
        "new_count":get_new_count(cart,order_item["slug"],order_item["image_id"]),
        "product_id":order_item["product_id"],
        "from":None,
        "order_item":order_item
    }

    context["from"] = request.POST.get("from")    
    return render(request, "shop/partials/_cart-counter.html", context)

def merge_auth_unauth_cart(request):
    updated_cart = {}
    if request.user.is_authenticated:
        session_cart = get_cart_in_session(request.session)
        db_cart = dict_cart(get_cart_in_db(request.user))
        merged_item_count = 0
        unmergeable_items = ""
        
        for item in db_cart:
            if item in session_cart \
                and db_cart[item]["color"] == session_cart[item]["color"] \
                and db_cart[item]["size"] == session_cart[item]["size"]:
                    
                    
                    merged_item = merge_item(db_cart[item], session_cart[item])
                    product = get_object_or_404(Product, slug = merged_item["slug"])
                    
                    if merged_item["quantity"] <= int(get_current_val(
                        product.details,"quantity", 
                        merged_item["color"], merged_item["size"]
                    )):
                        
                        
                        order_item = OrderItem.objects.get(
                            product = product,
                            color = merged_item["color"],
                            size = merged_item["size"],
                            price = merged_item["price"],
                            image_url = merged_item["image_url"],
                            image_id = merged_item["image_id"],
                        ) 
                        order_item.quantity = merged_item["quantity"]
                        # order_item.sub_total = merged_item["sub_total"]
                        order_item.save()  
                        merged_item_count += 1
                    else:
                        merged_item["quantity"] = db_cart[item]["quantity"]
                        unmergeable_items += f"{merged_item['slug']}, "
                        
                    updated_cart[item] = merged_item

                    
            else:
                updated_cart[item] = db_cart[item]
        if merged_item_count:   
            messages.info(request, f"Succesfully merged {merged_item_count} item(s) into cart")   
             
        if unmergeable_items:
            messages.error(request,
                f'{unmergeable_items.rsplit(",",1)[0]} couldnt be merged because quantity exceeds available item quantity'
            )
            
    context = {
        "cart":updated_cart
    }
    request.session["cart"] = {}
    request.session.modified = True
    return render(request, "shop/partials/_cart_items.html",context )
    


    
    
    return updated_item

def remove_from_cart(request):
    if request.user.is_authenticated:
        order_item = get_object_or_404(
            OrderItem, 
            product_id = request.POST.get('product_id'),
            image_id = request.POST.get('image_id')
        )
        order_item.delete()
        
    else:
        del dict_cart(get_cart(request))[f"{request.POST.get('product_slug')}-{request.POST.get('image_id')}"]
        request.session.modified = True
        
    context = {
        "cart": dict_cart(get_cart(request))
    }
    context["from"] = request.POST.get("from")
    messages.error(request, f"Removed {request.POST.get('product_slug')} from cart successfully")
    return render(request, "shop/partials/_cart_items.html", context)

def remove_unauthenticated_cart(request):
    cart_size = len(request.session['cart'])
    request.session['cart'] = {}
    request.session.modified = True
    
    messages.error(request,f"Succesfully removed {cart_size} item(s) from unlogged cart ")

    return render(request, "shop/partials/_toasts.html")

def toast_clear(request):
    return HttpResponse("")

def product_detail(request,slug):
    
    product = get_object_or_404(Product, slug = slug)
    
    details = product.details
    # for detail in details:
    #     detail["image_url"] = (
    #         get_object_or_404(
    #             ProductImage,id = detail["image_id"]
    #             ).photo.url
    #     )   
    print("details = ",details)
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

def products(request):
    image_subquery = ProductImage.objects.filter(
        product=OuterRef('pk')
    ).order_by('id').values('photo')[:1]

    products = Product.objects.annotate(
        first_image_for_cover = Concat(
        Value('/media/'),
        Subquery(image_subquery),
        output_field=CharField()
    )
    ) 

    cart = dict_cart(get_cart(request))
            
    for product in products:
        product.quantity_in_cart = \
        cart[f'{product.slug}-{product.details[0]["image_id"]}']["quantity"] \
        if cart and f'{product.slug}-{product.details[0]["image_id"]}' in cart else 0
    
    context = {
        "products": products
    }
    
    return render(request, "shop/product-listings.html", context)

def category_detail(request, slug):
    category = get_object_or_404(
        Category, slug = slug
    )
    
    image_subquery = ProductImage.objects.filter(
        product=OuterRef('pk')
    ).order_by('id').values("photo")[:1]
    
    
    category_products = Product.objects.filter(
        categories = category ).annotate(
            first_image_for_cover = Subquery(image_subquery)
        )
    
    context = {
        "category":category,
        "category_products":category_products
    }
    
    return render(request, "shop/category_detail.html",context)

def checkout(request):
    return render(request, "shop/checkout.html")

