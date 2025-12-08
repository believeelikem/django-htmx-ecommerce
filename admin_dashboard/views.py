from django.http import HttpResponse
from django.shortcuts import render
from .utils import error_processor



def admin_dashboard(request):
    return render(
        request,
        "admin_dashboard/admin-dashboard.html",
        {"active_page": "dashboard"},
    )


def admin_orders(request):
    # if  request.htmx:
    #     print("htmx request")
    #     context = {"active_page": "orders"}
    #     return render(request, "admin_dashboard/partials/admin-orders.html",context)
    
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
    return render(
        request,
        "admin_dashboard/admin-products.html",
        {"active_page": "products"},
    )


@error_processor
def validate_product_add_error(request, error_message = "", css_class = ""):
    
    context = {
        "btn_is_valid":request.headers.get('HX-Request'),
        "message":error_message,
        "class":css_class
    }
    return render(request, "admin_dashboard/partials/product-add-errors.html", context)   
   

def admin_product_edit(request):
    return render(
        request,
        "admin_dashboard/admin-product-edit.html",
        {"active_page": "product-edit"},
    )


def admin_customers(request):
    return render(
        request,
        "admin_dashboard/admin-customers.html",
        {"active_page": "customers"},
    )


def admin_settings(request):
    return render(
        request,
        "admin_dashboard/admin-settings.html",
        {"active_page": "settings"},
    )


def admin_sign_in(request):
    return render(request, "admin_dashboard/admin-sign-in.html")


def admin_forgot_password(request):
    return render(request, "admin_dashboard/admin-forgot-password.html")

