import re
from django.http import HttpResponse
from django.shortcuts import render

from shop.views import product_detail
from .utils import (
    add_product_to_list_session_handler,error_processor,
    attach_product_images,get_product,refix_editing_status
)
from shop.models import  Product, ProductImage, Category
from .models import TempImage
from django.shortcuts import get_object_or_404


def admin_dashboard(request):
    if  request.htmx:
        context = {"active_page": "dashboard"}
        return render(request, "admin_dashboard/partials/admin-dashboard.html",context)

    return render(
        request,
        "admin_dashboard/admin-dashboard.html",
        {"active_page": "dashboard"},
    )


def admin_orders(request):
    print(request.headers.get("HX-Target"))

    if  request.htmx:
        context = {"active_page": "orders"}
        return render(request, "admin_dashboard/partials/admin-orders.html",context)
    
    return render(
        request,
        "admin_dashboard/admin-orders.html",
        {"active_page": "orders"},
    )

def admin_order_detail(request):
    return render(
        request,
        "admin_dashboard/admin-order-detail.html",
        {"active_page": "orders"},
    )


# < -------   PRODUCTS    -------- >

def admin_products(request):
    if  request.htmx:
        context = {"active_page": "products"}
        return render(request, "admin_dashboard/partials/admin-products.html",context)
    
    return render(
        request,
        "admin_dashboard/admin-products.html",
        {"active_page": "products"},
    )

#VALIDATE INPUTS
@error_processor
def validate_product_add_error(request, error_message = "", css_class = ""):
    print(request.headers.get("HX-Target"))
    
    context = {
        "btn_is_valid":request.headers.get('HX-Request'),
        "message":error_message,
        "class":css_class
    }
    return render(request, "admin_dashboard/partials/product-add-errors.html", context)   
   
def create_product(request):
    if request.method == "POST":
        print(request.POST)
 
# ADMIN-PRODUCT-ADD 
@attach_product_images          
def admin_product_add(request, context = None):
    refix_editing_status(request)
    categories = Category.objects.values("slug","name")
    # request.session.flush()
    
    context.update( 
        {
        "active_page": "product-edit",
        "categories":categories,
        "is_create_view":True
        }
    )    
    
    if  request.htmx:
        return render(request, "admin_dashboard/partials/admin-product-add.html",context)

    return render(request,"admin_dashboard/admin-product-add.html", context)

#ADD-TO-LIST
@add_product_to_list_session_handler
@attach_product_images
def add_product_to_list(request,context = None):
    return render(request, "admin_dashboard/partials/product-lists.html", context)

#DELETE PRODUCT
@attach_product_images
def delete_product_from_list(request, id, context = None):  
    
    product_details = context["product_details"]

    context["product_details"] = request.session["product_details"] = [product for product in \
        product_details if product["product_id"] != id ]
       
    return render(request, "admin_dashboard/partials/product-lists.html",context)           


# EDIT PRODUCT 
def edit_product_from_list(request, id):
    product = get_product(request,id)
    
    a_product_already_being_edited = None
    
    
    for _product in request.session["product_details"]:
        if  _product != product  and  _product["is_being_edited"]:
            _product["is_being_edited"] = False
            request.session.modified = True
            a_product_already_being_edited = _product
            break      
            
    context = {
        "categories" : Category.objects.values("slug","name")
    }
    
    if a_product_already_being_edited:
        context["a_product_already_being_edited_id"] = a_product_already_being_edited
        
    if product:
        index = request.session["product_details"].index(product)
        product["is_being_edited"] = True
        request.session["product_details"][index] = product
        request.session.modified = True
        context["product"] = product
        
    if request.htmx:       
        return render(request, "admin_dashboard/partials/add-product-form.html",context)
    
    return render(request, "admin_dashboard/admin-product-add.html", context)
        
  
def product_image_modal(request, id):
    image_url = get_product(request, id)["image_url"]
    
    return render(request, "admin_dashboard/partials/product-image-modal.html", context={"image_url":image_url})
      
    



def admin_customers(request):
    if  request.htmx:
        context = {"active_page": "customers"}
        return render(request, "admin_dashboard/partials/admin-customers.html",context)
       
    return render(
        request,
        "admin_dashboard/admin-customers.html",
        {"active_page": "customers"},
    )


def admin_settings(request):
    if  request.htmx:
        context = {"active_page": "settings"}
        return render(request, "admin_dashboard/partials/admin-settings.html",context)
    
    return render(
        request,
        "admin_dashboard/admin-settings.html",
        {"active_page": "settings"},
    )


def admin_sign_in(request):
    return render(request, "admin_dashboard/admin-sign-in.html")


def admin_forgot_password(request):
    return render(request, "admin_dashboard/admin-forgot-password.html")

