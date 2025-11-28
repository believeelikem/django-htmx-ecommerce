from django.http import HttpResponse
from django.shortcuts import render

def shop(request):
    return HttpResponse("Welcome to shop app")
