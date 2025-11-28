import re
from django.http import HttpResponse
from django.shortcuts import render

from admin_dashboard.views import dashboard

def shop(request):
    return render(request, "shop/index.html")

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