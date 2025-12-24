from email import message
import email
import re
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import login,logout, authenticate
from .utils import validate_user_input

User = get_user_model()

def sign_in(request):
    if request.method == "POST":
        email = request.POST.get("email-for-sign-in")
        password = request.POST.get("password")
        
        if all((email, password)):
            
            user = authenticate(request, email = email, password = password)
            
            print("user is ",user)
            # if user is not None:
            #       login(request)
            #       return render(request, "shop/index.html")  
            # else:
            #     re
        else:
            print("something went wrong")
    return render(request, "users/sign-in.html")


@validate_user_input
def validate_user_inputs(request, context):        
    return render(request, "users/partials/_email-error.html",context)


def sign_up(request):
    return render(request, "users/sign-up.html")

def profile(request):
    return render(request, "users/profile.html")

def password_reset(request):
    return render(request, "users/password-reset.html")

def password_update(request):
    return render(request, "users/password-update.html")