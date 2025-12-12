import re
from django.http import HttpResponse
from django.shortcuts import render

from shop.views import product_detail
from .utils import add_to_list_session_handler,\
error_processor,attach_product_images, get_table_total_price
from shop.models import  Product, ProductImage, Category
from .models import TempImage



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
          
def admin_product_add(request):
    print(request.headers.get("HX-Target"))
    
    categories = Category.objects.all()
    
    context = {
        "active_page": "product-edit",
        "categories":categories,
    }

    request.session.flush()   
  
    if "product_details" in request.session:   
        if request.session["product_details"]:
            print("has product details = ", bool(request.session["product_details"]))
            context["product_details"] = request.session["product_details"]
            
            context = attach_product_images(context)
            
            context["total_price"] = f"{get_table_total_price(context['product_details']):,} "
            
        
    if  request.htmx:
        return render(request, "admin_dashboard/partials/admin-product-add.html",context)

    return render(request,"admin_dashboard/admin-product-add.html", context)


@add_to_list_session_handler
def add_product_to_list(request,context = None):
    context_images_attached = attach_product_images(context)
    # print("**** the final request sent *******")
    # print(request.session["product_details"]) 
    if context_images_attached:
        context = context_images_attached
    context["total_price"] = f"{get_table_total_price(context['product_details']):,} "
    return render(request, "admin_dashboard/partials/product-lists.html", context)




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

