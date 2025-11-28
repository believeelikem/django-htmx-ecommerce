import re
from django.http import HttpResponse
from django.shortcuts import render

def shop(request):
    return render(request, "shop/index.html")

def cart(request):
    return render(request, "shop/cart.html")

def products(request):
    return render(request, "shop/product_listings.html")