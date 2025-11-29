from django.urls import path
from admin_dashboard import views

urlpatterns = [
    path("", views.admin_dashboard, name="admin-dashboard"),   
    path("orders/", views.admin_orders, name="admin-orders"),   
]