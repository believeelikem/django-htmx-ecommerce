from django.shortcuts import render
from django.http import HttpResponse



def admin_dashboard(request):
    return render(request, "admin_dashboard/admin-dashboard.html")

def admin_orders(request):
    return render(request, "admin_dashboard/admin-orders.html")

