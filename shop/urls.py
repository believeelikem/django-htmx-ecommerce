from django.urls import path
from shop import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("cart/", views.cart, name="cart"),
    path("products/", views.products, name="product-listings"),
    # path("products/detail/", views.product_detail, name="product-detail"),
    path("checkout/", views.checkout, name="checkout"),
    path("user-dashboard/", views.user_dashboard, name="dashboard"),
]


htmx_patterns = [
    path("products/<slug:slug>/detail/", views.product_detail, name="product-detail"),
    path("decrease-quantity/<slug:slug>/", views.decrease_quantity, name="decrease-quantity"),
    path("increase-quantity/<slug:slug>/", views.increase_quantity, name="increase-quantity"),
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("toast-clear/", views.toast_clear, name="toast-clear"),
    path("remove-from-cart", views.remove_from_cart, name="remove-from-cart"),
]

urlpatterns += htmx_patterns