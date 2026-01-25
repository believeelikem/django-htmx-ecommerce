from django.urls import path
from shop import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("cart/", views.cart, name="cart"),
    path("products/", views.products, name="product-listings"),
    # path("products/detail/", views.product_detail, name="product-detail"),
    path("checkout/", views.checkout, name="checkout"),
    path("categories/<slug:slug>", views.category_detail, name="category-detail"),
]


htmx_patterns = [
    path("products/<slug:slug>/detail/", views.product_detail, name="product-detail"),
    path("decrease-quantity/<slug:slug>/", views.decrease_quantity, name="decrease-quantity"),
    path("increase-quantity/<slug:slug>/", views.increase_quantity, name="increase-quantity"),
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("toast-clear/", views.toast_clear, name="toast-clear"),
    path("remove-from-cart", views.remove_from_cart, name="remove-from-cart"),
    path("remove-unlogged-cart", views.remove_unauthenticated_cart, name="remove-unlogged-cart"),
    path("merge-auth-unauth-cart", views.merge_auth_unauth_cart, name="merge-auth-unauth-cart"),
    path("paystack/initiate_payment", views.initialize_payment, name="initiate-payment"),
    path("paystack/callback", views.paystack_callback, name = "paystack-callback"),
]

urlpatterns += htmx_patterns