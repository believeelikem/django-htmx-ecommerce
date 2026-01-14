from email import message
import email
from multiprocessing import context
import re
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import login,logout, authenticate
from django.urls import reverse
from .utils import validate_user_input
from django_htmx.http import HttpResponseClientRedirect

User = get_user_model()

def sign_in(request):
    if request.method == "POST":
        email = request.POST.get("email-for-sign-in")
        password = request.POST.get("password")
        
        if all((email, password)):
            
            user = authenticate(request, email = email, password = password)
            
            print("user is ",user)
            if user is not None:
                  login(request, user)
                  
                  print("reverse for ",reverse("shop:home"))
                  response = HttpResponse(status=200)
                  response["Hx-Push"] = reverse("shop:home") 
                  response['HX-Redirect'] = reverse("shop:home")
                  return response
            else:
                context = {
                    "error":"Invalid Login credentials"
                }
                
                response =  render(request, "users/sign-in.html", context)
                response["Hx-Push"] = reverse("users:sign-in")
                print(reverse("users:sign-in"))
                return response
        else:
            print("something went wrong")
            
    if request.htmx:
        return render(request, "users/partials/_sign-in.html")       
    return render(request, "users/sign-in.html")

@validate_user_input
def validate_user_inputs(request, context):        
    return render(request, "users/partials/_email-error.html",context)

def user_dashboard(request):
    return render(request, "users/user-dashboard.html")

def sign_up(request):
    return render(request, "users/sign-up.html")

def profile(request):
    return render(request, "users/profile.html")

def password_reset(request):
    return render(request, "users/password-reset.html")

def password_update(request):
    return render(request, "users/password-update.html")