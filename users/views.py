from email import message
import email
import re
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model

def sign_in(request):
    print("Hit here")
    return render(request, "users/sign-in.html")

def check_email(request):
    email = request.GET["email"]
    css_color = "red"
    message = f"no account with email '{email}' exists"
    if get_user_model().objects.filter(email = email).exists():
        css_color = "green"
        message = "✅"
        
    context = {
        "color":css_color,
        "message":message
    }
        
    return render(request, "users/partials/_email-error.html",context)

def sign_up(request):
    return render(request, "users/sign-up.html")

def profile(request):
    return render(request, "users/profile.html")

def password_reset(request):
    return render(request, "users/password-reset.html")

def password_update(request):
    return render(request, "users/password-update.html")