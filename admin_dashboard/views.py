import re
from django.http import HttpResponse
from django.shortcuts import render

from shop.views import product_detail
from .utils import add_product_to_list_session_handler,\
error_processor,attach_product_images,\
get_table_total_price,get_product
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
    return render(request, "admin_dashboard/partials/product-lists.html", context)

#DELETE PRODUCT
@attach_product_images
def delete_product_from_list(request, id, context = None):  
    
    product_details = context["product_details"]
    
    print("product details is = ",product_details)
    
    context["product_details"] = request.session["product_details"] = [product for product in \
        product_details if product["product_id"] != id ]

    return render(request, "admin_dashboard/partials/product-lists.html",context)           

# EDIT PRODUCT 
def edit_product_from_list(request, id):
    product = get_product(request,id)
    
    context = {
        "categories" : Category.objects.values("slug","name")
    }
    
    if product:
        context.update({
                "product_id": product["product_id"],
                "product_image_id":product["product_image_id"],
                "image_url" :  product["image_url"],
                "product_name":product["product_name"],
                "category_name": product["category_name"],
                "tag_name":product["tag_name"],
                "is_digital":product["is_digital"],
                "quantity":product["quantity"],
                "size":product["size"],
                "color":product["color"],
                "price":product["price"],
                "description":product["description"]
            }
        )
    return render(request, "admin_dashboard/partials/add-product-form.html",context)
        
    
    
    
    







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

