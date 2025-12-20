from hmac import new
import re
from django.http import HttpResponse
from django.shortcuts import redirect, render

from shop.views import product_detail
from .utils import (
    add_product_to_list_session_handler,error_processor,
    attach_product_images,get_product,refix_editing_status,
    get_product_already_being_edited,set_product_editing_status,
    product_update_in_list,save_to_db
)
from shop.models import  Product, ProductImage, Category
from .models import TempImage
from django.shortcuts import get_object_or_404
from django.contrib import messages
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
    new_image_chosen = False
    product = None
    # error_message = error_message
    
    if isinstance(error_message, dict):
        print("error is = ",error_message)
        new_image_chosen = error_message["new_image_chosen"]
        product = get_product(request, int(error_message["product_id"]))
        error_message = error_message["error_message"]
        
    
    context = {
        "btn_is_valid":request.headers.get('HX-Request'),
        "message":error_message,
        "class":css_class
    }
    
    if new_image_chosen:
        context.update({"new_image_chosen":True})
        
    
    context.update({
            "product":product
        })
        
    return render(request, "admin_dashboard/partials/product-add-errors.html", context)   
 
# ADMIN-PRODUCT-ADD 
@attach_product_images          
def admin_product_add(request, context = None):
    if "product_details" in request.session:    
        refix_editing_status(request)
    categories = Category.objects.values("slug","name")
    
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
    print("len of details is  = ",len(request.session["product_details"]))
    
    context["is_create_view"] = True
    context["categories"] = Category.objects.values("slug","name")
    messages.success(request, "Product added successfully")
    return render(request, "admin_dashboard/partials/product-lists.html", context)


#DELETE PRODUCT
@attach_product_images
def delete_product_from_list(request, id, context = None):  
    
    product_details = context["product_details"]

    context["product_details"] = request.session["product_details"] = [product for product in \
        product_details if product["product_id"] != id ]
    
    messages.error(request, "Product deleted successfully")
       
    return render(request, "admin_dashboard/partials/product-lists.html",context)           

# EDIT PRODUCT 
def get_product_edit_form(request, id):
    product = get_product(request,id)
    
    a_product_already_being_edited = get_product_already_being_edited(
        request, new_product=product
    )
            
    context = {
        "categories" : Category.objects.values("slug","name"),
        "product_details":request.session["product_details"],
        "from_edit":True
    }
    
    if a_product_already_being_edited:
        context["a_product_already_being_edited_id"] = a_product_already_being_edited
                
    if product:
        context["product"] = set_product_editing_status(request, product)
        
    if request.htmx:       
        return render(request, "admin_dashboard/partials/add-product-form.html",context)
    
    return render(request, "admin_dashboard/admin-product-add.html", context)
        
# PRODUCT IMAGE MODAL
def product_image_modal(request, id):
    image_url = get_product(request, id)["image_url"]
    
    context={"image_url":image_url}
    return render(request, "admin_dashboard/partials/product-image-modal.html", context)


# PRODUCT UPDATE-SAVE
@product_update_in_list
@attach_product_images
def save_product_update_to_list(request, context = None):
    
    context["is_create_view"] = True
    Category.objects.values("slug","name")
    messages.info(request, "Product edited successfully")
    return render(request, "admin_dashboard/partials/product-lists.html", context)

def clear_all_products_from_list(request):   
    if "product_details" in request.session:
        del request.session["product_details"]
        request.session.modified = True
    messages.error(request,"Cleared data from list")
    return render(request, "admin_dashboard/partials/product-lists.html")

def cancel_toast(request):
    return render(request,"admin_dashboard/partials/cancel_toast.html")

@save_to_db
def save_products_to_db(request):
    if "product_details" in request.session:
        del request.session["product_details"]
        request.session.modified = True
    return render(request, "admin_dashboard/partials/product-lists.html")

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
    request.session.flush()
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

