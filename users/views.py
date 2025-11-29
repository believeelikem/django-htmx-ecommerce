import re
from django.shortcuts import render
from django.http import HttpResponse


def sign_in(request):
    return render(request, "users/sign-in.html")

def sign_up(request):
    return render(request, "users/sign-up.html")

def profile(request):
    return render(request, "users/profile.html")

def password_reset(request):
    return render(request, "users/password-reset.html")

def password_update(request):
    return render(request, "users/password-update.html")