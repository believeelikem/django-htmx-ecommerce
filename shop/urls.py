from django.urls import path
from shop import views


urlpatterns = [
    path("", views.shop, name="dashboard"),
    path("cart/", views.cart, name="cart"),
    path("products/", views.products, name="products"),
]