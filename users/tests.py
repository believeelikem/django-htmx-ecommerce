from django.test import TestCase
from django.http import HttpResponse

def home(request):
    return HttpResponse("Very Bad")